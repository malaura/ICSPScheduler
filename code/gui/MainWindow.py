from tkinter import *
from tkinter import ttk
from tkinter import font
from .Prompt import Prompt


class MainWindow():
    def __init__(self, root):
        self.root = root
        self.root.title("ICSPS Scheduler")
        self.root.minsize(height=300, width=800)
        self.root.maxsize(height=300, width=800)
        self.month = "November"

        self.initializeUI()
        #self.prompt = Prompt(self, "test", "hello word")

    def initializeUI(self):
        menu = Menu(self.root)
        # Use a different image if the sys platform is a Mac
        if sys.platform == 'darwin':
            self.root.maxsize(height=350, width=1200)
            self.root.minsize(height=300, width=1000)
        self.root.config(menu=menu)
        filemenu = Menu(menu)
        menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.root.destroy)

        self.leftFrame = ttk.Frame(self.root, width=800/3, height=300)
        self.leftFrame.grid(row=0, column=0, sticky=NS)
        self.centralFrame = ttk.Frame(self.root, width=800/3, height=300)
        self.centralFrame.grid(row=0, column=1, sticky=NS)
        self.rightFrame = ttk.Frame(self.root, width=800/3, height=300)
        self.rightFrame.grid(row=0, column=2, sticky=NS)

        # Initalize left frame widgets
        requestLabel = Label(self.leftFrame, text="Requests", background="gray90")
        requestLabel.grid(column=0, row=0, columnspan=2)
        requestView = Listbox(self.leftFrame, height=15, width=20)
        requestView.grid(row=1, column=0, padx=5, columnspan=2)
        newButton = ttk.Button(self.leftFrame, text="New",width=8)
        newButton.grid(row=2, column=0, sticky=E)
        editButton = ttk.Button(self.leftFrame, text="Edit", width=8)
        editButton.grid(row=2, column=1, sticky=W)


        # Initalize central frame widgets
        appHighlightFont = font.Font(family='Helvetica', size=18, weight='bold')
        monthLabel = Label(self.centralFrame, text=self.month, font=appHighlightFont, background="gray90")
        monthLabel.grid(column=0, row=0, columnspan=2)
        leftButton = ttk.Button(self.centralFrame, text="<", width=5)
        leftButton.grid(column=4, row=8, sticky=E, pady=5)
        rightButton = ttk.Button(self.centralFrame, text=">", width=5)
        rightButton.grid(column=5, row=8, sticky=W, pady=5)
        createButton = ttk.Button(self.centralFrame, text="Create")
        createButton.grid(column=6, row=8, columnspan=2, pady=5)


        days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Satuday"]
        count = 0
        for day in days:
            dayLabel = Label(self.centralFrame, text=day, background="gray90")
            dayLabel.grid(row=1, column=count)
            count += 1

        count = 1
        for i in range(5):
            for j in range(7):
                dayButton = ttk.Button(self.centralFrame, text=str(count)+"\n")
                dayButton.grid(row=i+2, column=j)
                count += 1
        # Initialize right frame widgets
        studentLabel = Label(self.rightFrame, text="Students", background="gray90")
        studentLabel.grid(row=0, column=0, columnspan=2)
        studentView = Listbox(self.rightFrame, height=15, width=20)
        studentView.grid(row=1, column=0, padx=5, columnspan=2)
        addButton = ttk.Button(self.rightFrame, text="+", width=5)
        addButton.grid(row=2, column=0, sticky=E)
        removeButton = ttk.Button(self.rightFrame, text="-", width=5)
        removeButton.grid(row=2, column=1, sticky=W)
