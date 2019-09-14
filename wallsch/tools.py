import json
from pathlib import Path
from wallsch import config


def make_config():
    '''
    Method to make a config file interactively
    '''
    config_dir = config.CONFIG_FILE.parent
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

    day_subdir = input('Subdirectory for daytime wallpapers: ')
    night_subdir = input('Subdirectory for nighttime wallpapers: ')

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

    config_dict = {
        'latitude': latitude,
        'longitude': longitude,
        'wallpaper_dir': wallpaper_dir.as_posix(),
        'day_subdir': day_subdir,
        'night_subdir': night_subdir,
        'blurred_dir': blurred_dir.as_posix(),
        'interval': interval
    }

    with config.CONFIG_FILE.open(mode='w') as cf:
        json.dump(config_dict, cf, indent=2)

    print('Config written to `~/.config/wallsch/config.json`.')
    print('You can edit the file there manually.')
