import psycopg2
import psycopg2.extras
import os

from datetime import datetime
from tkinter import *

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

def submit():
    connect_string = "host='localhost' dbname='dbms_final_project' user='dbms_project_user' password='dbms_password'"
    conn = psycopg2.connect( connect_string )
    cursor = conn.cursor()
    query = "SELECT * FROM covid19 WHERE testdate = %s and county ILIKE %s"
    # query = "SELECT * FROM covid19 WHERE testdate >= %s and county ILIKE %s"
    cursor.execute( query , ( test_date.get() , county.get() ) )
    records = cursor.fetchall()
    print_records = "Date \t County \t New Positive \t Total tested\n"
    for record in records :
        print_records = print_records + str( record ) + '\n'
    print( records )
    records_label = Label( root , text = print_records )
    records_label.grid( row = 3 , column = 0 , columnspan = 3 )
    conn.commit()

# Setup window 
root = Tk()
app = Window(root)
root.wm_title("Database Systems Final Project")
root.geometry( "800x800" )

# Create text labels
date_label = Label( root , text = "Date" )
date_label.grid( row = 0 , column = 0 )
county_label = Label( root , text = "County" )
county_label.grid( row = 1 , column = 0 )

# Create text boxes
test_date = Entry( root , width = 30 )
test_date.grid( row = 0 , column = 1  )
county = Entry( root , width = 30 )
county.grid( row = 1 , column = 1  )

# Create submit button
my_submit = Button( root , text = "Submit" , command = submit )
my_submit.grid( row = 2 , column = 0 , columnspan = 2 , pady = 10 , padx = 10, ipadx = 100 )

# show window
root.mainloop()
