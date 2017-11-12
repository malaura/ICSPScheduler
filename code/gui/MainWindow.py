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
        createButton = ttk.Button(self.centralFrame, text="Create", command=self.createNewPrompt)
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

    def createNewPrompt(self):
        self.prompt = Toplevel(self.root)
        self.prompt.title("Create New Request")

        appHighlightFont = font.Font(family='Helvetica', size=18, weight='bold')
        titleLabel = ttk.Label(self.prompt, text="New Request", font=appHighlightFont)
        titleLabel.grid(row=0, column=0, columnspan=2, sticky="W", pady=10, padx=10)
        nameLabel = ttk.Label(self.prompt, text="Name")
        nameLabel.grid(row=1, column=0, sticky="e")
        monthLabel = ttk.Label(self.prompt, text="Month")
        monthLabel.grid(row=2, column=0, sticky="e")
        dayLabel = ttk.Label(self.prompt, text="Day")
        dayLabel.grid(row=3, column=0, sticky="e")
        startLabel = ttk.Label(self.prompt, text="Start Time")
        startLabel.grid(row=4, column=0, sticky="e")
        endLabel = ttk.Label(self.prompt, text="End Time")
        endLabel.grid(row=5, column=0, sticky="e")
        bufferStart = ttk.Label(self.prompt, text="Buffer Time Before")
        bufferStart.grid(row=6, column=0, sticky="e")
        bufferEnd = ttk.Label(self.prompt, text="Buffer Time After")
        bufferEnd.grid(row=7, column=0, sticky="e")

        nameInput = ttk.Entry(self.prompt, width=20)
        nameInput.grid(row=1, column=1, columnspan=2, padx=10)
        monthInput = ttk.Combobox(self.prompt, width=17, state="readonly")
        monthInput['values'] = ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
                                'September', 'October', 'November', 'December')
        monthInput.grid(row=2, column=1, columnspan=2, padx=10)
        dayInput = ttk.Combobox(self.prompt, width=17, state="readonly")
        days = []
        for i in range(1, 32):
            days.append(i)
        dayInput['values'] = days
        dayInput.grid(row=3, column=1, columnspan=2, padx=10)
        startInput = ttk.Combobox(self.prompt, width=17, state="readonly")
        startInput.grid(row=4, column=1, columnspan=2, padx=10)
        times = []
        for i in range(1, 13):
            times.append(str(i) + " AM")
        for i in range(1, 13):
            times.append(str(i) + " PM")
        startInput['values'] = times
        endInput = ttk.Combobox(self.prompt, width=17, state="readonly")
        endInput.grid(row=5, column=1, columnspan=2, padx=10)
        endInput['values'] = times
        bufferStartInput = ttk.Combobox(self.prompt, width=17, state="readonly")
        bufferStartInput.grid(row=6, column=1, columnspan=2, padx=10)
        bufferList = []
        for i in range(0, 65, 5):
            bufferList.append(i)
        bufferStartInput['values'] = bufferList
        bufferEndInput = ttk.Combobox(self.prompt, width=17, state="readonly")
        bufferEndInput.grid(row=7, column=1, columnspan=2, padx=10)
        bufferEndInput['values'] = bufferList
        assignedView = Listbox(self.prompt, width=20, height=10)
        assignedView.grid(row=8, column=0, padx=5, pady=5, sticky="W")
        availableView = Listbox(self.prompt, width=20, height=10)
        availableView.grid(row=8, column=1, padx=5, pady=5, sticky="E")

        cancelButton = ttk.Button(self.prompt, text="Cancel", command=self.prompt.destroy)
        cancelButton.grid(row=9, column=0, sticky="W", padx=5, pady=5)
        searchButton = ttk.Button(self.prompt, text="Search")
        searchButton.grid(row=9, column=1, sticky="E", padx=5)
        confirmButton = ttk.Button(self.prompt, text="Confirm")
        confirmButton.grid(row=10, column=1, sticky="E", padx=5, pady=(0,5))
