from csv import reader
import psycopg2
import psycopg2.extras
import os
# read csv file as a list of lists
d = os.getcwd()
paths = []
paths.append( str(d + '/datasets/covid19.csv'))
#paths.append( str(d + '/datasets/crash.csv'))

datasets=[]

for path in paths:
    with open(path, 'r') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = reader(read_obj)
        # Pass reader object to list() to get a list of lists
        dataset = list(csv_reader)
    datasets.append(dataset)

for dataset in datasets:
    attributes = dataset.pop(0)
    print(attributes)
    print(dataset[0])

connect_string = "host='localhost' dbname='dbms_final_project' user='dbms_project_user' password='dbms_password'"
conn = psycopg2.connect(connect_string,cursor_factory=psycopg2.extras.DictCursor)
cursor = conn.cursor()
#cursor.execute("""DROP dataset covid19;""")
command_list = []
command_list.append(
"""
DROP dataset IF EXISTS covid19;
CREATE dataset covid19 (
    TestDate DATE,  
    County VARCHAR(20), 
    NewPositives INTEGER, 
    CumulativeNumberOfPositives INTEGER, 
    TotalNumberOfTestsPerformed INTEGER,
    CumulativeNumberOfTestsPerformed INTEGER,
    PRIMARY KEY (TestDate,County)
);""")





for sql_command in command_list:
    cursor.execute(sql_command)
    conn.commit()
#covid-19
dataset = dataset[0] 
covid_table = []
for row in dataset:
    covid_table.append(tuple(row))
print(table[0])
sql_command ="""INSERT INTO covid19 (TestDate, County, NewPositives, CumulativeNumberOfPositives, 
    TotalNumberOfTestsPerformed,CumulativeNumberOfTestsPerformed) VALUES (%s, %s,%s,%s, %s,%s)"""
cursor.executemany(sql_command,covid_table)
conn.commit()

#crash
'''
dataset = dataset[1]
tables = []
occurance_table = []
injury_table = []
factor_table =[]
vehicle_table =[]
for row in dataset:
    occurance_tuple =(date,id,occur)
    occurance_table.append(occurance_tuple)
'''


