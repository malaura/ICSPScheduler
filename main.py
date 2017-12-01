import sys
from tkinter import *
from code.gui import MainWindow

def main():
	'''
	Initializes the MainWindow class, which displays the user interface.
	The user interface is updated continuously in an infinite loop initiated by this method.
	'''
	root = Tk()
	mainWindow = MainWindow.MainWindow(root)
	root.mainloop()

	return 'hello world'



main()
