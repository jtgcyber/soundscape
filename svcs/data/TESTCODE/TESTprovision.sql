CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE osm_roads (
    osm_id BIGINT PRIMARY KEY,
    name TEXT,
    type TEXT,
    geometry GEOMETRY(LineString, 4326) -- assuming roads are represented as line strings
);

CREATE TABLE osm_places (
    osm_id BIGINT PRIMARY KEY,
    name TEXT,
    type TEXT,
    geometry GEOMETRY(Point, 4326) -- assuming places are represented as points
);

CREATE TABLE osm_entrances (
    osm_id BIGINT PRIMARY KEY,
    name TEXT,
    type TEXT,
    geometry GEOMETRY(Point, 4326) -- assuming entrances are represented as points
);
