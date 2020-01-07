import Pyro4
from pathlib import Path
import sys


def main():
    argv = sys.argv[1:]

    try:
        pid_file = Path.home()/Path('.config/wallsch/pid')
        with pid_file.open(mode='r') as pid:
            uri = str(pid.read())
    except FileNotFoundError:
        print('Config not found. Creating')
        from wallsch import tools
        tools.make_config()

    wallsch = Pyro4.Proxy(uri)

    for cmd in argv:
        if cmd == 'lock':
            try:
                wallsch.lock_screen()
            except Pyro4.errors.CommunicationError:
                print('Daemon not running.')
                exit(1)
        elif cmd == 'update':
            try:
                wallsch.update_filelist()
            except Pyro4.errors.CommunicationError:
                print('Daemon not running.')
                exit(1)
        elif cmd == 'change':
            try:
                wallsch.change_wallpaper()
            except Pyro4.errors.CommunicationError:
                print('Daemon not running.')
                exit(1)
        elif cmd == 'mkconfig':
            from wallsch import tools
            tools.make_config()
        elif cmd == 'close':
            try:
                wallsch.shutdown()
            except Pyro4.errors.CommunicationError:
                print('Daemon not running.')
                exit(0)
        elif cmd == 'help':
            print('Available commands:\n'
                  '  update - update file list (use after adding\n'
                  '    or removing files in wallpaper directory)\n'
                  '  change - change the wallpaper immediately\n'
                  '  lock - lock the screen\n'
                  '  close - shutdown the daemon\n'
                  '  mkconfig - interactively make a new config file')
        else:
            print('Wrong command. Available commands:\n'
                  '  update - update file list (use after adding\n'
                  '    or removing files in wallpaper directory)\n'
                  '  change - change the wallpaper immediately\n'
                  '  lock - lock the screen\n'
                  '  close - shutdown the daemon\n'
                  '  mkconfig - interactively make a new config file')


if __name__ == '__main__':
    main()
