#!/usr/bin/python
import databaseutils as db
import timeframe
import multiprocesslibrary as mpl

PHP_INTERPRETER = 'php'
AGGREGATION_SCRIPT = 'test.php'


if __name__ == '__main__':
    conn = db.connect(db='raw')
    conn_agg = db.connect(db='agg')

    date_range = db.get_date_range(conn)
    frames = timeframe.get_time_frames(*date_range)

    # TOCHECK: clean out tables: current, history, archive
    db.empty_out_archive(conn)
    db.empty_out_current(conn_agg)
    db.empty_out_history(conn_agg)

    for tf_index, f in enumerate(frames):

        print(tf_index, f)
        # TOCHECK: 1) clean out single_data table
        db.empty_out_single_data(conn)
        # TOCHECK: 2) populate single_data table
        db.move_data_within_time_frame(conn, f)
        # TODO: 3) apply special (no filtering on old data points) aggregation
        # on single_data table (note: NO history stepper at the end)
        # (to run php script: https://stackoverflow.com/a/16071877) Check=True
        # TOCHECK: 3.1) check for different osm_line_id in SINGLE_DATA_TABLE
        osm_ids = db.get_osm_ids(conn)
        mpl.launch(PHP_INTERPRETER, AGGREGATION_SCRIPT, osm_ids)

        # TOCHECK  3.3) launch [NUM CORES] modified PHP script
        #            changes:
        #               - TODO SRS_Road_Roughness_Values days limit to something like 10000
        # TOCHECK: 4) save current in history table (with proper tf index)
        db.save_current_to_history(conn_agg, tf_index)
        pass

    db.disconnect(conn)
    db.disconnect(conn_agg)
