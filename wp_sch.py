from datetime import datetime
from suntime import Sun, SunTimeException
from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
import pytz
import tzlocal
from pathlib import Path
import json


class WallpaperScheduler(object):
    def __init__(self):
        super(WallpaperScheduler, self).__init__()

    CONFIG_FILE = Path.home()/Path('.config/wallsch/config.json')

    wallpaper_dir = None
    blurred_dir = None

    local_timezone = tzlocal.get_localzone()
    sun = None

    sunrise_time = None
    sunset_time = None

    interval = 60

    is_day = True

    executors = {
        'default': ThreadPoolExecutor(1)
    }
    scheduler = BlockingScheduler(executors=executors)

    def print_sunrise_sunset(self):
        print('Sunrise: {0}, sunset: {1}'
              .format(self.sun.get_local_sunrise_time(),
                      self.sun.get_local_sunset_time()))

    def initialize(self):
        pass  # TODO: refresh everything at the start of a daemon
        self.refresh_sun()
        now = self.local_timezone.localize(datetime.now())
        if now < self.sunrise_time or now >= self.sunset_time:
            self.set_day(False)
        else:
            self.set_day(True)

        self.scheduler.add_job(self.update_wallpaper,
                               'interval',
                               minutes=self.interval,
                               max_instances=1)

        self.scheduler.print_jobs()

        try:
            self.scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            self.scheduler.shutdown(wait=False)

    def parse_config(self):
        '''
        Method parsing config file or setting default values
        '''
        with self.CONFIG_FILE.open(mode='r') as cf:
            config = json.load(cf)
        self.wallpaper_dir = Path(config['wallpaper_dir'])
        self.blurred_dir = Path(config['blurred_dir'])
        self.interval = config['interval']
        self.sun = Sun(config['latitude'], config['longitude'])

    def refresh_sun(self):
        '''
        Method refreshing sunrise and sunset times.
        Should be executed after parsing the config
        and every 00:00.
        '''
        now = self.local_timezone.localize(datetime.now())
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

    def set_day(self, is_day):
        '''
        Method called by apscheduler when day rises or night comes
        or the daemon is started
        '''
        pass  # TODO: implementation
        self.is_day = is_day
        self.update_wallpaper()
        # log
        print('It is day now.') if is_day else print('It is night now.')

    def update_wallpaper(self):
        '''
        Method called always after set_night/set_day
        and every hour (or different time interval)
        '''
        pass  # TODO: implementation
        # log
        if self.is_day:
            print('Wallpaper update (day)!')
        else:
            print('Wallpaper update (night)!')

    def update_filelist(self, path):
        pass

    def make_config(self):
        '''
        Method to make a config file interactively
        '''
        config_dir = self.CONFIG_FILE.parent()
        print('Creating `~/.config/wallsch`...')
        try:
            config_dir.mkdir(parents=True)
        except FileExistsError:
            print('Directory `~/.config/wallsch` already exists. Skipping.')

        while True:
            wallpaper_dir = Path(input('Wallpaper directory: ')).absolute()
            if wallpaper_dir.exists():
                break
            else:
                print('This path does not exist. Check the input.')

        while True:
            blurred_dir = Path(input('Blurred directory: ')).absolute()
            if blurred_dir.exists():
                break
            else:
                print('This path does not exist. Check the input.')

        while True:
            try:
                latitude = float(input('Latitude: '))
            except (TypeError, ValueError):
                print('The number is invalid. Input the number as a float.')
            if latitude < 90.0 and latitude > -90.0:
                break
            else:
                print('Latitude should be between -90 and 90 degrees.')

        while True:
            try:
                longitude = float(input('Longitude: '))
            except (TypeError, ValueError):
                print('The number is invalid. Input the number as a float.')
            if longitude < 180.0 and longitude > -180.0:
                break
            else:
                print('Longitude should be between -180 and 180 degrees.')

        while True:
            try:
                interval = int(input('Interval between changes (minutes): '))
            except (TypeError, ValueError):
                print('The number is invalid. Input the number as an int.')
                continue
            break

        config = {
            'latitude': latitude,
            'longitude': longitude,
            'wallpaper_dir': wallpaper_dir.as_posix(),
            'blurred_dir': blurred_dir.as_posix(),
            'interval': interval
        }

        with self.CONFIG_FILE.open(mode='w') as cf:
            json.dump(config, cf, indent=2)

        print('Config written to `~/.config/wallsch/config.json`.')
        print('You can edit the file there manually.')


if __name__ == '__main__':
    wallsch = WallpaperScheduler()
    wallsch.print_sunrise_sunset()
    wallsch.make_config()
