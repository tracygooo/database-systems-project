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

def submitCovidByDateCounty( test_date , county , records ):
    connect_string = "host='localhost' dbname='dbms_final_project' user='dbms_project_user' password='dbms_password'"
    conn = psycopg2.connect( connect_string )
    cursor = conn.cursor()
    query = "SELECT * FROM covid19 WHERE testdate = %s and county ILIKE %s"
    cursor.execute( query , ( test_date.get() , county.get() ) )
    records.set( cursor.fetchall()[0] )
    print(records.get())
    conn.commit()

    print_records = "Date \t County \t New Positive \t Total tested\n"
    #for record in records :
    #    print_records = print_records + str( record ) + '\n'
    print( records )
    # records_label.pack()

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

def queryCovidByDateCounty( frame , records ):
    clearChildren( frame )

    # Create text labels
    date_label = Label( frame , text = "Date" )
    date_label.grid( row = 0 , column = 1 )
    county_label = Label( frame , text = "County" )
    county_label.grid( row = 1 , column = 1 )

    # Create text boxes
    test_date = Entry( frame , width = 30 )
    test_date.grid( row = 0 , column = 2  )
    county = Entry( frame , width = 30 )
    county.grid( row = 1 , column = 2 )

    # Create submit button
    my_submit = Button( frame , text = "Submit" , command = partial( submitCovidByDateCounty , test_date , county , records ) )
    my_submit.grid( row = 2 , column = 2 , columnspan = 2 , pady = 10 , padx = 10, ipadx = 100 )

def queryCovidRankCases( frame , records ):
    clearChildren( frame )
    return True


def weatherQuery( root ):
    return True

def crashQuery1( root ):
    return True

def crashQuery2( root ):
    return True

def crashWeatherQuery1( root ):
    return True

def crashWeatherQuery2( root ):
    return True

def crashCovidQuery( root ):
    return True

# --- Setup window 
root = Tk()
app = Window(root)
root.wm_title("Database Systems Final Project")
root.geometry( "600x400" )

leftframe = Frame(root)
leftframe.pack(side = LEFT)

rightframe = Frame(root)
rightframe.pack(side = RIGHT)

# --- Buttons linked to queries 
mypadx , mypady = 5 , 5 
mysticky = "E"
myrow = 0
records = StringVar()
records_label = Label( rightframe , textvariable = records )
records_label.grid( row = 3 , column = 2 , columnspan = 2 )

covid_button1 = Button( leftframe , text = "Covid19-1" , command = partial( queryCovidByDateCounty , rightframe , records ) )
covid_button1.grid( row = myrow , column = 0 , sticky = mysticky , padx = mypadx , pady = mypady )
myrow += 1

covid_button2 = Button( leftframe , text = "Covid19-2" , command = partial( queryCovidRankCases , rightframe , records ) )
covid_button2.grid( row = myrow , column = 0 , sticky = mysticky , padx = mypadx , pady = mypady )
myrow += 1

"""
weather_temp_button = Button( root , text = "Weather Query" , command = partial( weatherQuery, root ) )
weather_temp_button.grid( row = myrow , column = 0 , sticky = mysticky , padx = mypadx , pady = mypady )
myrow += 1

crash_button1 = Button( root , text = "Crash Query 1" , command = partial( crashQuery1, root ) )
crash_button1.grid( row = myrow , column = 0 , sticky = mysticky , padx = mypadx , pady = mypady )
myrow += 1

crash_button2 = Button( root , text = "Crash Query 2" , command = partial( crashQuery2, root ) )
crash_button2.grid( row = myrow , column = 0 , sticky = mysticky , padx = mypadx , pady = mypady )
myrow += 1

crash_weather_button1 = Button( root , text = "Crash Weather Query1" , command = partial( crashWeatherQuery1, root ) )
crash_weather_button1.grid( row = myrow , column = 0 , sticky = mysticky , padx = mypadx , pady = mypady )
myrow += 1

crash_weather_button2 = Button( root , text = "Crash Weather Query2" , command = partial( crashWeatherQuery2, root ) )
crash_weather_button2.grid( row = myrow , column = 0 , sticky = mysticky , padx = mypadx , pady = mypady )
myrow += 1
"""

# --- show window
root.mainloop()
