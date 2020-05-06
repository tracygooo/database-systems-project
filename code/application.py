import psycopg2
import psycopg2.extras
import os

from tkinter import *
from datetime import datetime
from functools import partial
from tabulate import tabulate

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.grid()

        for r in range(7):
            self.master.rowconfigure(r, weight=1)    
        for c in range(6):
            self.master.columnconfigure(c, weight=1)

        self.left_frame = Frame( master )
        self.left_frame.grid(row = 0, column = 0, rowspan = 7, columnspan = 2, sticky = W+E+N+S) 
        self.top_right_frame = Frame( master )
        self.top_right_frame.grid(row = 0, column = 2, rowspan = 2, columnspan = 4, sticky = W+E+N+S)
        self.bottom_right_frame = Frame(master, bg="white")
        self.bottom_right_frame.grid(row = 3, column = 2, rowspan = 4, columnspan = 4, sticky = W+E+N+S)

        self.records_text = Text( self.bottom_right_frame , height = 25 , width = 70 )
        self.records_text.pack()

        self.connect_string = '''host='localhost' 
                                 dbname='dbms_final_project' 
                                 user='dbms_project_user' 
                                 password='dbms_password' '''
        self.conn = psycopg2.connect( self.connect_string )
        self.cursor = self.conn.cursor()


    def createUserInput( self , frame , curr_row , reminder ) :
        my_label = Label( frame , text = reminder )
        my_label.grid( row = curr_row , column = 0 )
        my_entry = Entry( frame , width = 30 )
        my_entry.grid( row = curr_row , column = 1  )
        return my_entry

    def clearText( self ):
        self.records_text.delete("1.0", END)

    def outputRecords( self , records , headers ) :
        self.clearChildren( self.bottom_right_frame )
        print_records = tabulate( records , headers , tablefmt = "fancy_grid" )
        print( print_records )
        self.clearText()
        #records_text = Text( self.bottom_right_frame , height = len(records) + 5, width = 60 )
        #records_text.pack()
        self.records_text.insert( END , print_records )

    def submitCovidByDateCounty( self , test_date , county ):
        query = "SELECT * FROM covid19 WHERE testdate = %s and county ILIKE %s"
        self.cursor.execute( query , ( test_date.get() , county.get() ) )
        self.conn.commit()

        records = self.cursor.fetchall()
        headers = [ 'Date' , 'County' , 'New Positive' , 'Total tests' ] 

        self.outputRecords( records , headers )

    def submitCovidRankCases( self , start_date , end_date , limit ):
        query = "SELECT county, SUM(newpositives) "\
                + "FROM covid19 WHERE testdate >= %s AND testdate <= %s "\
                + "GROUP BY county " + \
                "ORDER BY sum(newpositives) DESC LIMIT %s ;"
        self.cursor.execute( query , ( start_date.get() , end_date.get() , limit.get() ) )
        self.conn.commit()

        records = self.cursor.fetchall()
        headers = [ 'County' , 'Accumulated positives' ]
        self.outputRecords( records , headers )

    def submitCovidPosRatio( self , start_date , end_date , county ):
        query = '''
                SELECT cast(sum(newpositives)::NUMERIC/sum(totalnumberoftestsperformed) as decimal(10,2))
                FROM covid19
                WHERE TestDATE >= %s 
                AND TestDATE <= %s
                AND County ilike %s;       
                '''
        self.cursor.execute( query , ( start_date.get() , end_date.get() , county.get() ) )
        self.conn.commit()
        records = self.cursor.fetchall()
        headers = [ 'Psotivity rate' ]
        self.outputRecords( records , headers )


    def submitCrashFactor( self , limit , frame , myrow ):
        print( "Running, takes around 10 seconds..." )
        query = '''
                SELECT DISTINCT(a.factor),count(collision_id) rank
                FROM factor,(
                SELECT DISTINCT factor1 as factor
                FROM factor
                GROUP BY factor1
                UNION
                SELECT DISTINCT factor2
                FROM factor
                GROUP BY factor2
                UNION
                SELECT DISTINCT factor3
                FROM factor
                GROUP BY factor3
                UNION   
                SELECT DISTINCT factor4
                FROM factor
                GROUP BY factor4
                UNION
                SELECT DISTINCT factor5
                FROM factor
                GROUP BY factor5) a
                WHERE a.factor = factor1
                OR a.factor=factor2
                OR a.factor=factor3
                OR a.factor=factor4
                OR a.factor=factor5
                GROUP BY factor
                ORDER BY rank DESC LIMIT %s;
                '''
        self.cursor.execute( query , ( limit.get(), ) )
        self.conn.commit()
        records = self.cursor.fetchall()
        headers = [ 'Factors' , 'Number of Crashes' ]
        self.outputRecords( records , headers )

    def submitCrashRegion( self , start_date , end_date  ):
        query = '''
                SELECT region , count(region) FROM occurence
                WHERE region NOT LIKE '' AND 
                      crashDate >= %s AND crashDate <= %s
                GROUP BY region
                HAVING count(region) > 0
                ORDER BY count(region) DESC
                '''
        self.cursor.execute( query , ( start_date.get() , end_date.get() ) )
        self.conn.commit()
        records = self.cursor.fetchall()
        headers = [ 'Borough', '# of crashes' ]
        self.outputRecords( records , headers )

    def submitCrashWeather( self , weather_type ):

        weather = weather_type.get()
        l =['is_foggy','is_foggy_heavy','is_thunder',
            'is_ice_pellets','is_glaze_rime','is_smoke_haze', 
            'is_damaging_wind','is_mist', 'is_drizzle', 'is_rainy', 
            'is_snowy', 'is_unknown_precipitation',  'is_freezing_foggy']

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

        self.cursor.execute( query )
        self.conn.commit()
        records = self.cursor.fetchall()
        headers = [ 'Ave num of crashes in {}'.format( weather_type.get() )  ]
        self.outputRecords( records , headers )

    def submitCrashPrecipitation(  self , low , high , frame , myrow ):
        query = '''
                SELECT count(COLLISION_ID)/tyw as ratio
                FROM occurence, precipitation,(
                SELECT count(measure_date) tyw
                FROM precipitation
                WHERE precipitation >= %s
                AND precipitation <= %s) wyt
                WHERE precipitation >= %s
                AND precipitation <= %s
                AND crashdate = measure_date
                GROUP BY tyw;
                '''

        self.cursor.execute( query , ( low.get(), high.get() , low.get() , high.get() ) )
        self.conn.commit()
        records = self.cursor.fetchall()
        headers = [ 'Ave num of crashes when {}mm < PRCP < {}mm'.format( low.get() ,high.get() ) ]
        self.outputRecords( records , headers )


    def getChildren ( self , window ) :
        child_list = window.winfo_children()
        for item in child_list :
            if item.winfo_children() :
                child_list.extend(item.winfo_children())
        return child_list

    def clearChildren( self , window ) :
        widget_list = self.getChildren(window)
        for item in widget_list:
            item.grid_forget()

    def queryCovidByDateCounty( self , frame ) :
        self.clearChildren( frame )

        # Create text labels and entry boxes
        myrow = 0
        date_entry = self.createUserInput( frame , myrow , "Date" )
        myrow += 1
        county_entry = self.createUserInput( frame , myrow , "County" )
        myrow += 1

        # Create submit button
        my_submit = Button( frame , text = "Submit" , command = partial( self.submitCovidByDateCounty , date_entry , county_entry ) )
        my_submit.grid( row = myrow , column = 1 , columnspan = 2 , pady = 10 , padx = 10, ipadx = 100 )

    def queryCovidRankCases( self , frame ) :
        self.clearChildren( frame )

        myrow = 0
        date_start_entry = self.createUserInput( frame , myrow , "Start date" )
        myrow += 1

        date_end_entry = self.createUserInput( frame , myrow , "End date" )
        myrow += 1

        limit_entry = self.createUserInput( frame , myrow , "Top n counties" )
        myrow += 1

        # Create submit button
        my_submit = Button( frame , text = "Submit" , command = partial( self.submitCovidRankCases , date_start_entry , date_end_entry , limit_entry ) )
        my_submit.grid( row = myrow , column = 1 , columnspan = 2 , pady = 10 , padx = 10, ipadx = 100 )


    def queryCovidPosRatio( self , frame ) :
        self.clearChildren( frame )
        myrow = 0
        date_start_entry = self.createUserInput( frame , myrow , "Start date" )
        myrow += 1

        date_end_entry = self.createUserInput( frame , myrow , "End date" )
        myrow += 1

        county_entry = self.createUserInput( frame , myrow , "County" )
        myrow += 1

        # Create submit button
        my_submit = Button( frame , text = "Submit" , command = partial( self.submitCovidPosRatio , date_start_entry , date_end_entry , county_entry ) )
        my_submit.grid( row = myrow , column = 1 , columnspan = 2 , pady = 10 , padx = 10, ipadx = 100 )

    def queryCrashFactor( self , frame ) :
        self.clearChildren( frame )
        myrow = 0
        limit_label = Label( frame , text = "Top n factors" )
        limit_label.grid( row = myrow , column = 0 )
        limit_entry = Entry( frame , width = 30 )
        limit_entry.grid( row = myrow , column = 1  )
        myrow += 1

        # Create submit button
        my_submit = Button( frame , text = "Submit" , command = partial( self.submitCrashFactor , limit_entry , frame , myrow ) )
        my_submit.grid( row = myrow , column = 1 , columnspan = 2 , pady = 10 , padx = 10, ipadx = 100 )

    def queryCrashRegion( self , frame ):
        self.clearChildren( frame )
        date_start_entry = self.createUserInput( frame , 0 , "Start date" )
        date_end_entry = self.createUserInput( frame , 1 , "End date" )

        # Create submit button
        my_submit = Button( frame , text = "Submit" , command = partial( self.submitCrashRegion, date_start_entry , date_end_entry ) )
        my_submit.grid( row = 2 , column = 1 , columnspan = 2 , pady = 10 , padx = 10, ipadx = 100 )

    def queryCrashWeather( self , frame ) :
        self.clearChildren( frame )
        myrow = 0
        type_label = Label( frame , text = "Weather type" )
        type_label.grid( row = myrow , column = 0 )
        type_entry = Entry( frame , width = 30 )
        type_entry.grid( row = myrow , column = 1  )
        myrow += 1

        # Create submit button
        my_submit = Button( frame , text = "Submit" , command = partial( self.submitCrashWeather , type_entry ) )
        my_submit.grid( row = myrow , column = 1 , columnspan = 2 , pady = 10 , padx = 10, ipadx = 100 )

    def queryCrashPrecipitation( self , frame ) :
        self.clearChildren( frame )

        # Create entries
        myrow = 0
        low_entry = self.createUserInput( frame , myrow , "Precipitation low" )
        myrow += 1
        up_entry = self.createUserInput( frame , myrow ,  "Precipitation high" )
        myrow += 1

        # Create submit button
        my_submit = Button( frame , text = "Submit" , command = partial( self.submitCrashPrecipitation , low_entry , up_entry , frame , myrow ) )
        my_submit.grid( row = myrow , column = 1 , columnspan = 2 , pady = 10 , padx = 10, ipadx = 100 )

    def createMultiButtons( self , button_names , functions , mypad , mysticky ) :
        for i in range( len( button_names ) ) :
            button = Button( self.left_frame , text = button_names[i] , 
                             command = partial( functions[i] , self.top_right_frame ) )
            button.grid( row = i , column = 0 , sticky = mysticky , padx = mypad , pady = mypad )

def main() :
    # Setup window 
    root = Tk()
    app = Window(root)
    root.wm_title( "Database Systems Final Project" )
    root.geometry("600x400+1200+1200")

    # Create buttons for querying
    mypad , mysticky = 10 , W+E+N+S 
    button_names = ["Covid19-1" , "Covid19-2" ,  "Covid19-3" , 
                    "Crash-1" , "Crash-2" , "Crash & Weather-1" , 
                    "Crash & Weather-2" ] 
    functions = [ app.queryCovidByDateCounty , app.queryCovidRankCases , 
                  app.queryCovidPosRatio , app.queryCrashFactor , 
                  app.queryCrashRegion , app.queryCrashWeather , app.queryCrashPrecipitation ]

    app.createMultiButtons( button_names , functions , mypad , mysticky )

    # show window
    root.mainloop()

if __name__ == "__main__":
    main()
