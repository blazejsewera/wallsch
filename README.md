https://github.com/jazzsewera/wallsch# Wallsch
A simple wallpaper scheduler daemon.

Designed to work with feh, but works also with different wallpaper programs.
Supports locking the screen with a blurred version of the background.
As for now, you will have to blur the background manually, but automatic blurring will be added in the future.

## Preparation
Find yourself some fancy wallpapers and split them into two directories:
`{your_wallpaper_directory}/day` and `{your_wp_dir}/night` to your liking.
If you don't know where to start, consider: [Wallpaper subreddit](https://reddit.com/r/wallpaper) or [Wallhaven](https://wallhaven.cc).
Blur all the wallpapers and put them in `{your_blur_dir}/day` and `{your_blur_dir}/night` (the same filenames and hierarchy as in wallpaper directory) if you want to use i3lock with blurred backgrounds. If not, simply put the same path in the blurred backgrounds as wallpaper backgrounds in the `wallschctl mkconfig`

## Installing
From AUR: wallsch-git

or manually

```
sudo python3 setup.py install
```

You will have to install scripts from scripts folder manually. To do this:
```
sudo install -Dm 755 scripts/set-wallpaper scripts/lockscreen /usr/bin
```
Note that lockscreen script requires i3-lock. If you do not intend to use screen locking with i3-lock, you can omit this script.

## Configuring
After installation, run
```
wallschctl mkconfig
```
And put in all the required information. Use absolute paths to avoid errors.
This data is stored locally on you computer, never uploaded.

Remember to put the `wallschd` (if you're using nitrogen) or `wallschd -e` (to use the extended wallpaper changing script) command in your startup config (eg. `~/.config/i3/config` or `.xinitrc`).

> Made with <3 by thejazzroot  
> (C) 2019 Błażej Sewera  
> License: MPL 2.0
