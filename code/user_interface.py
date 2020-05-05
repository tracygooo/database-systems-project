import psycopg2
import psycopg2.extras
import os

from tkinter import *
from datetime import datetime
from functools import partial

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

def submitCovidByDateCounty( test_date , county , frame , myrow ):
    print(test_date )
    print(county)
    connect_string = "host='localhost' dbname='dbms_final_project' user='dbms_project_user' password='dbms_password'"
    conn = psycopg2.connect( connect_string )
    cursor = conn.cursor()
    query = "SELECT * FROM covid19 WHERE testdate = %s and county ILIKE %s"
    cursor.execute( query , ( test_date.get() , county.get() ) )
    records = cursor.fetchall()[0]
    records_label = Label( frame , text = records )
    records_label.grid( row = myrow + 1 , column = 1 , columnspan = 2 )
    conn.commit()

    print_records = "Date \t County \t New Positive \t Total tested\n"
    #for record in records :
    #    print_records = print_records + str( record ) + '\n'
    # records_label.pack()
    print(records)

def submitCovidRankCases( start_date , end_date , limit , frame , myrow ):
    connect_string = "host='localhost' dbname='dbms_final_project' user='dbms_project_user' password='dbms_password'"
    conn = psycopg2.connect( connect_string )
    cursor = conn.cursor()
    query = "SELECT county, SUM(newpositives) "\
            + "FROM covid19 WHERE testdate > %s AND testdate < %s "\
            + "GROUP BY county " + \
            "ORDER BY sum(newpositives) DESC LIMIT %s ;"
    cursor.execute( query , ( start_date.get() , end_date.get() , limit.get() ) )
    conn.commit()
    records = cursor.fetchall()
    print_records = ''
    for record in records :
        print_records = print_records + str( record ) + '\n'
    records_label = Label( frame , text = print_records )
    records_label.grid( row = myrow + 1 , column = 1 , columnspan = 2 )
    print(print_records)

def submitCovidPosRatio( start_date , end_date , county , frame , myrow ):
    connect_string = "host='localhost' dbname='dbms_final_project' user='dbms_project_user' password='dbms_password'"
    conn = psycopg2.connect( connect_string )
    cursor = conn.cursor()
    query = '''
    SELECT cast(sum(newpositives)::NUMERIC/sum(totalnumberoftestsperformed) as decimal(10,2))
    FROM covid19
    WHERE TestDATE > %s 
    AND TestDATE < %s
    AND County ilike %s;       
    '''
    cursor.execute( query , ( start_date.get() , end_date.get() , county.get() ) )
    conn.commit()
    records = cursor.fetchall()[0]
    records_label = Label( frame , text = records )
    records_label.grid( row = myrow + 1 , column = 1 , columnspan = 2 )

def submitCrashFactor( limit , frame , myrow ):
    connect_string = "host='localhost' dbname='dbms_final_project' user='dbms_project_user' password='dbms_password'"
    conn = psycopg2.connect( connect_string )
    cursor = conn.cursor()

    query = '''SELECT factor1,num1+num2+num3+num4+num5 num
    FROM
    (SELECT DISTINCT factor1,count(factor1) num1
    FROM factor
    GROUP BY factor1 
    ) a,
    (SELECT DISTINCT factor2,count(factor2) num2
    FROM factor
    GROUP BY factor2) b,
    (SELECT DISTINCT factor3,count(factor3) num3
    FROM factor
    GROUP BY factor3) c,
    (SELECT DISTINCT factor4,count(factor4) num4
    FROM factor
    GROUP BY factor4) d,
    (SELECT DISTINCT factor5,count(factor5) num5
    FROM factor
    GROUP BY factor5) e
    WHERE factor1 = factor2
    AND factor2 = factor3
    AND factor3 = factor4
    AND factor4 = factor5
    ORDER BY num DESC LIMIT %s;'''

    cursor.execute( query , ( limit.get(), ) )
    conn.commit()
    records = cursor.fetchall()

    print_records = 'Factors \t # of crashes\n'
    for record in records :
        print_records = print_records + str( record ) + '\n'
    print(print_records)

    records_label = Label( frame , text = print_records )
    records_label.grid( row = myrow + 1 , column = 1 , columnspan = 2 )

def submitCrashWeather( weather_type , frame , myrow ):
    connect_string = "host='localhost' dbname='dbms_final_project' user='dbms_project_user' password='dbms_password'"
    conn = psycopg2.connect( connect_string )
    cursor = conn.cursor()

    weather = weather_type.get()
    l =['is_foggy','is_foggy_heavy','is_thunder','is_ice_pellets','is_glaze_rime','is_smoke_haze', 'is_damaging_wind','is_mist', 'is_drizzle', 'is_rainy', 'is_snowy', 'is_unknown_precipitation',  'is_freezing_foggy']

    for e in l:
        if weather in e:
            weather = e

    query = '''SELECT num1/num2 ratio
                FROM(
                SELECT count(measure_date) num1
                FROM weatherType, occurence
                WHERE crashdate = measure_date
                AND %s = TRUE) a,
                (SELECT count(measure_date) num2
                FROM weatherType
                WHERE %s = TRUE) b''' % ( weather, weather ) 

    cursor.execute( query )
    conn.commit()
    records = cursor.fetchall()[0]
    records_label = Label( frame , text = records )
    records_label.grid( row = myrow + 1 , column = 1 , columnspan = 2 )

