# from csv import reader
import psycopg2
import psycopg2.extras
import os
from datetime import datetime

# --- Create schema
print( 'Creating temporary tables for datasets loading' )
schema_fname = 'schema.sql'
connect_string = "host='localhost' dbname='dbms_final_project' user='dbms_project_user' password='dbms_password'"
conn = psycopg2.connect( connect_string )
cursor = conn.cursor()
create_schema = open( schema_fname , 'r' ).read()
cursor.execute( create_schema )
conn.commit()
print( '-'*65 )

# --- Load data into temporary tables 
print( 'Loading datasets into temperary tables' )
dataset_path = 'datasets/'
dataset_fname = [ 'covid19.csv' , 'weather.csv' , 'crash.csv' ]
table_name = [ 'covid' , 'weather' , 'crash' ]
for i in range( len(dataset_fname) ) :
    print( "Temporary Table '{}' start loading: {}".format( table_name[i] , datetime.now() ) )
    f_dataset = open( dataset_path + dataset_fname[i] , "r")
    cursor.copy_expert( "copy {} from STDIN CSV HEADER QUOTE '\"'".format( table_name[i] ), f_dataset )
    conn.commit()
    print( "Temporary Table '{}' complete loading: {}".format( table_name[i] , datetime.now() ) )
print( '-'*65 )

# --- Insert data into splitted tables from temporary table 
print( 'Creating splitted tables for research' )
print( "Tables start creating: {}".format( datetime.now()))
schema_fname = 'table.sql'
create_schema = open( schema_fname , 'r' ).read()
cursor.execute(create_schema)
conn.commit()
print( "Tables complete creating: {}".format( datetime.now()))
print( '-'*65 )
