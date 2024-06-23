#!/usr/bin/python3
# -*- coding: utf8 -*-
import sys
import datetime
import subprocess
import time
import argparse
import shutil

flag_comps = {
               'hm': True,
               'hms': True,
               'bat': True,
               'upower': True,
               'vol': True,
               'amixer': True,
               'cpu': True,
               'aud': True,
               'mpd': True,
               'mpc': True,
               'xbacklight': True,
               'light': True
             }

try:
    import psutil
except ImportError as err:
    flag_comps['bat'] = False
try:
    from mpd import MPDClient
except ImportError as err:
    flag_comps['mpd'] = False
try:
    import alsaaudio
except ImportError as err:
    flag_comps['vol'] = False

### functions
# def output_component_names() -> None: {{{
def output_component_names() -> None:
    print('--- Available component names ---')
    print('hm     : date and time (yyyy-MM-dd HH:mm)')
    print('hms    : date and time (yyyy-MM-dd HH:mm:ss)')
    print('bat    : battery percentage using python-psutil')
    print('upower : battery percentage using upower')
    print('vol    : audio volume percentage using python-alsaaudio')
    print('amixer : audio volume percentage using amixer')
    print('cpu    : cpu temperature')
    print('aud    : Audacious status using audtool')
    print('mpd    : MPD status using python-mpd')
    print('mpc    : MPD status using mpc')
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
# def battery_percentage_2() -> str: {{{
def battery_percentage_2() -> str:
    try:
        # List objects paths for devices
        devices = subprocess.run(["upower", "-e"],
                            stdout=subprocess.PIPE,
                            check=True).stdout.decode().strip()
    except subprocess.CalledProcessError:
        return ''

    device_list = devices.splitlines()
    for line in device_list:
        if 'battery' in line:
            battery_path = line

    try:
        # Show information about battery device
        battery_info = subprocess.run(["upower", "-i", battery_path],
                            stdout=subprocess.PIPE,
                            check=True).stdout.decode().strip()
    except subprocess.CalledProcessError:
        return ''

    battery_list = battery_info.splitlines()
    for line in battery_list:
        if 'percentage' in line:
            bat_percentage = line.split()[1]

    return bat_percentage
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
# def mpd_status_2() -> str: {{{
def mpd_status_2() -> str:
    try:
        mpd_status = subprocess.run(["mpc", "-f", "%artist% - %title%"],
                            stdout=subprocess.PIPE,
                            check=True).stdout.decode().strip()
    except subprocess.CalledProcessError:
        return ''

    status_list = mpd_status.splitlines()
    if len(status_list) < 3:
        return ''

    artist_title = status_list[0]
    song_time = status_list[1].split()[2]

    current_song = artist_title + ' ' + song_time
    return current_song
# }}}

# def xbacklight_status() -> str: {{{
def xbacklight_status() -> str:
    try:
        #percent_str = subprocess.run(["xbacklight"],
        percent_str = subprocess.run(["xbacklight", "-get"],
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
# def get_vol(line :str) -> str: {{{
def get_vol(line :str) -> str:
    percent_vol = ''

    cols = line.split(' ')
    for col in cols:
        if '%]' in col:
            percent_vol = col.replace('%]', '').replace('[', '')
            break

    return percent_vol
# }}}
# def vol_percentage_2(control :str) -> str: {{{
def vol_percentage_2(control :str) -> str:
    try:
        control_str = subprocess.run(["amixer", "sget", control],
                        stdout=subprocess.PIPE,
                        check=True).stdout.decode().strip()
    except subprocess.CalledProcessError:
        return '-:-'

    control_list = control_str.splitlines()
    #print(control_list)
    for line in control_list:
        if 'Front Left:' in line:
            #print(line)
            left_vol = get_vol(line)
        elif 'Front Right:' in line:
            #print(line)
            right_vol = get_vol(line)
        elif 'Mono:' in line:
            left_vol = get_vol(line)
            right_vol = left_vol
            break

    return left_vol + ':' + right_vol
# }}}

# def output_status(components :list, flag_comps :dict) -> str: {{{
def output_status(components :list, flag_comps :dict) -> str:
    delimiter = u'\u2502'
    #delimiter = '| '
    list_statusbar = list()

    for comp in components:
        if comp == 'hm' and flag_comps['hm']:
            list_statusbar.append(date_time(comp))
        elif comp == 'hms' and flag_comps['hms']:
            list_statusbar.append(date_time(comp))
        elif comp == 'bat' and flag_comps['bat']:
            list_statusbar.append(battery_percentage())
        elif comp == 'upower' and flag_comps['upower']:
            list_statusbar.append(battery_percentage_2())
        elif comp == 'cpu' and flag_comps['cpu']:
            list_statusbar.append(cpu_temperature())
        elif comp == 'aud' and flag_comps['aud']:
            list_statusbar.append(audacious_status())
        elif comp == 'mpd' and flag_comps['mpd']:
            list_statusbar.append(mpd_status())
        elif comp == 'mpc' and flag_comps['mpc']:
            list_statusbar.append(mpd_status_2())
        elif comp == 'xbacklight' and flag_comps['xbacklight']:
            list_statusbar.append(xbacklight_status())
        elif comp == 'light' and flag_comps['light']:
            list_statusbar.append(light_status())
        elif comp == 'vol' and flag_comps['vol']:
            list_statusbar.append(vol_percentage('Master'))
        elif comp == 'amixer' and flag_comps['amixer']:
            list_statusbar.append(vol_percentage_2('Master'))

    statusbar = delimiter.join(list_statusbar)
    #print(statusbar)

    return statusbar
# }}}

### main routine
parser = argparse.ArgumentParser()
parser.add_argument('--comps', type=str, required=True, nargs="+", help='a list of component names')
parser.add_argument('--wait', type=int, required=True, help='sleep seconds')
parser.add_argument('--output', type=str, required=False, help='output type')
args = parser.parse_args()
#print(args.comps)
#print(args.wait)
#print(type(args.wait))
#print(args.output)

# Check specified component names
for comp in args.comps:
    if comp not in ['hm', 'hms', 'bat', 'upower', 'vol', 'amixer',
                    'cpu', 'aud', 'mpd', 'mpc', 'xbacklight', 'light']:
        print('[Error] unrecognized component name:', comp, file=sys.stderr)
        output_component_names()
        quit()

    if comp == 'aud':
        if shutil.which('audtool') is None:
            flag_comps['aud'] = False

    for command in ['xbacklight', 'light', 'amixer', 'upower', 'mpc']:
        if comp == command:
            if shutil.which(command) is None:
                flag_comps[command] = False

while True:
    statusbar = output_status(args.comps, flag_comps)

    if args.output is None:
        subprocess.run(["xsetroot", "-name", statusbar])
    else:
        print(statusbar)

    time.sleep(args.wait)

