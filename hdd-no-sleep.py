#!/usr/bin/env python3

import ctypes
import sys
import random
import os
import atexit
import time
import string
import traceback

def on_exit():
    input('* Press enter to continue: ')

def get_drives():
    drive_bits = ctypes.windll.kernel32.GetLogicalDrives()
    drives = []
    for name in string.ascii_uppercase:
        if drive_bits & 1:
            drives.append(name + ':')
        drive_bits >>= 1
    return drives

def main():
    if sys.platform != 'win32':
        os.execvp('py.exe', ['py.exe', sys.argv[0]])

    if not ctypes.windll.shell32.IsUserAnAdmin():
        ret = ctypes.windll.shell32.ShellExecuteW(None, 'runas', sys.executable, f'"{sys.argv[0]}"', None, 1)
        if ret <= 32:
            print(f'* ShellExecuteW error: {ret}')
            return
        return

    atexit.register(on_exit)

    print('* Reading random data to prevent hard disks from sleeping...')

    while True:
        for drive in get_drives():
            try:
                with open(rf'\\.\{drive}', 'rb') as fp:
                    fp.seek(512 * random.randrange(1024 * 1024))
                    fp.read(1)
            except:
                print('* Error while reading random data:', file=sys.stderr)
                traceback.print_exc()

        time.sleep(30 - 1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        atexit.unregister(on_exit)
