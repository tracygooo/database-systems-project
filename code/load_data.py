# from csv import reader
import psycopg2
import psycopg2.extras
import os
from datetime import datetime

# --- Connect database 
connect_string = "host='localhost' dbname='dbms_final_project' user='dbms_project_user' password='dbms_password'"
conn = psycopg2.connect( connect_string )
cursor = conn.cursor()

# --- Create schema
schema_fname = 'schema.sql'
create_schema = open( schema_fname , 'r' ).read()
cursor.execute( create_schema )
conn.commit()

# --- Load data into tables 
dataset_path = 'datasets/'
dataset_fname = [ 'covid19.csv' , 'weather.csv' , 'crash.csv' ]
table_name = [ 'covid19' , 'weather' , 'crash' ]
for i in range( len(dataset_fname) ) :
    print( "\nTable '{}' start loading: {}".format( table_name[i] , datetime.now() ) )
    f_dataset = open( dataset_path + dataset_fname[i] , "r")
    cursor.copy_expert( "copy {} from STDIN CSV HEADER QUOTE '\"'".format( table_name[i] ), f_dataset )
    conn.commit()
    print( "\nTable '{}' completing loading: {}".format( table_name[i] , datetime.now() ) )
