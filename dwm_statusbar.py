#!/usr/bin/python3
# -*- coding: utf8 -*-
import sys
import datetime
import subprocess
import psutil
from mpd import MPDClient

### functions
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
    client.connect("localhost", 6600)
    
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
# def func_xsetroot(output_funcs :str) -> str: {{{
def func_xsetroot(output_funcs :str) -> str:
    list_statusbar = list()

    list_functions = output_funcs.split('_')
    for i in list_functions:
        if i == 'hm' or i == 'hms':
            list_statusbar.append(date_time(i))
        elif i == 'bat':
            list_statusbar.append(battery_percentage())
        elif i == 'cpu':
            list_statusbar.append(cpu_temperature())
        elif i == 'aud':
            list_statusbar.append(audacious_status())
        elif i == 'mpd':
            list_statusbar.append(mpd_status())

    statusbar = '| '.join(list_statusbar)
    #print(statusbar)
    subprocess.run(["xsetroot", "-name", statusbar])
# }}}

### main routine
if len(sys.argv) < 2:
    print('[Error] input $2, underbar delimited functions')
    print('        ex. b_hms, c_b_hm, m_b_hms')
    print('--function name--')
    print('hm  : date and time (yyyy-MM-dd HH:mm)')
    print('hms : date and time (yyyy-MM-dd HH:mm:ss)')
    print('bat : battery percentage')
    print('cpu : cpu temperature')
    print('aud : Audacious status')
    print('mpd : MPD status')
    quit()

output_funcs = sys.argv[1]

func_xsetroot(output_funcs) 

