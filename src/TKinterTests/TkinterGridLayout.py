from tkinter import *

# Fake login Screen with Grid layout
root = Tk()
labelName = Label(root, text="Name")
labelPassword = Label(root, text="Password")
# When the user needs to enter small amount of text, use entry
entryName = Entry(root)
entryPassword = Entry(root)

# aligning to grid
labelName.grid(row=0)
labelPassword.grid(row=1)
entryName.grid(row=0,column=1)
entryPassword.grid(row=1,column=1)


root.mainloop()
