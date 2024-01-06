# dwm_statusbar
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

Install dwm_statusbar.py.

For example,
```bash
$ git clone https://github.com/tsugibayashi/dwm_statusbar.git
$ cp -p dwm_statusbar/dwm_statusbar.py /usr/local/bin/
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
while true; do
    # execute dwm_statusbar.py
    if [[ -z $(pgrep -U $UID -f dwm_statusbar.py) ]]; then
        /usr/local/bin/dwm_statusbar.py bat_hms 1 &  # battery and date(yyyy-MM-dd HH:mm:ss)
        #/usr/local/bin/dwm_statusbar.py bat_cpu_hm 1 &  # battery, cpu temp., and date(yyyy-MM-dd HH:mm)
        #/usr/local/bin/dwm_statusbar.py bat_cpu_hms 1 &  # battery, cpu temp., and date(yyyy-MM-dd HH:mm:ss)
        #/usr/local/bin/dwm_statusbar.py mpd_vol_light_bat_hms 1 &  # mpd status, audio volume, brightness, battery, and date(yyyy-MM-dd HH:mm:ss)
    fi

    sleep 1s  # Update every second
done &

# Window Manager
/usr/bin/dwm
```

