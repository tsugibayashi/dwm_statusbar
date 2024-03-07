#!/usr/bin/python3
# -*- coding: utf8 -*-
import sys
import datetime
import subprocess
import time
import argparse
import psutil
from mpd import MPDClient
import alsaaudio

### functions
# def output_component_names() -> None: {{{
def output_component_names() -> None:
    print('--- Available component names ---')
    print('hm  : date and time (yyyy-MM-dd HH:mm)')
    print('hms : date and time (yyyy-MM-dd HH:mm:ss)')
    print('bat : battery percentage')
    print('vol : audio volume percentage')
    print('cpu : cpu temperature')
    print('aud : Audacious status')
    print('mpd : MPD status')
    print('xbacklight : screen brightness status using xbacklight')
    print('light      : screen brightness status using light')
    return None
# }}}
# def date_time(date_format :str) -> str: {{{
def date_time(date_format :str) -> str:
    today = datetime.datetime.now()

    if date_format == 'hm':
        current_time = today.strftime('%F %R')
    elif date_format == 'hms':
        current_time = today.strftime('%F %T')
    else:
        current_time = ''

    return current_time
# }}}
# def battery_percentage() -> str: {{{
def battery_percentage() -> str:
    battery = psutil.sensors_battery()
    return str(int(battery.percent)) + '%'
# }}}
# def cpu_temperature() -> str: {{{
def cpu_temperature() -> str:
    tempFile = open("/sys/class/thermal/thermal_zone0/temp")
    temp_cpu0 = tempFile.read()
    tempFile.close()
    return str(float(temp_cpu0) / 1000) + '°C'
# }}}
# def audacious_status() -> str: {{{
def audacious_status() -> str:
    try:
        status = subprocess.run(["audtool", "playback-status"],
                                stdout=subprocess.PIPE,
                                check=True).stdout.decode().strip()
    except subprocess.CalledProcessError:
        return ''

    if status == 'playing':
        current_song = subprocess.run(["audtool", "--current-song"],
                                stdout=subprocess.PIPE,
                                check=True).stdout.decode().strip()
        current_song_length = subprocess.run(["audtool", "--current-song-length"],
                                stdout=subprocess.PIPE,
                                check=True).stdout.decode().strip()
        current_song_output_length = subprocess.run(["audtool", "--current-song-output-length"],
                                stdout=subprocess.PIPE,
                                check=True).stdout.decode().strip()
        return current_song + ' ' \
                 + current_song_output_length + '/' + current_song_length
    else:
        return ''
# }}}
# def mpd_status() -> str: {{{
def mpd_status() -> str:
    # Connects to local MPD server
    client = MPDClient()
    try:
        client.connect("localhost", 6600)
    except:
        return ''
    
    dict_status = client.status()
    if dict_status["state"] == "play":
        dict_currentsong = client.currentsong()
    
        # Current time of current song
        elapsed = round(float(dict_status["elapsed"]))
        min_elapsed, sec_elapsed = divmod(elapsed, 60)
    
        # Total time of current song
        duration = round(float(dict_currentsong["duration"]))
        min_duration, sec_duration = divmod(duration, 60)
    
        artist = dict_currentsong["artist"]
        title  = dict_currentsong["title"]
    
        current_song = artist + ' - ' + title + ' ' \
              + str(min_elapsed) + ':' + str(sec_elapsed).zfill(2) \
              + '/' + str(min_duration) + ':' + str(sec_duration).zfill(2)
    else:
        current_song = ''
    
    # Disconnects from local MPD server
    client.close()
    client.disconnect()

    return current_song
# }}}
# def xbacklight_status() -> str: {{{
def xbacklight_status() -> str:
    try:
        percent_str = subprocess.run(["xbacklight"],
                                stdout=subprocess.PIPE,
                                check=True).stdout.decode().strip()
    except subprocess.CalledProcessError:
        return ''

    percentage = float(percent_str)
    return str(round(percentage, 1))
# }}}
# def light_status() -> str: {{{
def light_status() -> str:
    try:
        percent_str = subprocess.run(["light"],
                                stdout=subprocess.PIPE,
                                check=True).stdout.decode().strip()
    except subprocess.CalledProcessError:
        return ''

    percentage = float(percent_str)
    return str(round(percentage, 1))
# }}}
# def vol_percentage(control :str) -> str: {{{
def vol_percentage(control :str) -> str:
    try:
        m = alsaaudio.Mixer(control)
        list_m = m.getvolume()
    except:
        return '-:-'

    return ':'.join(map(str, list_m))
# }}}
# def output_status(components :list) -> str: {{{
def output_status(components :list) -> str:
    delimiter = u'\u2502'
    #delimiter = '| '
    list_statusbar = list()

    for comp in components:
        if comp == 'hm' or comp == 'hms':
            list_statusbar.append(date_time(comp))
        elif comp == 'bat':
            list_statusbar.append(battery_percentage())
        elif comp == 'cpu':
            list_statusbar.append(cpu_temperature())
        elif comp == 'aud':
            list_statusbar.append(audacious_status())
        elif comp == 'mpd':
            list_statusbar.append(mpd_status())
        elif comp == 'xbacklight':
            list_statusbar.append(xbacklight_status())
        elif comp == 'light':
            list_statusbar.append(light_status())
        elif comp == 'vol':
            list_statusbar.append(vol_percentage('Master'))

    statusbar = delimiter.join(list_statusbar)
    #print(statusbar)

    return statusbar
# }}}

### main routine
parser = argparse.ArgumentParser()
parser.add_argument('--comps', type=str, required=True, nargs="+", help='a list of component names')
parser.add_argument('--wait', type=int, required=True, help='sleep seconds')
args = parser.parse_args()
#print(args.comps)
#print(args.wait)
#print(type(args.wait))

# Check specified component names
for comp in args.comps:
    if comp not in ['hm', 'hms', 'bat', 'vol', 'cpu', 'aud', 'xbacklight', 'light']:
        print('[Error] unrecognized component name:', comp)
        output_component_names()
        quit()

while True:
    statusbar = output_status(args.comps)
    subprocess.run(["xsetroot", "-name", statusbar])
    time.sleep(args.wait)

