# dwmstatusbar
A dwm statusbar implemented with Python

## Prerequisites

Install python3-psutil, python3-mpd, and python3-alsaaudio.

Ubuntu and Debian
```bash
$ sudo apt install python3-psutil python3-mpd python3-alsaaudio
```

Arch
```bash
$ sudo pacman -S python-psutil python-mpd2
$ yay -S python-pyalsaaudio
```

## Installation

Install dwmstatusbar.py.

For example,
```bash
$ git clone https://github.com/tsugibayashi/dwm_statusbar.git
$ cp -p dwm_statusbar/dwmstatusbar.py /usr/bin/
```

Arch
```bash
$ git clone https://github.com/tsugibayashi/aur.git
$ cd aur/dwm_statusbar/
$ makepkg -si
```

## How to use

Edit $HOME/.xinitrc, $HOME/.xsession, or $HOME/.xprofile.

For example,
```bash
# create $HOME/log
if [ ! -d $HOME/log ]; then
    mkdir $HOME/log
fi

# execute dwmstatusbar.py
date > $HOME/log/dwmstatusbar.log
/usr/bin/dwmstatusbar.py --comps bat hms --wait 1 >>$HOME/log/dwmstatusbar.log 2>&1 &  #battery and date(yyyy-MM-dd HH:mm:ss)
#/usr/bin/dwmstatusbar.py --comps bat cpu hm --wait 1 &  #battery, cpu temp., and date(yyyy-MM-dd HH:mm)
#/usr/bin/dwmstatusbar.py --comps bat cpu hms --wait 1 &  #battery, cpu temp., and date(yyyy-MM-dd HH:mm:ss)
#/usr/bin/dwmstatusbar.py --comps mpd vol light bat hms --wait 1 &  #mpd status, audio volume, brightness, battery, and date(yyyy-MM-dd HH:mm:ss)

# Window Manager
/usr/bin/dwm
```

