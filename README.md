# dwmstatusbar
> ⚠️ This project has moved to [Codeberg](https://codeberg.org/tsugibayashi/pyoutput_status).

A dwm statusbar implemented with Python

## Prerequisites

Install packages if you use components bat, mpd, or vol.

| Component | Required package (Ubuntu and Debian) | Required package (Arch) |
----|----|----
| bat | python3-psutil | python-psutil |
| mpd | python3-mpd | python-mpd2 |
| vol | python3-alsaaudio | python-pyalsaaudio |

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

### Component name

| Component | Description |
----|----
| hm | Date and time in '%F %R'. |
| hms | Date and time in '%F %T'. |
| bat | Battery percentage. This component uses python3-psutil. |
| upower | Battery percentage. This component uses upower. |
| vol | Audio volume. This component uses python3-alsaaudio. |
| amixer | Audio volume. This component uses amixer. |
| cpu | Cpu temperature. |
| aud | Audacious status. This component uses audtool. |
| mpd | MPD status. This component uses python3-mpd. |
| xbacklight | Backlight status. This component uses xbacklight. |
| light | Backlight status. This component uses light. |

