import sys
from tkinter import *
from code.gui import MainWindow

def main():
	root = Tk()
	mainWindow = MainWindow.MainWindow(root)
	root.mainloop()

	return 'hello world'



main()
