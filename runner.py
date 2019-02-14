#!/usr/bin/python
import databaseutils as db
import timeframe
import multiprocesslibrary as mpl

if __name__ == '__main__':
    conn = db.connect(db='raw')
    conn_agg = db.connect(db='agg')

    date_range = db.get_date_range(conn)
    frames = timeframe.get_time_frames(*date_range)

    # TODO: clean out tables: current, history

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
        # TODO: 3.2) splits list in [NUM CORES] entries
        mpl.launch('php script', osm_ids)
        # TODO  3.3) launch [NUM CORES] modified PHP script
        #            changes:
        #               - SRS_Road_Roughness_Values days limit to something like 10000
        # TODO: 4) save current in history table (with proper tf index)
        db.save_current_to_history(conn_agg, tf_index)
        pass

    db.disconnect(conn)
    db.disconnect(conn_agg)
