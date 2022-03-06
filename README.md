# dwm_statusbar.py
A dwm statusbar implemented in Python

## Prerequisites

Install python-mpd2 and psutil.

For example,
```Shell
$ sudo apt install python3 psutil python3-mpd
```

## Installation

Install dwm_statusbar.py.

For example,
```Shell
$ git clone https://github.com/tsugibayashi/dwm_statusbar.py.git
$ cp -p dwm_statusbar.py/dwm_statusbar.py /usr/local/bin/
```

## How to use

Edit $HOME/.xsession or $HOME/.xprofile.

For example,
```Shell
# Statubar loop for dwm
while true; do
        /usr/local/bin/dwm_statusbar.py bat_hms    # battery and date(yyyy-MM-dd HH:mm:ss)
        #/usr/local/bin/dwm_statusbar.py bat_cpu_hm     # battery, cpu, and date(yyyy-MM-dd HH:mm)
        #/usr/local/bin/dwm_statusbar.py bat_cpu_hms    # battery, cpu, and date(yyyy-MM-dd HH:mm:ss)
        #/usr/local/bin/dwm_statusbar.py mpd_bat_hms    # mpd status, battery, and date(yyyy-MM-dd HH:mm:ss)

        sleep 1s    # Update every second
        #sleep 5s    # Update every 5 seconds
        #sleep 1m    # Update every minute
done &

# Window Manager
/usr/bin/dwm
```

