from datetime import datetime
from suntime import Sun, SunTimeException
from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
import pytz
import tzlocal


class WallpaperScheduler(object):
    def __init__(self):
        super(WallpaperScheduler, self).__init__()

    local_timezone = tzlocal.get_localzone()
    warsaw_coords = 52.237049, 21.017532  # TODO: cfg file with coords and tz
    sun = Sun(*warsaw_coords)

    sunrise_time = datetime(2019, 1, 1)
    sunset_time = datetime(2019, 1, 1)

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
        pass  # TODO: implementation

    def refresh_sun(self):
        '''
        Method refreshing sunrise and sunset times every 00:00
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

    def update_filelist(self):
        pass

    def make_config(self):
        '''
        Method to make a config file interactively
        '''
        pass  # TODO: implementation


if __name__ == '__main__':
    wp_sch = WallpaperScheduler()
    wp_sch.print_sunrise_sunset()
    wp_sch.initialize()
