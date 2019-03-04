--
-- Name: srs_current_to_history(integer); Type: FUNCTION; Schema: public; Owner: crowd4roads_sw
--

CREATE OR REPLACE FUNCTION srs_current_to_history(integer, integer) RETURNS void
    LANGUAGE plpgsql STRICT
    AS $_$
DECLARE
  how_many ALIAS FOR $1;
  new_time_frame ALIAS FOR $2;
BEGIN
  insert into history (ppe, osm_id, quality, the_geom, highway, created_at, time_frame, count, stddev, last_count) (select ppe, osm_id, quality, the_geom, highway,  updated_at as created_at, new_time_frame, count, stddev, last_count from current limit how_many);
END;
$_$;


ALTER FUNCTION public.srs_current_to_history(integer, integer) OWNER TO crowd4roads_sw;

--
-- Name: FUNCTION srs_current_to_history(integer, integer); Type: COMMENT; Schema: public; Owner: crowd4roads_sw
--

COMMENT ON FUNCTION srs_current_to_history(integer, integer) IS 'values from "current" table and store them in the "history" table, assigning a new time_frame value.
USAGE: SELECT srs_current_to_history(999999999, 10);
This is the OFFLINE version of the actual function';