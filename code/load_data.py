# from csv import reader
import psycopg2
import psycopg2.extras
import os
from datetime import datetime

schema_fname = 'schema.sql'
connect_string = "host='localhost' dbname='dbms_final_project' user='dbms_project_user' password='dbms_password'"
conn = psycopg2.connect( connect_string )
cursor = conn.cursor()
create_schema = open( schema_fname , 'r' ).read()
cursor.execute( create_schema )
conn.commit()

dataset_fname= 'datasets/covid19.csv'
table_name = 'covid19'
f_dataset = open( dataset_fname , "r")
cursor.copy_expert( "copy {} from STDIN CSV HEADER QUOTE '\"'".format( table_name ), f_dataset )
conn.commit()

dataset_fname= 'datasets/weather.csv'
table_name = 'weather_tmp'
f_dataset = open( dataset_fname , "r")
print( "\n'{}' loading table: {}".format( table_name , datetime.now() ) )
cursor.copy_expert( "copy {} from STDIN CSV HEADER QUOTE '\"'".format( table_name ), f_dataset )
conn.commit()
print( "\n'{}' completing loading table: {}".format( table_name , datetime.now() ) )
