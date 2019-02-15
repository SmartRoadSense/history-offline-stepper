#!/usr/bin/python
import multiprocessing
import numpy as np
import subprocess
import time

MERGE_CHECK_PERIOD = 1

def get_core_count():
    return multiprocessing.cpu_count()


NUM_CORES = get_core_count()


def launch(script, parameters, osm_ids):
    process_list = []

    if len(osm_ids) < 1:
        return process_list

    # divide inputs in evenly sized chunks
    input_lists = np.array_split(osm_ids, NUM_CORES)

    for i in range(0, NUM_CORES - 1, 1):
        if len(input_lists[i]) > 0:
            process_list.append(
                subprocess.Popen(['ping', '8.8.8.8']))  # TODO change with actual values PHP and script
            # subprocess.Popen([script, parameters, input_lists[i]]))  # TODO change with actual values PHP and script

    return process_list


def merge(processes):
    flags = [False for p in processes]

    seconds = 0

    while True:
        for i, pro in enumerate(processes):
            flags[i] = pro.poll()

        time.sleep(MERGE_CHECK_PERIOD)
        seconds = seconds + 1

        if any(f is not None for f in flags):
            break

    for i, f in enumerate(flags):
        if f != 0:
            print(processes[i].pid, ' Process exited with return code %d' % processes[i].returncode)


inputs = range(50)
procs = launch(None, inputs)

merge(procs)
