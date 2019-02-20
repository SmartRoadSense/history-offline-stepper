#!/usr/bin/python
import config
import multiprocessing
import numpy as np
import subprocess
import os
import time


MERGE_CHECK_PERIOD = 1

def get_core_count():
    return multiprocessing.cpu_count()


NUM_CORES = get_core_count()


def create_environment():
    env = os.environ.copy()
    raw_config = config.raw_config()
    env['RAW_DB_HOST'] = raw_config['host']
    env['RAW_DB_PORT'] = raw_config['port']
    env['RAW_DB_NAME'] = raw_config['database']
    env['RAW_DB_USER'] = raw_config['user']
    env['RAW_DB_PASS'] = raw_config['password']

    agg_config = config.agg_config()
    env['AGG_DB_HOST'] = agg_config['host']
    env['AGG_DB_PORT'] = agg_config['port']
    env['AGG_DB_NAME'] = agg_config['database']
    env['AGG_DB_USER'] = agg_config['user']
    env['AGG_DB_PASS'] = agg_config['password']

    return env


def serialize(data: list):
    data = map(lambda a: str(a), data)
    return ",".join(data)


def launch(script, parameters, osm_ids):
    process_list = []

    if len(osm_ids) < 1:
        return process_list

    # divide inputs in evenly sized chunks
    input_lists = np.array_split(osm_ids, NUM_CORES)
    print("input args:")
    print(input_lists)

    for i in range(0, NUM_CORES, 1):

        if len(input_lists[i]) > 0:

            proc_env = create_environment()
            proc_env["args"] = serialize(input_lists[i].tolist())

            print("launching {0} {1}".format([script, parameters], proc_env["args"]))

            process_list.append(
                # subprocess.Popen(['ping', '8.8.8.8'], env=proc_env))  # TODO change with actual values PHP and script
                # subprocess.Popen([script, parameters], env=proc_env))  # TODO change with actual values PHP and script
                subprocess.Popen([script, parameters], env=proc_env))  # TODO change with actual values PHP and script

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
            print(processes[i].pid, ' Process exited with return code {0}'.format(processes[i].returncode))


