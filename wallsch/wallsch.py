from datetime import datetime, timedelta
from suntime import Sun
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
from pathlib import Path
import json
import inspect
import random
import subprocess
from . import config


class WallpaperScheduler(object):
    # Parsed from config.json
    wallpaper_dir = None
    day_subdir = 'day'
    night_subdir = 'night'
    blurred_dir = None
    interval = 5

    # Runtime variables
    filelist = {}
    current_subdir = 'day'
    current_wallpaper = None
    is_day = True

    sun = None
    sunrise_time = None
    sunset_time = None

    executors = {
        'default': ThreadPoolExecutor(2)
    }
    scheduler = BackgroundScheduler(executors=executors)

    def initialize(self):
        self.parse_config()
        self.load_filelist()
        self.refresh_sun()
        now = config.local_timezone.localize(datetime.now())
        if now < self.sunrise_time or now >= self.sunset_time:
            self.set_day(False)
        else:
            self.set_day(True)

        self.scheduler.add_job(self.update_wallpaper,
                               'interval',
                               minutes=self.interval,
                               max_instances=1)

        # log
        if config.VERBOSE:
            self.scheduler.print_jobs()

        try:
            self.scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            self.scheduler.shutdown(wait=False)

    def parse_config(self):
        '''
        Method parsing config file or setting default values
        '''
        with config.CONFIG_FILE.open(mode='r') as cf:
            config_dict = json.load(cf)
        self.wallpaper_dir = Path(config_dict['wallpaper_dir'])
        self.day_subdir = config_dict['day_subdir']
        self.night_subdir = config_dict['night_subdir']
        self.blurred_dir = Path(config_dict['blurred_dir'])
        self.interval = config_dict['interval']
        self.sun = Sun(config_dict['latitude'], config_dict['longitude'])

    def load_filelist(self):
        '''
        Method loading filelist in order not to scan the wp directory everytime
        '''
        try:
            with config.FILELIST_FILE.open(mode='r') as ff:
                self.filelist = json.load(ff)
        except FileNotFoundError:
            self.update_filelist()

    def refresh_sun(self):
        '''
        Method refreshing sunrise and sunset times.
        Should be executed after parsing the config
        and every 00:00.
        '''
        now = config.local_timezone.localize(datetime.now())
        tomorrow = now.date() + timedelta(days=1)
        self.sunrise_time = self.sun.get_local_sunrise_time()
        if now < self.sunrise_time:
            self.scheduler.add_job(self.set_day,
                                   trigger='date',
                                   args=[True],
                                   run_date=self.sunrise_time,
                                   replace_existing=True)
        self.sunset_time = self.sun.get_local_sunset_time()
        if now < self.sunset_time:
            self.scheduler.add_job(self.set_day,
                                   trigger='date',
                                   args=[False],
                                   run_date=self.sunset_time,
                                   replace_existing=True)
        self.scheduler.add_job(self.refresh_sun,
                               trigger='date',
                               run_date=tomorrow)

    def set_day(self, is_day):
        '''
        Method called by apscheduler when day rises or night comes
        or the daemon is started
        '''
        self.is_day = is_day
        if is_day:
            self.current_subdir = self.day_subdir
        else:
            self.current_subdir = self.night_subdir
        self.update_wallpaper()

        # log
        if config.VERBOSE:
            print('It is day now.') if is_day else print('It is night now.')

    def update_wallpaper(self):
        '''
        Method called always after set_night/set_day
        and every hour (or different time interval)
        '''
        if self.is_day:
            self.current_wallpaper = random.choice(self.filelist['day'])
        else:
            self.current_wallpaper = random.choice(self.filelist['night'])

        wallpaper_to_set = '{0}/{1}/{2}'.format(
                self.wallpaper_dir.absolute().as_posix(),
                self.current_subdir,
                self.current_wallpaper)

        wallsch_loc = Path(inspect.getabsfile(WallpaperScheduler))

        # log
        if config.VERBOSE:
            print(f'Path dir: {self.wallpaper_dir.absolute().as_posix()}')
            print(f'Wallpaper to set: {wallpaper_to_set}')

        if config.SIMPLE_SCRIPT:
            simple = wallsch_loc.parent/Path('set_wallpaper_simple')
            subprocess.run(
                [
                    simple.absolute().as_posix(),
                    wallpaper_to_set
                ],
                stdout=subprocess.DEVNULL)

        else:
            script = Path(wallsch_loc).parent/Path('set_wallpaper')
            subprocess.run(
                [
                    script.absolute().as_posix(),
                    wallpaper_to_set
                ],
                stdout=subprocess.DEVNULL)

    def update_filelist(self):
        '''
        Method to scan wallpaper folders
        and make a json database with the filenames.
        '''
        if config.VERBOSE:
            print('Filelist update started.')

        day_dir = self.wallpaper_dir/Path(self.day_subdir)
        self.filelist['day']\
            = [f.name for f in day_dir.iterdir() if f.is_file()]

        night_dir = self.wallpaper_dir/Path(self.night_subdir)
        self.filelist['night']\
            = [f.name for f in night_dir.iterdir() if f.is_file()]

        with config.FILELIST_FILE.open(mode='w') as ff:
            json.dump(self.filelist, ff)

        if config.VERBOSE:
            print('Filelist update finished.')

    def lock_screen(self):
        '''
        Method to lock the screen using the blurred wallpaper
        '''
        wallsch_loc = inspect.getabsfile(WallpaperScheduler)
        lockscreen_script = Path(wallsch_loc).parent/Path('lockscreen.sh')
        blurred_wallpaper_to_set = '{0}/{1}/{2}'.format(
                self.blurred_dir.absolute().as_posix(),
                self.current_subdir,
                self.current_wallpaper)

        subprocess.run(
            [
                lockscreen_script.absolute().as_posix(),
                blurred_wallpaper_to_set
            ],
            stdout=subprocess.DEVNULL)
