#!/usr/bin/env python
import os
import sys
import fnmatch
import time
import subprocess

sassc_binary = 'sassc'
check_interval = .2
base_dir = os.path.dirname(os.path.abspath(__file__))
sass_dir = os.path.join(base_dir, 'suit', 'sass')


def watch_file():
    def get_scss_files():
        return [
            os.path.join(dirpath, f)
            for dirpath, dirnames, files in os.walk(sass_dir)
            for f in fnmatch.filter(files, '*.scss')]

    scss_files = get_scss_files()

    def get_props():
        l = []
        for scss_file in scss_files:
            l.append(str(os.stat(scss_file).st_mtime))
        return ','.join(l)

    def write(s):
        sys.stdout.write(s + os.linesep)
        sys.stdout.flush()

    def on_change():
        cmd = '%s -t compact %s/suit.scss %s/static/suit/css/suit.css' % \
              (sassc_binary, sass_dir, base_dir)
        err = subprocess.call(cmd, shell=True)
        if err == 0:
            write(cmd)

    write('Watching for changes in %s dir...' % sass_dir)
    this = last = get_props()
    while 1:
        if this > last:
            last = this
            on_change()

        this = get_props()
        time.sleep(check_interval)


if __name__ == "__main__":
    try:
        watch_file()
    except KeyboardInterrupt:
        pass
