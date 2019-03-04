
CREATE OR REPLACE FUNCTION public.srs_avg_roughness(
    the_geom geometry,
    meters integer,
    osm_id bigint,
    min_resolution integer,
    days integer)
  RETURNS SETOF record AS
$BODY$
DECLARE
  r record;
  meters_radians double precision;
BEGIN
  meters_radians = $2 / 111000.0;
  FOR r IN
  SELECT
    AVG(ppe) AS avg_roughness,
    $1 AS avg_point,
    MAX(date) as max_date,
    COUNT(*) as count,
    STDDEV(ppe) as stddev_ppe,
    AVG(occupancy)
  FROM (
         SELECT
           ppe,
           vals.date,
           cast(nullif(metadata::json->>'numberOfPeople', '1') AS float) as occupancy
         FROM
           single_data AS vals left join track  as t on t.track_id = vals.track_id
         WHERE
           ST_Distance_Sphere($1, vals.position) < $2
           AND vals.osm_line_id = $3
           AND vals.evaluate = 1
           AND position_resolution < $4
           AND vals.date > NOW() - ($5 || 'days')::INTERVAL
       ) AS foo
  LOOP
    RETURN NEXT r;
  END LOOP;
  RETURN;
END;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100
  ROWS 1000;
ALTER FUNCTION public.srs_avg_roughness(geometry, integer, bigint, integer, integer)
  OWNER TO crowd4roads_sw;


-- Function: public.srs_road_roughness_values(integer, integer, integer, integer, integer)

-- DROP FUNCTION public.srs_road_roughness_values(integer, integer, integer, integer, integer);

CREATE OR REPLACE FUNCTION public.srs_road_roughness_values(
    geom_id integer,
    meters integer,
    range integer,
    min_resolution integer,
    days integer)
  RETURNS SETOF record AS
$BODY$
DECLARE
  i float;
  step float;
  curr_road geometry;
BEGIN
  SELECT srs_meters_to_line_fraction(geom_id, meters) INTO step;
  SELECT way FROM planet_osm_line WHERE osm_id = geom_id LIMIT 1 INTO curr_road;
  i:= 0;
  WHILE (i <= 1)
  LOOP
    -- Get avg here --
    RETURN QUERY SELECT result.avg_roughness, result.avg_point, result.max_date, result.count, result.stddev_ppe, result.occupancy FROM srs_avg_roughness(ST_Line_Interpolate_Point(curr_road, i), range, geom_id, min_resolution, days) AS result(avg_roughness float, avg_point geometry, max_date timestamp, count bigint, stddev_ppe float, occupancy float);
    i := i + step;
  END loop;
  RETURN;
END;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100
  ROWS 1000;
ALTER FUNCTION public.srs_road_roughness_values(integer, integer, integer, integer, integer)
  OWNER TO crowd4roads_sw;
