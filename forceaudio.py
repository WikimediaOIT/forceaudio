#!/usr/bin/python

"""
Simple script to force the audio device and levels for audio in and out

FIXME: Determine optimum input and output volumes for other device types
"""

import sys
import subprocess

# Device preferences
# (higher preference level means USE ME FIRST)
device_prefs = {
    'Chat' : {
        'preference' : 100,
        'volume_out': 50,
        'volume_in' : 70,
        },
    'Jabra SPEAK' : {
        'preference' : 90,
        'volume_out': 83,
        'volume_in' : 100,
    },
    'Phnx Spider' : {
        'preference' : 110,
        'volume_out': 60,
        'volume_in' : 60,
    },
    'MDR-10RBT' : {
        'preference' : 10,
        'volume_out': 60,
        'volume_in' : 60,
    }
}

debug=True

# cli utility to change audio device, found on github
# https://github.com/deweller/switchaudio-osx
# needs to be compiled with xcode and 'installed' somehwhere locally
audioswitcher='./audioswitcher'

def run_me(cmd):
    p = subprocess.Popen(cmd, shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
    # Check exit code
    if p.wait() != 0:
        print('Error running: %s' % cmd)
        print(p.stdout.read())
        sys.exit(2)
    return(p)

def set_input(device):
    run_me('%s -t input -s "%s"' % (audioswitcher, device))

def set_output(device):
    run_me('%s -t output -s "%s"' % (audioswitcher, device))
    return(True)

def list_devices():
    p = run_me('%s -a' % (audioswitcher))
    return(p.stdout.readlines())

# NOTE: osascript with these options work in 10.10, but may fail <10.9
def set_output_volume(level=80):
    run_me('osascript -e "set Volume output volume %s"' % (level))
    return(True)

def set_input_volume(level=80):
    run_me('osascript -e "set Volume input volume %s"' % (level))
    return(True)

# Main
if __name__ == "__main__":
    device=False
    preference=0

    if debug: print 'Devices Found:'
    for line in list_devices():
        if debug: print line,

        # Check device list against known devices
        for knowndevice in device_prefs.keys():
            if knowndevice in line:

                # If device has a higher preference, use it.
                if device_prefs[knowndevice]['preference'] > preference:
                    device = line.split("(")[0].strip()
                    preference = device_prefs[knowndevice]['preference']
                    volume_out = device_prefs[knowndevice]['volume_out']
                    volume_in  = device_prefs[knowndevice]['volume_in']

    if device:
        print 'Forcing Audio Device:\n', device, volume_out, volume_in
        set_input(device)
        set_output(device)

        set_output_volume(volume_out)
        set_input_volume(volume_in)