def submitCrashPrecipitation( low , high , frame , myrow ):
    connect_string = "host='localhost' dbname='dbms_final_project' user='dbms_project_user' password='dbms_password'"
    conn = psycopg2.connect( connect_string )
    cursor = conn.cursor()

    query = '''
            SELECT count(COLLISION_ID)/tyw as ratio
            FROM occurence, precipitation,(
            SELECT count(measure_date) tyw
            FROM precipitation
            WHERE precipitation >%s
            AND precipitation < %s) wyt
            WHERE precipitation > %s
            AND precipitation < %s
            AND crashdate = measure_date
            GROUP BY tyw;
            '''

    cursor.execute( query , ( low.get(), high.get() , low.get() , high.get() ) )
    conn.commit()
    records = cursor.fetchall()[0]
    records_label = Label( frame , text = records )
    records_label.grid( row = myrow + 1 , column = 1 , columnspan = 2 )


def getChildren (window) :
    child_list = window.winfo_children()
    for item in child_list :
        if item.winfo_children() :
            child_list.extend(item.winfo_children())
    return child_list

def clearChildren( window ) :
    widget_list = getChildren(window)
    for item in widget_list:
        item.grid_forget()

def queryCovidByDateCounty( frame ) :
    clearChildren( frame )

    # Create text labels and entry boxes
    myrow = 0
    date_label = Label( frame , text = "Date" )
    date_label.grid( row = myrow , column = 0 )
    date_entry = Entry( frame , width = 30 )
    date_entry.grid( row = myrow , column = 1  )
    myrow += 1

    county_label = Label( frame , text = "County" )
    county_label.grid( row = myrow , column = 0 )
    county_entry = Entry( frame , width = 30 )
    county_entry.grid( row = myrow , column = 1 )
    myrow += 1

    # Create submit button
    my_submit = Button( frame , text = "Submit" , command = partial( submitCovidByDateCounty , date_entry , county_entry , frame , myrow ) )
    my_submit.grid( row = myrow , column = 1 , columnspan = 2 , pady = 10 , padx = 10, ipadx = 100 )

def queryCovidRankCases( frame ) :
    clearChildren( frame )
    myrow = 0
    date_start_label = Label( frame , text = "Start date" )
    date_start_label.grid( row = myrow , column = 0 )
    date_start_entry = Entry( frame , width = 30 )
    date_start_entry.grid( row = myrow , column = 1  )
    myrow += 1

    date_end_label = Label( frame , text = "End date" )
    date_end_label.grid( row = myrow , column = 0 )
    date_end_entry = Entry( frame , width = 30 )
    date_end_entry.grid( row = myrow , column = 1  )
    myrow += 1

    limit_label = Label( frame , text = "First n counties" )
    limit_label.grid( row = myrow , column = 0 )
    limit_entry = Entry( frame , width = 30 )
    limit_entry.grid( row = myrow , column = 1 )
    myrow += 1

    # Create submit button
    my_submit = Button( frame , text = "Submit" , command = partial( submitCovidRankCases , date_start_entry , date_end_entry , limit_entry , frame , myrow ) )
    my_submit.grid( row = myrow , column = 1 , columnspan = 2 , pady = 10 , padx = 10, ipadx = 100 )


def queryCovidPosRatio( frame ) :
    clearChildren( frame )
    myrow = 0
    date_start_label = Label( frame , text = "Start date" )
    date_start_label.grid( row = myrow , column = 0 )
    date_start_entry = Entry( frame , width = 30 )
    date_start_entry.grid( row = myrow , column = 1  )
    myrow += 1

    date_end_label = Label( frame , text = "End date" )
    date_end_label.grid( row = myrow , column = 0 )
    date_end_entry = Entry( frame , width = 30 )
    date_end_entry.grid( row = myrow , column = 1  )
    myrow += 1

    limit_label = Label( frame , text = "County" )
    limit_label.grid( row = myrow , column = 0 )
    limit_entry = Entry( frame , width = 30 )
    limit_entry.grid( row = myrow , column = 1 )
    myrow += 1

    # Create submit button
    my_submit = Button( frame , text = "Submit" , command = partial( submitCovidPosRatio , date_start_entry , date_end_entry , limit_entry , frame , myrow ) )
    my_submit.grid( row = myrow , column = 1 , columnspan = 2 , pady = 10 , padx = 10, ipadx = 100 )

