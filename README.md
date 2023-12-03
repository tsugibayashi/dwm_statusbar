# dwm_statusbar.py
A dwm statusbar implemented in Python

## Prerequisites

Install python-mpd2, psutil, and python3-alsaaudio.

Ubuntu and Debian
```bash
$ sudo apt install python3-psutil python3-mpd python3-alsaaudio
```

Arch
```bash
$ sudo pacman -S python-psutil python-mpd2
```

## Installation

Install dwm_statusbar.py.

For example,
```bash
$ git clone https://github.com/tsugibayashi/dwm_statusbar.py.git
$ cp -p dwm_statusbar.py/dwm_statusbar.py /usr/local/bin/
```

Arch
```bash
$ git clone https://github.com/tsugibayashi/aur.git
$ cd aur/dwm_statusbar.py/
$ makepkg -si
```

## How to use

Edit $HOME/.xinitrc, $HOME/.xsession, or $HOME/.xprofile.

For example,
```bash
/usr/local/bin/dwm_statusbar.py bat_hms 1 &  # battery and date(yyyy-MM-dd HH:mm:ss)
#/usr/local/bin/dwm_statusbar.py bat_cpu_hm 1 &  # battery, cpu, and date(yyyy-MM-dd HH:mm)
#/usr/local/bin/dwm_statusbar.py bat_cpu_hms 1 &  # battery, cpu, and date(yyyy-MM-dd HH:mm:ss)
#/usr/local/bin/dwm_statusbar.py mpd_bat_hms 1 &  # mpd status, battery, and date(yyyy-MM-dd HH:mm:ss)

# Window Manager
/usr/bin/dwm
```

