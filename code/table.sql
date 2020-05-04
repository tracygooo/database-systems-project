--crash
DROP TABLE IF EXISTS injury;
DROP TABLE IF EXISTS factor;
DROP TABLE IF EXISTS vehicle;
DROP TABLE IF EXISTS occurence;
CREATE TABLE occurence (
	COLLISION_ID VARCHAR(7) PRIMARY KEY,
	crashdate DATE,
	location VARCHAR(20)
	);
INSERT INTO occurence (
	COLLISION_ID,
	crashdate,
	location)
SELECT COLLISION_ID, 
		CRASH_DATE,
		BOROUGH
FROM crash;

CREATE TABLE injury (
	COLLISION_ID VARCHAR(7) REFERENCES occurence,
	number_of_injury INTEGER,
	number_of_killed INTEGER,
	PRIMARY KEY (COLLISION_ID)
	);
INSERT INTO injury (
	COLLISION_ID,
	number_of_injury,
	number_of_killed)
SELECT COLLISION_ID, 
		NUMBER_OF_PERSONS_INJURED+UMBER_OF_PEDESTRIANS_INJURED+NUMBER_OF_CYCLIST_INJURED+UMBER_OF_MOTORIST_INJURED,
		NUMBER_OF_PERSONS_KILLED+NUMBER_OF_PEDESTRIANS_KILLED+NUMBER_OF_CYCLIST_KILLED+NUMBER_OF_MOTORIST_KILLED
FROM crash;

CREATE TABLE factor (
	COLLISION_ID VARCHAR(7) REFERENCES occurence,
	factor1 VARCHAR(63),
	factor2 VARCHAR(63),
	factor3 VARCHAR(63),
	factor4 VARCHAR(63),
	factor5 VARCHAR(63),
	PRIMARY KEY(COLLISION_ID)
	);
INSERT INTO factor(
	COLLISION_ID,
	factor1,
	factor2,
	factor3,
	factor4,
	factor5)
SELECT COLLISION_ID,
		CONTRIBUTING_FACTOR_VEHICLE_1,
		CONTRIBUTING_FACTOR_VEHICLE_2,
		CONTRIBUTING_FACTOR_VEHICLE_3,
		CONTRIBUTING_FACTOR_VEHICLE_4,
		CONTRIBUTING_FACTOR_VEHICLE_5
FROM crash;

CREATE TABLE vehicle (
	COLLISION_ID VARCHAR(7) REFERENCES occurence,
	vehicle1 VARCHAR(63),
	vehicle2 VARCHAR(63),
	vehicle3 VARCHAR(63),
	vehicle4 VARCHAR(63),
	vehicle5 VARCHAR(63),
	PRIMARY KEY(COLLISION_ID)
	);
INSERT INTO vehicle(
	COLLISION_ID,
	vehicle1,
	vehicle2,
	vehicle3,
	vehicle4,
	vehicle5)
SELECT COLLISION_ID,
		VEHICLE_TYPE_CODE_1,
		VEHICLE_TYPE_CODE_2,
		VEHICLE_TYPE_CODE_3,
		VEHICLE_TYPE_CODE_4,
		VEHICLE_TYPE_CODE_5
FROM crash;



--weather
DROP TABLE IF EXISTS precipitation;
DROP TABLE IF EXISTS weatherType ;
DROP TABLE IF EXISTS wind;
DROP TABLE IF EXISTS temperature ;
CREATE TABLE temperature (
    measure_date DATE PRIMARY KEY,
    tmin INTEGER ,
    tmax INTEGER
);
INSERT INTO temperature( measure_date, tmin, tmax)
    SELECT measure_date,
           tmin,
           tmax
    FROM weather
    WHERE station = 'USW00094728';

CREATE TABLE precipitation (
    measure_date DATE REFERENCES temperature,
    precipitation NUMERIC(6,1) ,
    PRIMARY KEY (measure_date)
);
INSERT INTO precipitation( measure_date, precipitation)
SELECT measure_date,
		precipitation
FROM weather
WHERE station = 'USW00094728';

CREATE TABLE weatherType (
    measure_date DATE REFERENCES temperature,
    is_foggy BOOLEAN , 
    is_foggy_heavy BOOLEAN ,
    is_thunder BOOLEAN ,
    is_ice_pellets BOOLEAN ,
    is_glaze_rime BOOLEAN ,
    is_smoke_haze BOOLEAN , 
    is_damaging_wind BOOLEAN ,
    is_mist BOOLEAN , 
    is_drizzle BOOLEAN , 
    is_rainy BOOLEAN , 
    is_snowy BOOLEAN , 
    is_unknown_precipitation BOOLEAN ,  
    is_freezing_foggy BOOLEAN 
) ;

INSERT INTO weatherType( measure_date, is_foggy , is_foggy_heavy , 
                         is_thunder , is_ice_pellets , is_glaze_rime , 
                         is_smoke_haze , is_damaging_wind , is_mist , 
                         is_drizzle , is_rainy , is_snowy , 
                         is_unknown_precipitation , is_freezing_foggy )
    SELECT measure_date , is_foggy , is_foggy_heavy , is_thunder ,
           is_ice_pellets , is_glaze_rime , is_smoke_haze , 
           is_damaging_wind , is_mist , is_drizzle , 
           is_rainy , is_snowy , is_unknown_precipitation , is_freezing_foggy 
    FROM weather
    WHERE station = 'USW00094728';

CREATE TABLE wind(
    measure_date DATE REFERENCES temperature,
    ave_wind_speed NUMERIC( 6 , 1), -- AWND
    wind_direction_2min SMALLINT,--  WDF2 
    wind_direction_5min SMALLINT,--  WDF5
    wind_speed_2min NUMERIC(6,1),--  WSF2 
    wind_speed_5min NUMERIC(6,1) --  WSF5
);

INSERT INTO wind( 
                  measure_date,
                  ave_wind_speed , 
                  wind_direction_2min ,
                  wind_direction_5min ,
                  wind_speed_2min ,
                  wind_speed_5min
				)
    SELECT measure_date, ave_wind_speed , 
           wind_direction_2min , wind_direction_5min ,
           wind_speed_2min , wind_speed_5min
FROM weather
WHERE station = 'USW00094728';

--covid19
DROP TABLE IF EXISTS covid19;
CREATE TABLE covid19(
	TestDate DATE,
	county VARCHAR(20) ,
	NewPositives INTEGER,
	TotalNumberOfTestsPerformed INTEGER,
	PRIMARY KEY (TestDate,county)
);
INSERT INTO covid19(
	TestDate,
	county,
	NewPositives,
	TotalNumberOfTestsPerformed)
SELECT TestDate,
		county,
		NewPositives,
		TotalNumberOfTestsPerformed
FROM covid;

--drop temporary tables
-- DROP TABLE covid;
-- DROP TABLE crash;
-- DROP TABLE weather;
