#!/usr/bin/python
import databaseutils as db
import timeframe
import multiprocesslibrary as mpl
import logging, sys

# PHP_INTERPRETER = 'php'
PHP_INTERPRETER = 'C:/xampp/php/php.exe'
AGGREGATION_SCRIPT = 'aggregation/aggregate.php'
#AGGREGATION_SCRIPT = 'aggregation/test.php'

# set logging level
#logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

if __name__ == '__main__':
    conn = db.connect(db='raw')
    conn_agg = db.connect(db='agg')

    date_range = db.get_date_range(conn)
    frames = timeframe.get_time_frames(*date_range)

    logging.info("{0} cores detected".format(mpl.get_core_count()))

    # clean out tables: current, history
    db.empty_out_current(conn_agg)
    db.empty_out_history(conn_agg)

    for tf_index, f in enumerate(frames):

        logging.info("time_frame: {0} - from {1} to {2}".format(tf_index, *f))
        # clean out single_data table
        db.empty_out_single_data(conn)
        # populate single_data table
        db.move_data_within_time_frame(conn, f)
        record_count = db.get_single_data_count(conn)
        logging.info("{0} raw records".format(record_count))

        # check for different osm_line_id in SINGLE_DATA_TABLE
        osm_ids = db.get_osm_ids(conn)
        logging.debug("Aggregating OSM ids: {0}".format(osm_ids))

        if len(osm_ids) > 0:
            logging.debug("Aggregation over frame {0}".format(f))
            procs = mpl.launch(PHP_INTERPRETER, AGGREGATION_SCRIPT, osm_ids)

            # launch [NUM CORES] modified PHP script
            # NOTE: SRS_Road_Roughness_Values days limit to something like 10000

            if len(procs) > 0:
                mpl.merge(procs)
        else:
            logging.debug("Skipping frame {0}".format(f))

        agg_record_count = db.get_current_count(conn_agg)
        logging.info("{0} agg records".format(agg_record_count))
        # save current in history table (with proper tf index)
        db.save_current_to_history(conn_agg, tf_index)

    db.disconnect(conn)
    db.disconnect(conn_agg)

    logging.info("All done")
