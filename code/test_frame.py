from tkinter import *

root = Tk()

root.geometry("400x300")

leftframe = Frame(root)
leftframe.pack(side = LEFT)

rightframe = Frame(root)
rightframe.pack(side = RIGHT)

mysticky = 'E'
mypadx , mypady = 5, 5
myrow = 0
covid_case_button = Button( leftframe , text = "Covid19 Query" )
covid_case_button.grid( row = myrow , column = 0 , sticky = mysticky , padx = mypadx , pady = mypady )
myrow += 1

weather_temp_button = Button( leftframe , text = "Weather Query" )
weather_temp_button.grid( row = myrow , column = 0 , sticky = mysticky , padx = mypadx , pady = mypady )
myrow += 1

crash_button1 = Button( leftframe, text = "Crash Query 1" )
crash_button1.grid( row = myrow , column = 0 , sticky = mysticky , padx = mypadx , pady = mypady )
myrow += 1

root.mainloop()
