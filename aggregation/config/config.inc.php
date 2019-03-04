<?php

// return the env variable or the default value
function _getenv($env, $default) {
  $value = getenv($env);
  return ($value? $value : $default);
}

// raw database
DEFINE("RAW_DB_HOST", _getenv("RAW_DB_HOST", "raw-db"));
DEFINE("RAW_DB_PORT", _getenv("RAW_DB_PORT", "5432"));
DEFINE("RAW_DB_NAME", _getenv("RAW_DB_NAME", "srs_raw_db"));
DEFINE("RAW_DB_USER", _getenv("RAW_DB_USER", "crowd4roads_sw"));
DEFINE("RAW_DB_PASS", _getenv("RAW_DB_PASS", "password"));

// aggregate database
DEFINE("AGG_DB_HOST", _getenv("AGG_DB_HOST", "agg-db"));
DEFINE("AGG_DB_PORT", _getenv("AGG_DB_PORT", "5432"));
DEFINE("AGG_DB_NAME", _getenv("AGG_DB_NAME", "srs_agg_db"));
DEFINE("AGG_DB_USER", _getenv("AGG_DB_USER", "crowd4roads_sw"));
DEFINE("AGG_DB_PASS", _getenv("AGG_DB_PASS", "password"));

// general options
DEFINE("NEW_LINE", "\n");
DEFINE("SRS_UPDATE_DATA_PROJECTIONS_SIZE", 30000);
DEFINE("ROAD_ROUGHNESS_METERS", 20);
//DEFINE("ROAD_ROUGHNESS_RANGE", 40);
DEFINE("ROAD_ROUGHNESS_RANGE", 20);

// quality index
DEFINE("QUALITY_INDEX_MINIMUM_DATA", 3);
DEFINE("QUALITY_Z_VALUE", 1.645);

date_default_timezone_set("Europe/Rome");
