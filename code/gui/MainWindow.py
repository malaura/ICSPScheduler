from tkinter import *
from tkinter import ttk
from tkinter import font
from .Prompt import Prompt
from ..stubFunctions import *
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

        self.students = load_all_student()
        #self.test = Requests()
        #self.req = self.test.Request("Syd", "01/01/2017", "12:00", "13:00", "00:05", "00:05")
        #self.test.add_request(self.req)
        self.requests = Requests()

        self.initializeUI()
        #self.prompt = Prompt(self, "test", "hello word")

    def initializeUI(self):

        #print(self.requests)
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
        appHighlightFont = font.Font(family='Helvetica', size=14, weight='bold')
        self.monthLabel = Label(self.centralFrame, text=self.months[self.currentMonth-1]+ " " + str(self.currentYear), font=appHighlightFont, background="gray90")
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
                dayButton = ttk.Button(self.centralFrame, text="\n")
                dayButton.grid(row=i+2, column=j)
                self.buttons.append(dayButton)
                count += 1

        index = 0
        for day in self.calendar.itermonthdays(self.currentYear, self.currentMonth):
            curButton = self.buttons[index]
            if self.currentMonth < 10:
                month = "0" + str(self.currentMonth)
            else:
                month = str(self.currentMonth)
            if day == 0:
                curButton.configure(text="\n")
            else:
                if day < 10:
                    curButton.configure(text=month+"/"+"0"+str(day)+"\n")
                else:
                    curButton.configure(text=month+"/"+str(day)+"\n")
            index += 1

        # Initialize right frame widgets
        studentLabel = Label(self.rightFrame, text="Students", background="gray90")
        studentLabel.grid(row=0, column=0, columnspan=2)
        studentView = Listbox(self.rightFrame, height=17, width=20)
        for student in self.students:
            studentView.insert(END, student)
            print(self.students[student].get_dictionary_of_schedule())

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

        self.nameInput = ttk.Entry(self.prompt, width=20)
        self.nameInput.grid(row=1, column=1, columnspan=2, padx=10)
        self.monthInput = ttk.Combobox(self.prompt, width=17, state="readonly")
        #monthInput['values'] = ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
        #                        'September', 'October', 'November', 'December')
        months = []
        for i in range(1,13):
            if i < 10:
                months.append('0'+str(i))
            else:
                months.append(str(i))
        self.monthInput['values'] = months
        self.monthInput.grid(row=2, column=1, columnspan=2, padx=10)
        self.dayInput = ttk.Combobox(self.prompt, width=17, state="readonly")
        days = []
        for i in range(1, 32):
            if i < 10:
                days.append("0"+str(i))
            else:
                days.append(str(i))
        self.dayInput['values'] = days
        self.dayInput.grid(row=3, column=1, columnspan=2, padx=10)
        self.startHourInput = ttk.Combobox(self.prompt, width=3, state="readonly")
        self.startHourInput.grid(row=4, column=1, sticky="E", padx=(10,0))
        hours = []
        for i in range(23):
            if i < 10:
                hours.append('0'+str(i))
            else:
                hours.append(i)
        self.startHourInput['values'] = hours
        self.startMinuteInput = ttk.Combobox(self.prompt, width=5, state="readonly")
        self.startMinuteInput.grid(row=4, column=2, sticky="W")
        times = []
        for i in range(0, 60, 5):
            if i < 10:
                times.append('0'+str(i))
            else:
                times.append(str(i))
        self.startMinuteInput['values'] = times
        #startTimeInput = ttk.Combobox(self.prompt, width=3, state="readonly")
        #startTimeInput.grid(row=4, column=3, padx=(0,10), sticky="W")
        #startTimeInput['values'] = ("AM", "PM")
        self.endHourInput = ttk.Combobox(self.prompt, width=3, state="readonly")
        self.endHourInput.grid(row=5, column=1, sticky="EW", padx=(0,0))
        self.endHourInput['values'] = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
        self.endMinuteInput = ttk.Combobox(self.prompt, width=3, state="readonly")
        self.endMinuteInput.grid(row=5, column=2, sticky="EW")
        self.endMinuteInput['values'] = times
        #endTimeInput = ttk.Combobox(self.prompt, width=3, state="readonly")
        #endTimeInput.grid(row=5, column=3, padx=(0,10), sticky="W")
        #endTimeInput['values'] = ("AM", "PM")
        self.bufferStartInput = ttk.Combobox(self.prompt, width=17, state="readonly")
        self.bufferStartInput.grid(row=6, column=1, columnspan=2, padx=10)
        bufferList = []
        for i in range(0, 65, 5):
            bufferList.append(i)
        self.bufferStartInput['values'] = bufferList
        self.bufferEndInput = ttk.Combobox(self.prompt, width=17, state="readonly")
        self.bufferEndInput.grid(row=7, column=1, columnspan=2, padx=10)
        self.bufferEndInput['values'] = bufferList
        assignedLabel = ttk.Label(self.prompt, text="Assigned")
        assignedLabel.grid(row=8, column=0, pady=5)
        assignedView = Listbox(self.prompt, width=20, height=10)
        assignedView.grid(row=9, column=0, padx=(5,0), pady=5, sticky="W")
        availableLabel = ttk.Label(self.prompt, text="Available Students")
        availableLabel.grid(row=8, column=1, pady=(5,0))
        availableView = Listbox(self.prompt, width=20, height=10)
        availableView.grid(row=9, column=1, columnspan=2, padx=5, pady=5, sticky="E")

        cancelButton = ttk.Button(self.prompt, text="Cancel", command=self.prompt.destroy)
        cancelButton.grid(row=11, column=0, sticky="W", padx=5, pady=(0,5))
        searchButton = ttk.Button(self.prompt, text="Search", command=self.createRequest)
        searchButton.grid(row=10, column=1, sticky="E", columnspan=2, padx=5)
        confirmButton = ttk.Button(self.prompt, text="Confirm")
        confirmButton.grid(row=11, column=1, sticky="E", columnspan=2, padx=5, pady=(0,5))

    def createRequest(self):
        request = self.requests.Request(self.nameInput.get(),
                  self.monthInput.get()+"/"+self.dayInput.get()+"/"+str(self.currentYear),
                  str(self.startHourInput.get())+":"+str(self.startMinuteInput.get()),
                  str(self.endHourInput.get())+":"+str(self.endMinuteInput.get()),
                  "0:"+str(self.bufferStartInput.get()),
                  "0:"+str(self.bufferEndInput.get()))
        #self.requests.add_request(request)
        self.availableStudents = find_available_students(self.students, request)
        print(self.availableStudents)
        #print(load_all_requests())


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
        for button in self.buttons:
            button.config(text=" "+"\n")

        for day in self.calendar.itermonthdays(self.currentYear, self.currentMonth):
            curButton = self.buttons[index]
            if self.currentMonth < 10:
                month = "0" + str(self.currentMonth)
            else:
                month = str(self.currentMonth)
            if day == 0:
                curButton.configure(text=" "+"\n")
            else:
                if day < 10:
                    curButton.configure(text=month+"/"+"0"+str(day)+"\n")
                else:
                    curButton.configure(text=month+"/"+str(day)+"\n")
            index += 1
        self.monthLabel.configure(text=self.months[self.currentMonth-1]+" "+str(self.currentYear))
