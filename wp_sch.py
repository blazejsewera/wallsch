# import datetime
from suntime import Sun, SunTimeException
from apscheduler.schedulers.background import BackgroundScheduler
import pytz
import tzlocal


class WallpaperScheduler(object):
    def __init__(self, arg):
        super(WallpaperScheduler, self).__init__()

    local_timezone = tzlocal.get_localzone()
    config_timezone = pytz.timezone('Europe/Warsaw')
    warsaw_coords = 52.237049, 21.017532  # TODO: cfg file with coords and tz
    sun = Sun(*warsaw_coords)

    scheduler = BackgroundScheduler()

    def print_sunrise_sunset(self):
        print('Sunrise: {0}, sunset: {1}'
              .format(self.sun.get_local_sunrise_time(),
                      self.sun.get_local_sunset_time()))

    def initialize(self):
        pass  # TODO: refresh everything at the start of a daemon

    def parse_config(self, path):
        '''
        Method parsing config file or setting default values
        '''
        pass  # TODO: implementation

    def refresh_sun(self):
        '''
        Method refreshing sunrise and sunset times every 00:00
        and every start of a daemon
        '''
        pass  # TODO: implementation

    def set_day(self):
        '''
        Method called by apscheduler when day rises
        or the daemon is started at day
        '''
        pass  # TODO: implementation

    def set_night(self):
        '''
        Method called by apscheduler when night comes
        or the daemon is started at night
        '''
        pass  # TODO: implementation

    def update_wallpaper(self):
        '''
        Method called always after set_night/set_day
        and every hour (or different time interval)
        '''
        pass  # TODO: implementation

    def make_config(self):
        '''
        Method to make a config file interactively
        '''
        pass  # TODO: implementation


if __name__ == '__main__':
    wp_sch = WallpaperScheduler()
    wp_sch.print_sunrise_sunset()
