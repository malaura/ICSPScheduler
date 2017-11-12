from tkinter import *
from tkinter import ttk
from .Prompt import Prompt


class MainWindow():
    def __init__(self, root):
        self.root = root
        self.root.title("ICSPS Scheduler")
        self.root.minsize(height=600, width=800)
        self.root.maxsize(height=600, width=800)

        self.initializeUI()

    def initializeUI(self):
        menu = Menu(self.root)
        self.root.config(menu=menu)
        filemenu = Menu(menu)
        menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.root.destroy)
        self.prompt = Prompt(self, "test", "hello word")
