import Pyro4
from pathlib import Path
import sys


def main(argv):
    pid_file = Path.home()/Path('.config/wallsch/pid')
    with pid_file.open(mode='r') as pid:
        uri = str(pid.read())

    wallsch = Pyro4.Proxy(uri)

    for cmd in argv:
        if cmd == 'lock':
            try:
                wallsch.lock_screen()
            except Pyro4.errors.CommunicationError:
                print('Daemon not running.')
                exit()
        elif cmd == 'update':
            try:
                wallsch.update_filelist()
            except Pyro4.errors.CommunicationError:
                print('Daemon not running.')
                exit()
        elif cmd == 'change':
            try:
                wallsch.update_wallpaper()
            except Pyro4.errors.CommunicationError:
                print('Daemon not running.')
                exit()
        else:
            print('Wrong command. Available commands:\n'
                  '  update - update file list (use after adding\n'
                  '    or removing files in wallpaper directory)\n'
                  '  change - change the wallpaper immediately\n'
                  '  lock - lock the screen')


if __name__ == '__main__':
    main(sys.argv[1:])
