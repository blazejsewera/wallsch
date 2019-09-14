from wallsch.wallsch import WallpaperScheduler
from pathlib import Path
import Pyro4


@Pyro4.expose
@Pyro4.behavior(instance_mode='single')
class WallpaperSchedulerService(object):
    def __init__(self, daemon):
        super(WallpaperSchedulerService, self).__init__()
        self.wallsch = WallpaperScheduler()
        self.wallsch.initialize()
        self.daemon = daemon

    def lock_screen(self):
        self.wallsch.lock_screen()

    def change_wallpaper(self):
        self.wallsch.update_wallpaper()

    def update_filelist(self):
        self.wallsch.update_filelist()

    def shutdown(self):
        self.daemon.shutdown()


def main():
    pid_file = Path.home()/Path('.config/wallsch/pid')
    daemon = Pyro4.Daemon()
    # uri = daemon.register(WallpaperSchedulerService)
    wss = WallpaperSchedulerService(daemon)
    uri = daemon.register(wss)

    with pid_file.open(mode='w') as pid:
        pid.write(str(uri))

    daemon.requestLoop()
    daemon.close()
