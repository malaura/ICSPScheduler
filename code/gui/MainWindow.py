from tkinter import *
from tkinter import ttk
from tkinter import font
from .Prompt import Prompt
import calendar


class MainWindow():
    def __init__(self, root):
        self.root = root
        self.root.title("ICSPS Scheduler")
        self.width = 800
        self.height = 350
        self.root.minsize(height=self.height, width=self.width)
        self.root.maxsize(height=self.height, width=self.width)
        self.months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
                                'September', 'October', 'November', 'December']
        self.currentMonth = 12
        self.currentYear = 2017
        self.calendar = calendar.Calendar(firstweekday=6)
        self.buttons = []

        self.initializeUI()
        #self.prompt = Prompt(self, "test", "hello word")

    def initializeUI(self):
        menu = Menu(self.root)
        # Use a different image if the sys platform is a Mac
        if sys.platform == 'darwin':
            self.root.maxsize(height=350, width=self.width+400)
            self.root.minsize(height=300, width=self.width+200)
        self.root.config(menu=menu)
        filemenu = Menu(menu)
        menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.root.destroy)

        self.leftFrame = ttk.Frame(self.root, width=self.width/3, height=300)
        self.leftFrame.grid(row=0, column=0, sticky=NS)
        self.centralFrame = ttk.Frame(self.root, width=self.width/3, height=300)
        self.centralFrame.grid(row=0, column=1, sticky=NS)
        self.rightFrame = ttk.Frame(self.root, width=self.width/3, height=300)
        self.rightFrame.grid(row=0, column=2, sticky=NS)

        # Initalize left frame widgets
        requestLabel = Label(self.leftFrame, text="Request", background="gray90")
        requestLabel.grid(column=0, row=0, columnspan=2)
        requestView = Listbox(self.leftFrame, height=17, width=20)
        requestView.grid(row=1, column=0, padx=5, columnspan=2)
        editButton = ttk.Button(self.leftFrame, text="Edit", width=8)
        editButton.grid(row=2, column=0, sticky=W, padx=5)


        # Initalize central frame widgets
        appHighlightFont = font.Font(family='Helvetica', size=18, weight='bold')
        self.monthLabel = Label(self.centralFrame, text=self.months[self.currentMonth-1], font=appHighlightFont, background="gray90")
        self.monthLabel.grid(column=0, row=0, columnspan=2)
        leftButton = ttk.Button(self.centralFrame, text="<", width=5, command=self.prevMonth)
        leftButton.grid(column=4, row=8, sticky=E, pady=5)
        rightButton = ttk.Button(self.centralFrame, text=">", width=5, command=self.nextMonth)
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
        for i in range(6):
            for j in range(7):
                dayButton = ttk.Button(self.centralFrame, text=" "+"\n")
                dayButton.grid(row=i+2, column=j)
                self.buttons.append(dayButton)
                count += 1

        index = 0
        for day in self.calendar.itermonthdays(self.currentYear, self.currentMonth):
            curButton = self.buttons[index]
            if day == 0:
                curButton.configure(text=" "+"\n")
            else:
                curButton.configure(text=str(self.currentMonth)+"/"+str(day)+"\n")
            index += 1
        # Initialize right frame widgets
        studentLabel = Label(self.rightFrame, text="Students", background="gray90")
        studentLabel.grid(row=0, column=0, columnspan=2)
        studentView = Listbox(self.rightFrame, height=17, width=20)
        studentView.grid(row=1, column=0, padx=5, columnspan=2)
        addButton = ttk.Button(self.rightFrame, text="+", width=5)
        addButton.grid(row=2, column=0, sticky=E)
        removeButton = ttk.Button(self.rightFrame, text="-", width=5)
        removeButton.grid(row=2, column=1, sticky=W)

    def createNewPrompt(self):
        self.prompt = Toplevel(self.root)
        self.prompt.title("Create New Request")
        self.prompt.configure(background = "gray90")
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
        nameInput.grid(row=1, column=1, columnspan=3, padx=10)
        monthInput = ttk.Combobox(self.prompt, width=17, state="readonly")
        monthInput['values'] = ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
                                'September', 'October', 'November', 'December')
        monthInput.grid(row=2, column=1, columnspan=3, padx=10)
        dayInput = ttk.Combobox(self.prompt, width=17, state="readonly")
        days = []
        for i in range(1, 32):
            days.append(i)
        dayInput['values'] = days
        dayInput.grid(row=3, column=1, columnspan=3, padx=10)
        startHourInput = ttk.Combobox(self.prompt, width=3, state="readonly")
        startHourInput.grid(row=4, column=1, sticky="E", padx=(10,0))
        startHourInput['values'] = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
        startMinuteInput = ttk.Combobox(self.prompt, width=5, state="readonly")
        startMinuteInput.grid(row=4, column=2, sticky="WE")
        times = []
        for i in range(0, 60, 5):
            if i < 10:
                times.append('0'+str(i))
            else:
                times.append(str(i))
        startMinuteInput['values'] = times
        startTimeInput = ttk.Combobox(self.prompt, width=3, state="readonly")
        startTimeInput.grid(row=4, column=3, padx=(0,10), sticky="W")
        startTimeInput['values'] = ("AM", "PM")
        endHourInput = ttk.Combobox(self.prompt, width=3, state="readonly")
        endHourInput.grid(row=5, column=1, sticky="E", padx=(10,0))
        endHourInput['values'] = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
        endMinuteInput = ttk.Combobox(self.prompt, width=5, state="readonly")
        endMinuteInput.grid(row=5, column=2, sticky="WE")
        endMinuteInput['values'] = times
        endTimeInput = ttk.Combobox(self.prompt, width=3, state="readonly")
        endTimeInput.grid(row=5, column=3, padx=(0,10), sticky="W")
        endTimeInput['values'] = ("AM", "PM")
        bufferStartInput = ttk.Combobox(self.prompt, width=17, state="readonly")
        bufferStartInput.grid(row=6, column=1, columnspan=3, padx=10)
        bufferList = []
        for i in range(0, 65, 5):
            bufferList.append(i)
        bufferStartInput['values'] = bufferList
        bufferEndInput = ttk.Combobox(self.prompt, width=17, state="readonly")
        bufferEndInput.grid(row=7, column=1, columnspan=3, padx=10)
        bufferEndInput['values'] = bufferList
        assignedView = Listbox(self.prompt, width=20, height=10)
        assignedView.grid(row=8, column=0, padx=5, pady=5, sticky="W")
        availableView = Listbox(self.prompt, width=20, height=10)
        availableView.grid(row=8, column=1, columnspan=3, padx=5, pady=5, sticky="E")

        cancelButton = ttk.Button(self.prompt, text="Cancel", command=self.prompt.destroy)
        cancelButton.grid(row=10, column=0, sticky="W", padx=5, pady=(0,5))
        searchButton = ttk.Button(self.prompt, text="Search")
        searchButton.grid(row=9, column=1, sticky="E", columnspan=3, padx=5)
        confirmButton = ttk.Button(self.prompt, text="Confirm")
        confirmButton.grid(row=10, column=1, sticky="E", columnspan=3, padx=5, pady=(0,5))

    def nextMonth(self):
        if self.currentMonth == 12:
            self.currentMonth = 1
            self.currentYear += 1
        else:
            self.currentMonth += 1
        self.updateCalendar()

    def prevMonth(self):
        if self.currentMonth == 1:
            self.currentMonth = 12
            self.currentYear -=1
        else:
            self.currentMonth -= 1
        self.updateCalendar()

    def updateCalendar(self):
        index = 0
        for day in self.calendar.itermonthdays(self.currentYear, self.currentMonth):
            curButton = self.buttons[index]
            if day == 0:
                curButton.configure(text=" "+"\n")
            else:
                curButton.configure(text=str(self.currentMonth)+"/"+str(day)+"\n")
            index += 1
        self.monthLabel.configure(text=self.months[self.currentMonth-1])