def queryCrashFactor( frame ) :
    clearChildren( frame )
    myrow = 0
    limit_label = Label( frame , text = "Top n factors" )
    limit_label.grid( row = myrow , column = 0 )
    limit_entry = Entry( frame , width = 30 )
    limit_entry.grid( row = myrow , column = 1  )
    myrow += 1

    # Create submit button
    my_submit = Button( frame , text = "Submit" , command = partial( submitCrashFactor , limit_entry , frame , myrow ) )
    my_submit.grid( row = myrow , column = 1 , columnspan = 2 , pady = 10 , padx = 10, ipadx = 100 )

def queryCrashRegion( frame ):
    connect_string = "host='localhost' dbname='dbms_final_project' user='dbms_project_user' password='dbms_password'"
    conn = psycopg2.connect( connect_string )
    cursor = conn.cursor()
    query = '''
            SELECT region , count(region) FROM occurence
            WHERE region NOT LIKE '' 
            GROUP BY region
            HAVING count(region) > 0
            ORDER BY count(region) DESC
            '''
    cursor.execute( query )
    conn.commit()
    records = cursor.fetchall()
    print_records = ''
    for record in records :
        print_records = print_records + str( record ) + '\n'
    records_label = Label( frame , text = print_records )
    records_label.grid( row = 0 , column = 0 , columnspan = 1 )
    print(print_records)

def queryCrashWeather( frame ) :
    clearChildren( frame )
    myrow = 0
    type_label = Label( frame , text = "Weather type" )
    type_label.grid( row = myrow , column = 0 )
    type_entry = Entry( frame , width = 30 )
    type_entry.grid( row = myrow , column = 1  )
    myrow += 1

    # Create submit button
    my_submit = Button( frame , text = "Submit" , command = partial( submitCrashWeather , type_entry , frame , myrow ) )
    my_submit.grid( row = myrow , column = 1 , columnspan = 2 , pady = 10 , padx = 10, ipadx = 100 )

def queryCrashPrecipitation( frame ) :
    clearChildren( frame )
    myrow = 0
    low_label = Label( frame , text = "Precipitation lower limit" )
    low_label.grid( row = myrow , column = 0 )
    low_entry = Entry( frame , width = 30 )
    low_entry.grid( row = myrow , column = 1  )
    myrow += 1

    up_label = Label( frame , text = "Precipitation upper limit" )
    up_label.grid( row = myrow , column = 0 )
    up_entry = Entry( frame , width = 30 )
    up_entry.grid( row = myrow , column = 1  )
    myrow += 1

    # Create submit button
    my_submit = Button( frame , text = "Submit" , command = partial( submitCrashPrecipitation , low_entry , up_entry , frame , myrow ) )
    my_submit.grid( row = myrow , column = 1 , columnspan = 2 , pady = 10 , padx = 10, ipadx = 100 )

# --- Setup window 
root = Tk()
app = Window(root)
root.wm_title( "Database Systems Final Project" )
root.geometry( "600x400" )

leftframe = Frame(root)
leftframe.pack( side = LEFT )

rightframe = Frame( root )
rightframe.pack( side = RIGHT )

# --- Parameters for buttons linked to queries 
mypadx , mypady = 5 , 5 
mysticky = "E"
myrow = 0

# ---  Covid buttons
covid_button1 = Button( leftframe , text = "Covid19-1" , command = partial( queryCovidByDateCounty , rightframe ) )
covid_button1.grid( row = myrow , column = 0 , sticky = mysticky , padx = mypadx , pady = mypady )
myrow += 1

covid_button2 = Button( leftframe , text = "Covid19-2" , command = partial( queryCovidRankCases , rightframe ) )
covid_button2.grid( row = myrow , column = 0 , sticky = mysticky , padx = mypadx , pady = mypady )
myrow += 1

covid_button3 = Button( leftframe , text = "Covid19-3" , command = partial( queryCovidPosRatio , rightframe ) )
covid_button3.grid( row = myrow , column = 0 , sticky = mysticky , padx = mypadx , pady = mypady )
myrow += 1

# ---  Crash buttons
crash_button1 = Button( leftframe , text = "Crash-1" , command = partial( queryCrashFactor , rightframe ) )
crash_button1.grid( row = myrow , column = 0 , sticky = mysticky , padx = mypadx , pady = mypady )
myrow += 1

crash_button2 = Button( leftframe , text = "Crash-2" , command = partial( queryCrashRegion , rightframe ) )
crash_button2.grid( row = myrow , column = 0 , sticky = mysticky , padx = mypadx , pady = mypady )
myrow += 1

# ---  Crash & weather join button2 
crash_weather_button1 = Button( leftframe , text = "Crash & Weather-1" , command = partial( queryCrashWeather, rightframe ) )
crash_weather_button1.grid( row = myrow , column = 0 , sticky = mysticky , padx = mypadx , pady = mypady )
myrow += 1

crash_weather_button2 = Button( leftframe , text = "Crash & Weather-2" , command = partial( queryCrashPrecipitation , rightframe ) )
crash_weather_button2.grid( row = myrow , column = 0 , sticky = mysticky , padx = mypadx , pady = mypady )
myrow += 1

# --- show window
root.mainloop()
