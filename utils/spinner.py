import sys
import time

def spinning_cursor():
    while True:
        for cursor in '|/-\\':
            yield cursor
            

spinner = spinning_cursor()

def spinning(isRun):
    if isRun:
        sys.stdout.write(next(spinner))
        sys.stdout.flush()
        time.sleep(0.1)
        sys.stdout.write("\b")