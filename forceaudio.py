#!/usr/bin/python

"""
Simple script to force the audio device and levels for audio in and out

FIXME: Specifically add other devices (eg. JabraSpeak)
FIXME: Determine optimum input and output volumes for other device types
FIXME: Build a dictionary of preferred devices, set options, priority

"""

import sys
import subprocess

# cli utility to change audio device, found on github
# https://github.com/deweller/switchaudio-osx
# needs to be compiled with xcode and 'installed' somehwhere locally
audioswitcher='./audioswitcher'

def run_me(cmd):
    p = subprocess.Popen(cmd, shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)

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
def set_input_volume(level=80):
    run_me('osascript -e "set Volume input volume %s"' % (level))
    return(True)

def set_output_volume(level=80):
    run_me('osascript -e "set Volume output volume %s"' % (level))
    return(True)

# Main
if __name__ == "__main__":
    device=False
    print 'Devices Found:'
    for line in list_devices():
        print line,
        if 'Chat 160' in line:
            device = line.split("(")[0].strip()

    if device:
        print '\nForcing Audio Device:\n', device
        set_input(device)
        set_output(device)

        set_input_volume(80)
        set_output_volume(80)
