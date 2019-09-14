from wallsch import WallpaperScheduler
from pathlib import Path
import Pyro4
import sys
import getopt


@Pyro4.expose
@Pyro4.behavior(instance_mode='single')
class WallpaperSchedulerService(object):
    def __init__(self, daemon, verbose, extended):
        super(WallpaperSchedulerService, self).__init__()
        self.wallsch = WallpaperScheduler(verbose, extended)
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
    argv = sys.argv[1:]

    pid_file = Path.home()/Path('.config/wallsch/pid')
    daemon = Pyro4.Daemon()

    verbose = False
    extended = False

    try:
        opts, args = getopt.getopt(argv, 've')
    except getopt.GetoptError:
        print('Available options:\n'
              '  -v - verbose output\n'
              '  -e - extended shell script (simple one only supports feh)')
        exit(1)

    for opt, _ in opts:
        if opt == '-v':
            verbose = True
        elif opt == '-e':
            extended = True

    wss = WallpaperSchedulerService(daemon, verbose, extended)
    uri = daemon.register(wss)

    with pid_file.open(mode='w') as pid:
        pid.write(str(uri))

    daemon.requestLoop()
    daemon.close()


if __name__ == '__main__':
    main()
