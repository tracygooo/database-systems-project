from tkinter import *

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        for r in range(7):
            self.master.rowconfigure(r, weight=1)    
        for c in range(6):
            self.master.columnconfigure(c, weight=1)

        self.left_frame = Frame(master, bg="red")
        self.left_frame.grid(row = 0, column = 0, rowspan = 7, columnspan = 2, sticky = W+E+N+S) 
        self.top_right_frame = Frame(master, bg="grey")
        self.top_right_frame.grid(row = 0, column = 2, rowspan = 3, columnspan = 4, sticky = W+E+N+S)
        self.bottom_right_frame = Frame(master, bg="white")
        self.bottom_right_frame.grid(row = 3, column = 2, rowspan = 4, columnspan = 4, sticky = W+E+N+S)

    def createMultiButtons( self , button_names , mypad , mysticky ) :
        for i in range( len( button_names ) ) :
            button = Button( self.left_frame , text = button_names[i]  )
            button.grid( row = i , column = 0 , sticky = mysticky , padx = mypad , pady = mypad )

    def createMultiButtons2( self , button_names , mypad , mysticky ) :
        for i in range( len( button_names ) ) :
            button = Button( self.top_right_frame , text = button_names[i]  )
            button.grid( row = i , column = 0 , sticky = mysticky , padx = mypad , pady = mypad )
    def printText( self , mytext ) :
        T = Text( self.bottom_right_frame , height = 30 , width = 30 )
        T.pack()
        T.insert( END , mytext )

root = Tk()
root.geometry("800x600+1200+1200")
#root.geometry("800x600")
app = Application(master=root)
buttons = ['1' , '2', '3', '4', '5', '6', '7']
app.createMultiButtons( buttons , 5 , 'E' )
mytext = "Hello world!\n"*10
app.printText( mytext )
app.mainloop()
