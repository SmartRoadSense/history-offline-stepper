#!/usr/bin/python
import databaseutils as db
import timeframe

if __name__ == '__main__':
    conn = db.connect()

    date_range = db.get_date_range(conn)
    frames = timeframe.get_time_frames(*date_range)

    # TODO: clean out tables: current, history

    for tf_index, f in enumerate(frames):

        print(tf_index, f)
        # TODO: 1) clean out single_data table
        # TODO: 2) populate single_data table
        # TODO: 3) apply special (no filtering on old data points) aggregation
        # on single_data table (note: NO history stepper at the end)
        # (to run php script: https://stackoverflow.com/a/8984318) Check=True
        # TODO: 4) save current in history table (with proper tf index)
        pass

    db.disconnect(conn)
