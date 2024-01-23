# dwmstatusbar
A dwm statusbar implemented in Python

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
$ cp -p dwm_statusbar/dwmstatusbar.py /usr/local/bin/
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
# Wait until an audio device is enabled.
while true; do
    AMIXER_NUM=`amixer | wc -l`
    if [ $AMIXER_NUM -gt 0 ]; then
        break
    fi
    sleep 1
done

# execute dwmstatusbar.py
/usr/local/bin/dwmstatusbar.py bat_hms 1 &  #battery and date(yyyy-MM-dd HH:mm:ss)
#/usr/local/bin/dwmstatusbar.py bat_cpu_hm 1 &  #battery, cpu temp., and date(yyyy-MM-dd HH:mm)
#/usr/local/bin/dwmstatusbar.py bat_cpu_hms 1 &  #battery, cpu temp., and date(yyyy-MM-dd HH:mm:ss)
#/usr/local/bin/dwmstatusbar.py mpd_vol_light_bat_hms 1 &  #mpd status, audio volume, brightness, battery, and date(yyyy-MM-dd HH:mm:ss)

# Window Manager
/usr/bin/dwm
```

