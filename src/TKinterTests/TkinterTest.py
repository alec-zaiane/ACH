from tkinter import *

mainWindow = Tk()
topFrame = Frame(mainWindow, highlightbackground="black", highlightthickness=1)
topFrame.pack()

bottomFrame = Frame(mainWindow, highlightbackground="black", highlightthickness=1)
bottomFrame.pack(side=BOTTOM)

button1 = Button(topFrame, text="Button 1", fg="red")
button2 = Button(topFrame, text="Button 2", fg="blue")
button3 = Button(topFrame, text="Button 3", fg="green")
button4 = Button(bottomFrame, text="Button 4", fg="yellow")
button1.pack(side=LEFT)
button2.pack(side=LEFT)
button3.pack(side=LEFT)
button4.pack(side=BOTTOM)

textOne = Label(mainWindow,text="ONE",bg="red",fg="white")
textOne.pack(side=TOP,fill=BOTH)

mainWindow.mainloop()
