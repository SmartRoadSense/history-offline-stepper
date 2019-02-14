#!/usr/bin/python
import multiprocessing
import numpy as np
import subprocess
import time


def get_core_count():
    return multiprocessing.cpu_count()


def launch(script, osm_ids):

    # TOCHECK: divide inputs in evenly sized chunks
    input_lists = np.array_split(osm_ids, get_core_count())


# work with this framework
p = subprocess.Popen(['ping', '-t', '8.8.8.8'])

seconds = 0

while p.poll() is None:
    print('Still sleeping')
    time.sleep(1)
    seconds = seconds + 1

    if seconds > 10:
        p.terminate()


print('Not sleeping any longer.  Exited with return code %d' % p.returncode)
