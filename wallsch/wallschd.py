from wallsch import WallpaperScheduler
from pathlib import Path
import Pyro4


@Pyro4.expose
@Pyro4.behavior(instance_mode='single')
class WallpaperSchedulerService(object):
    def __init__(self):
        super(WallpaperSchedulerService, self).__init__()
        self.wallsch = WallpaperScheduler()
        self.wallsch.initialize()

    def lock_screen(self):
        self.wallsch.lock_screen()

    def change_wallpaper(self):
        self.wallsch.update_wallpaper()

    def update_filelist(self):
        self.wallsch.update_filelist()


if __name__ == '__main__':
    pid_file = Path.home()/Path('.config/wallsch/pid')
    daemon = Pyro4.Daemon()
    # uri = daemon.register(WallpaperSchedulerService)
    wss = WallpaperSchedulerService()
    uri = daemon.register(wss)

    with pid_file.open(mode='w') as pid:
        pid.write(str(uri))

    try:
        daemon.requestLoop()
    except (KeyboardInterrupt, SystemExit):
        daemon.shutdown()
