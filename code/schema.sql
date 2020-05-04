DROP TABLE IF EXISTS covid19 ;
CREATE TABLE covid19 (
    TestDate DATE, 
    County VARCHAR(20), 
    NewPositives INTEGER, 
    CumulativeNumberOfPositives INTEGER, 
    TotalNumberOfTestsPerformed INTEGER,
    CumulativeNumberOfTestsPerformed INTEGER
);

DROP TABLE IF EXISTS weather_tmp ;
CREATE TABLE weather_tmp (
    station VARCHAR( 15 ) ,
    measure_date DATE ,
    ave_wind_speed NUMERIC( 6 , 1), -- AWND
    days_in_multiday INT, -- DAPR - Number of days included in the multiday precipitation total (MDPR)
    precipitation_tot NUMERIC( 6 , 1), --MDPR - Multiday precipitation total (use with DAPR and DWPR, if available)
    peak_gust_time TIME, -- PGTM
    precipitation NUMERIC( 6 , 1), --PRCP
    snowfall NUMERIC(6,1), -- SNOW 
    snow_depth NUMERIC(6,1), -- SNWD
    tmax NUMERIC(4,1),-- TMAX
    tmin NUMERIC(4,1), -- TMIN
    sunshine_tot NUMERIC(4,1), -- TSUN 
    wind_direction_2min SMALLINT,--  WDF2 
    wind_direction_5min SMALLINT,--  WDF5
    wind_speed_2min NUMERIC(6,1),--  WSF2 
    wind_speed_5min NUMERIC(6,1),--  WSF5
    is_foggy BOOLEAN , --WT01 - Fog, ice fog, or freezing fog (may include heavy fog)
    is_foggy_heavy BOOLEAN ,-- WT02 - Heavy fog or heaving freezing fog (not always distinguished from fog)
    is_thunder BOOLEAN , -- WT03
    is_ice_pellets BOOLEAN ,--  WT04 - Ice pellets, sleet, snow pellets, or small hail
    is_glaze_rime BOOLEAN ,-- WT06 - Glaze or rime
    is_smoke_haze BOOLEAN , -- WT08 - Smoke or haze 
    is_damaging_wind BOOLEAN ,-- WT11 - High or damaging winds
    is_mist BOOLEAN , -- WT13 - Mist
    is_drizzle BOOLEAN , -- WT14 - Drizzle
    is_rainy BOOLEAN , -- WT16 - Rain (may include freezing rain, drizzle, and
    is_snowy BOOLEAN , -- WT18 - Snow, snow pellets, snow grains, or ice crystals
    is_unknown_precipitation BOOLEAN ,  -- WT19 - Unknown source of precipitation
    is_freezing_foggy BOOLEAN -- WT22 - Ice fog or freezing fog
) ;

DROP TABLE IF EXISTS temperature ;
CREATE TABLE temperature (
    measure_date DATE,
    tmin INTEGER ,
    tmax INTEGER
);

