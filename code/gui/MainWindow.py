import shutil
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from tkinter import font

import os

from .Prompt import Prompt
from ..MainCalendar import MainCalendar
import calendar
from code.Requests import Requests
from code.Student import Student
from datetime import datetime


class MainWindow():
    def __init__(self, root):
        '''
        Main user interface when application is opened.
        Sets the attribute students by calling the method load_all_student() from the MainCalendar class
        args: root - Tkinter instance
        returns: None
        '''
        self.root = root
        self.root.title("ICSPS Scheduler")
        self.width = 850
        self.height = 400
        self.root.minsize(height=self.height, width=self.width)
        self.root.maxsize(height=self.height, width=self.width)
        self.months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
                                'September', 'October', 'November', 'December']
        self.currentMonth = datetime.now().month
        self.currentYear = datetime.now().year
        self.calendar = calendar.Calendar(firstweekday=6)
        self.buttons = []

        self.students = MainCalendar.load_all_student()
        self.requestWindowOpen = False
        self.promptWindowOpen = False
        self.requests = Requests()

        self.initializeUI()

    def initializeUI(self):
        '''
        Initializes all Tkinter widgets necessary for main window. Displays
        all of the requests in a calendar view using the attribute calendar and lists all of the students using
        the attribute students

        args: None
        returns: None
        '''

        if isinstance(self.students, list):
            badFiles = []
            for i in range(0,len(self.students), 2):
                badFiles.append(self.students[i])
            Prompt(self, "Incorrect Student File", "The following files are incorrectly formatted: "+", ".join(badFiles)+".\n Please correct the files and restart the program")
            return

        menu = Menu(self.root)
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
        requestLabel.grid(column=1, row=0, columnspan=2)
        requestScroll = Scrollbar(self.leftFrame, orient=VERTICAL)
        self.requestView = Listbox(self.leftFrame, height=17, width=20, selectmode=SINGLE, yscrollcommand=requestScroll.set)
        requestScroll.config(command=self.requestView.yview)
        requestScroll.grid(row=1, column=0, sticky="NS")
        self.requestView.grid(row=1, column=1, padx=5, columnspan=3)
        viewButton = ttk.Button(self.leftFrame, text="View", width=7, command=self.viewPrompt)
        viewButton.grid(row=2, column=1, sticky=E)
        editButton = ttk.Button(self.leftFrame, text="Edit", width=7, command=self.editPrompt)
        editButton.grid(row=2, column=2, sticky=W)
        createButton = ttk.Button(self.leftFrame, text="Create", width=7, command=self.createNewPrompt)
        createButton.grid(column=1, row=3, sticky=E)
        deleteButton = ttk.Button(self.leftFrame, text="Delete", width=7, command=None)
        deleteButton.grid(row=3, column=2, sticky=W)

        allRequests = MainCalendar.load_all_requests()
        for request in sorted(allRequests):
            self.requestView.insert(END, allRequests[request][-1].get_name())

        # Initalize central frame widgets
        appHighlightFont = font.Font(family='Helvetica', size=14, weight='bold')
        self.monthLabel = Label(self.centralFrame, text=self.months[self.currentMonth-1]+ " " + str(self.currentYear), font=appHighlightFont, background="gray90")
        self.monthLabel.grid(column=0, row=0, columnspan=2)
        leftButton = ttk.Button(self.centralFrame, text="<", width=5, command=self.prevMonth)
        leftButton.grid(column=5, row=8, sticky=E, pady=5)
        rightButton = ttk.Button(self.centralFrame, text=">", width=5, command=self.nextMonth)
        rightButton.grid(column=6, row=8, sticky=W, pady=5)

        days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Satuday"]
        for i in range(len(days)):
            dayLabel = Label(self.centralFrame, text=days[i], background="gray90")
            dayLabel.grid(row=1, column=i)

        for i in range(6):
            for j in range(7):
                dayButton = ttk.Button(self.centralFrame, text="\n")
                dayButton.grid(row=i+2, column=j)
                self.buttons.append(dayButton)

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
                    curButton.configure(text=month+"/"+"0"+str(day)+"\n", command=lambda day=day: self.createNewPrompt(month+"/"+"0"+str(day)))
                else:
                    curButton.configure(text=month+"/"+str(day)+"\n", command=lambda day=day: self.createNewPrompt(month+"/"+str(day)))
            index += 1

        style = ttk.Style()
        style.configure("Blue.TButton", foreground="blue")
        for button in self.buttons:
            button.configure(style="default.TButton")
            for request in MainCalendar.load_all_requests():
                if button['text'].strip()+"/"+str(self.currentYear) == request:
                    button.configure(style="Blue.TButton", command= lambda request=request: self.viewPrompt(request))


        # Initialize right frame widgets
        studentLabel = Label(self.rightFrame, text="Students", background="gray90")
        studentLabel.grid(row=0, column=0, columnspan=2)
        studentScroll = Scrollbar(self.rightFrame, orient=VERTICAL)
        self.studentView = Listbox(self.rightFrame, height=17, width=20, yscrollcommand=studentScroll.set, selectmode=SINGLE)
        studentScroll.config(command=self.studentView.yview)
        studentScroll.grid(row=1, column=2, sticky="NS")
        for student in sorted(self.students):
            self.studentView.insert(END, student)

        self.studentView.grid(row=1, column=0, padx=5, columnspan=2)
        addButton = ttk.Button(self.rightFrame, text="+", width=5, command = self.add_student)
        addButton.grid(row=2, column=0, sticky=E)
        removeButton = ttk.Button(self.rightFrame, text="-", width=5, command = (lambda: self.delete_student() if messagebox.askokcancel("Confirmation", "Do you want to delete %s?"%self.studentView.get(self.studentView.curselection())) else False))
        removeButton.grid(row=2, column=1, sticky=W)
        openButton = ttk.Button(self.rightFrame, text="Open", width=10, command=lambda: self.students[self.studentView.get(self.studentView.curselection()[0])].open_file())
        openButton.grid(column=0, columnspan=2, row=3)


        image = PhotoImage(file="icon.gif")
        logo = Label(self.rightFrame, image=image, height=50, width=50)
        logo.image = image
        logo.grid(row=4, column=1, columnspan=2, sticky=NE)

    def add_student(self):
        """
        Add a new student to the folder as well as the app.
        :return: None
        """

        file = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                        filetypes=(("csv files", "*.csv"),
                                                                   ("all files", "*.*")))
        if file != "":
            list_name = os.listdir('Students')
            file_name = file.strip().split('/')[-1]
            if file_name in list_name:
                Prompt(self, "Invalid file name", "A file with that name already exists, please choose a new name")
            else:
                student = Student(file)
                if student.get_validation():
                    del student
                    shutil.move(file, os.path.join('Students', file_name))
                    student = Student(os.path.join('Students', file_name))
                    self.students[student.get_student_name()] = student
                    self.studentView.insert(END, student.get_student_name())
                else:
                    Prompt(self, "Incorrect Format", "The format of the file is incorrect.")

    def delete_student(self):
        """
        delete the student from the folder as well as the app.
        :return: None
        """
        name = self.studentView.get(self.studentView.curselection())
        self.students[name].delete_file()
        del self.students[name]
        self.studentView.delete(self.studentView.curselection())

    def closeWindow(self):
        '''
        Closes the window prompt.
        Sets the promptWindowOpen attribute from MainWindow to false

        :return:
        '''

        self.requestWindowOpen = False
        self.prompt.destroy()

    def createNewPrompt(self, date=None):
        '''
        Creates a new window that allows the user to create a new request. Calls
        on the MainCalendar class to create a new request and updates the MainWindow attributes
        calendar data.

        :return:
        '''
        if self.requestWindowOpen:
            return

        # Initialize labels
        self.prompt = Toplevel(self.root)
        self.prompt.protocol("WM_DELETE_WINDOW", self.closeWindow)
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

        #Initalize inputs
        if date != None:
            date = date.split("/")

        self.nameInput = ttk.Entry(self.prompt, width=30)
        self.nameInput.grid(row=1, column=1, columnspan=2)
        self.monthInput = ttk.Combobox(self.prompt, width=27, state="readonly")
        months = []
        for i in range(1,13):
            if i < 10:
                months.append('0'+str(i))
            else:
                months.append(str(i))
        self.monthInput['values'] = months
        if date != None:
            self.monthInput.current(int(date[0])-1)
        self.monthInput.grid(row=2, column=1, columnspan=2)
        self.dayInput = ttk.Combobox(self.prompt, width=27, state="readonly")
        days = []
        for i in range(1, 32):
            if i < 10:
                days.append("0"+str(i))
            else:
                days.append(str(i))
        self.dayInput['values'] = days
        if date != None:
            self.dayInput.current(int(date[1])-1)
        self.dayInput.grid(row=3, column=1, columnspan=2)
        self.startHourInput = ttk.Combobox(self.prompt, width=8, state="readonly")
        self.startHourInput.grid(row=4, column=1, sticky="E")
        hours = []
        for i in range(23):
            if i < 10:
                hours.append('0'+str(i))
            else:
                hours.append(i)
        self.startHourInput['values'] = hours
        self.startMinuteInput = ttk.Combobox(self.prompt, width=8, state="readonly")
        self.startMinuteInput.grid(row=4, column=2, sticky="W")
        times = []
        for i in range(0, 60, 5):
            if i < 10:
                times.append('0'+str(i))
            else:
                times.append(str(i))
        self.startMinuteInput['values'] = times
        self.endHourInput = ttk.Combobox(self.prompt, width=8, state="readonly")
        self.endHourInput.grid(row=5, column=1, padx=(75,0))
        self.endHourInput['values'] = hours
        self.endMinuteInput = ttk.Combobox(self.prompt, width=8, state="readonly")
        self.endMinuteInput.grid(row=5, column=2, sticky="W")
        self.endMinuteInput['values'] = times
        self.bufferStartInput = ttk.Combobox(self.prompt, width=27, state="readonly")
        self.bufferStartInput.grid(row=6, column=1, columnspan=2)
        bufferList = []
        for i in range(0, 65, 5):
            if i < 10:
                bufferList.append("0"+str(i))
            else:
                bufferList.append(str(i))
        self.bufferStartInput['values'] = bufferList
        self.bufferEndInput = ttk.Combobox(self.prompt, width=27, state="readonly")
        self.bufferEndInput.grid(row=7, column=1, columnspan=2)
        self.bufferEndInput['values'] = bufferList

        #Initalize list views
        assignedLabel = ttk.Label(self.prompt, text="Assigned")
        assignedLabel.grid(row=8, column=0, pady=5)
        assignedScroll = Scrollbar(self.prompt, orient=VERTICAL)
        availableScroll = Scrollbar(self.prompt, orient=VERTICAL)
        self.assignedView = Listbox(self.prompt, width=15, height=10, selectmode=SINGLE, yscrollcommand=assignedScroll.set)
        self.assignedView.grid(row=9, column=0, padx=(5,0), pady=5, sticky="W", rowspan=2)
        assignedScroll.config(command=self.assignedView.yview)
        assignedScroll.grid(row=9, column=1, sticky="NSW", rowspan=2)
        availableLabel = ttk.Label(self.prompt, text="Available")
        availableLabel.grid(row=8, column=2, pady=5)
        self.availableView = Listbox(self.prompt, width=15, height=10, yscrollcommand=availableScroll.set, selectmode=SINGLE)
        self.availableView.grid(row=9, column=2, rowspan=2, padx=(0,5), pady=5, sticky="E")
        availableScroll.config(command=self.availableView.yview)
        availableScroll.grid(row=9, column=1, sticky="NSE", rowspan=2)

        leftButton = ttk.Button(self.prompt, text="<", command=self.assignStudent)
        leftButton.grid(row=9, column=1, sticky='S')
        rightButton = ttk.Button(self.prompt, text=">", command=self.removeStudent)
        rightButton.grid(row=10, column=1, sticky='N')

        cancelButton = ttk.Button(self.prompt, text="Cancel", command=self.closeWindow)
        cancelButton.grid(row=12, column=0, sticky="W", padx=5, pady=(0,5))
        searchButton = ttk.Button(self.prompt, text="Search", command=self.findStudents)
        searchButton.grid(row=11, column=2, sticky="E", columnspan=2, padx=5)
        confirmButton = ttk.Button(self.prompt, text="Confirm", command=self.confirmRequest)
        confirmButton.grid(row=12, column=2, sticky="E", columnspan=2, padx=5, pady=(0,5))
        self.requestWindowOpen = True

    def viewPrompt(self, request=None):
        '''
        Opens a new window to view the selected request.
        Calls on Student's check_request method to see if they
        were assigned to the specific request.

        :return:
        '''

        if self.requestWindowOpen:
            return

        if request == None:
            try:
                selectedRequest = self.requestView.get(self.requestView.curselection()[0])
            except:
                return
        else:
            selectedRequest = request

        allRequests = MainCalendar.load_all_requests()
        selectedRequest = allRequests[selectedRequest][0]
        self.prompt = Toplevel(self.root)
        self.prompt.protocol("WM_DELETE_WINDOW", self.closeWindow)
        self.prompt.minsize(width=200, height=300)
        self.prompt.maxsize(width=450, height=500)
        self.prompt.title('View Request')
        self.prompt.configure(background="gray90")
        requestName = selectedRequest.get_name()

        assignedStudents = []
        for name in self.students:
            if self.students[name].check_request(requestName):
                assignedStudents.append(name)

        padding = ttk.Label(self.prompt, text="  ")
        padding.grid(row=2, column=1, sticky="e")
        appHighlightFont = font.Font(family='Helvetica', size=18, weight='bold')
        titleLabel = ttk.Label(self.prompt, text=requestName, font=appHighlightFont)
        titleLabel.grid(row=0, column=2, columnspan=4, sticky="E", pady=40, padx=40)
        dateLabel = ttk.Label(self.prompt, text="Date:")
        dateLabel.grid(row=1, column=2, sticky="e")
        date = selectedRequest.get_date()
        dateEntry = ttk.Label(self.prompt, text=date)
        dateEntry.grid(row=1, column=3, sticky="e")
        startLabel = ttk.Label(self.prompt, text="Start Time:")
        startLabel.grid(row=2, column=2, sticky="e")
        startEntry = ttk.Label(self.prompt, text=selectedRequest.get_start_time())
        startEntry.grid(row=2, column=3, sticky="e")
        endLabel = ttk.Label(self.prompt, text="End Time:")
        endLabel.grid(row=3, column=2, sticky="e")
        endEntry = ttk.Label(self.prompt, text=selectedRequest.get_end_time())
        endEntry.grid(row=3, column=3, sticky="e")
        if len(assignedStudents) == 0:
            studentTitle = ""
        elif len(assignedStudents) == 1:
            studentTitle = "Student:"
        else:
            studentTitle = "Students:"
        studentLabel = ttk.Label(self.prompt, text=studentTitle)
        studentLabel.grid(row=4, column=2, sticky="e")
        for index in range(len(assignedStudents)):
            studentLabel = ttk.Label(self.prompt, text=assignedStudents[index])
            studentLabel.grid(row=4+index, column=3, sticky="e")
        self.requestWindowOpen = True

    def editPrompt(self):
        '''
        Opens a new window to edit the selected request.
        Gets the request data by loading all of the request from MainCalendar.

        :return:
        '''

        if self.requestWindowOpen:
            return

        selectedRequest = self.requestView.get(self.requestView.curselection()[0])

        if selectedRequest == None:
            return

        allRequests = MainCalendar.load_all_requests()
        selectedRequest = allRequests[selectedRequest][0]

        self.prompt = Toplevel(self.root)
        self.prompt.protocol("WM_DELETE_WINDOW", self.closeWindow)
        self.prompt.title("Edit Request")
        self.prompt.configure(background = "gray90")
        appHighlightFont = font.Font(family='Helvetica', size=18, weight='bold')
        titleLabel = ttk.Label(self.prompt, text="Edit Request", font=appHighlightFont)
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

        #Initalize inputs
        date = selectedRequest.get_date().split("/")
        startTime = selectedRequest.get_start_time().split(":")
        endTime = selectedRequest.get_end_time().split(":")
        bufferStart = selectedRequest.get_buffer_start().split(":")
        bufferEnd = selectedRequest.get_buffer_end().split(":")

        self.nameInput = ttk.Entry(self.prompt, width=30)
        self.nameInput.insert(0, selectedRequest.get_name())
        self.nameInput.grid(row=1, column=1, columnspan=2)
        self.monthInput = ttk.Combobox(self.prompt, width=27, state="readonly")
        months = []
        for i in range(1,13):
            if i < 10:
                months.append('0'+str(i))
            else:
                months.append(str(i))
        self.monthInput['values'] = months
        self.monthInput.current(int(date[0])-1)
        self.monthInput.grid(row=2, column=1, columnspan=2)
        self.dayInput = ttk.Combobox(self.prompt, width=27, state="readonly")
        days = []
        for i in range(1, 32):
            if i < 10:
                days.append("0"+str(i))
            else:
                days.append(str(i))
        self.dayInput['values'] = days
        self.dayInput.current(int(date[1])-1)
        self.dayInput.grid(row=3, column=1, columnspan=2)
        self.startHourInput = ttk.Combobox(self.prompt, width=8, state="readonly")
        self.startHourInput.grid(row=4, column=1, sticky="E")
        hours = []
        for i in range(23):
            if i < 10:
                hours.append('0'+str(i))
            else:
                hours.append(i)
        self.startHourInput['values'] = hours
        self.startHourInput.current(int(startTime[0])-1)
        self.startMinuteInput = ttk.Combobox(self.prompt, width=8, state="readonly")
        self.startMinuteInput.grid(row=4, column=2, sticky="W")
        times = []
        for i in range(0, 60, 5):
            if i < 10:
                times.append('0'+str(i))
            else:
                times.append(str(i))
        self.startMinuteInput['values'] = times
        self.startMinuteInput.current((int(startTime[1])-1))
        self.endHourInput = ttk.Combobox(self.prompt, width=8, state="readonly")
        self.endHourInput.grid(row=5, column=1, padx=(75,0))
        self.endHourInput['values'] = hours
        self.endHourInput.current(int(endTime[0]))
        self.endMinuteInput = ttk.Combobox(self.prompt, width=8, state="readonly")
        self.endMinuteInput.grid(row=5, column=2, sticky="W")
        self.endMinuteInput['values'] = times
        self.endMinuteInput.current(int(endTime[1])-1)
        self.bufferStartInput = ttk.Combobox(self.prompt, width=27, state="readonly")
        self.bufferStartInput.grid(row=6, column=1, columnspan=2)
        bufferList = []
        for i in range(0, 65, 5):
            if i < 10:
                bufferList.append("0"+str(i))
            else:
                bufferList.append(str(i))
        self.bufferStartInput['values'] = bufferList
        self.bufferStartInput.current(int(bufferStart[0])-1)
        self.bufferEndInput = ttk.Combobox(self.prompt, width=27, state="readonly")
        self.bufferEndInput.grid(row=7, column=1, columnspan=2)
        self.bufferEndInput['values'] = bufferList
        self.bufferEndInput.current(int(bufferEnd[0])-1)

        #Initalize list views
        assignedLabel = ttk.Label(self.prompt, text="Assigned")
        assignedLabel.grid(row=8, column=0, pady=5)
        assignedScroll = Scrollbar(self.prompt, orient=VERTICAL)
        availableScroll = Scrollbar(self.prompt, orient=VERTICAL)
        self.assignedView = Listbox(self.prompt, width=15, height=10, selectmode=SINGLE, yscrollcommand=assignedScroll.set)
        self.assignedView.grid(row=9, column=0, padx=(5,0), pady=5, sticky="W", rowspan=2)
        availableLabel = ttk.Label(self.prompt, text="Available")
        availableLabel.grid(row=8, column=2, pady=5)
        self.availableView = Listbox(self.prompt, width=15, height=10, yscrollcommand=availableScroll.set, selectmode=SINGLE)
        self.availableView.grid(row=9, column=2, rowspan=2, padx=(0,5), pady=5, sticky="E")

        leftButton = ttk.Button(self.prompt, text="<", command=self.assignStudent)
        leftButton.grid(row=9, column=1, sticky='S')
        rightButton = ttk.Button(self.prompt, text=">", command=self.removeStudent)
        rightButton.grid(row=10, column=1, sticky='N')

        cancelButton = ttk.Button(self.prompt, text="Cancel", command=self.closeWindow())
        cancelButton.grid(row=12, column=0, sticky="W", padx=5, pady=(0,5))
        searchButton = ttk.Button(self.prompt, text="Search", command=self.findStudents)
        searchButton.grid(row=11, column=2, sticky="E", columnspan=2, padx=5)
        confirmButton = ttk.Button(self.prompt, text="Confirm", command=self.confirmRequest)
        confirmButton.grid(row=12, column=2, sticky="E", columnspan=2, padx=5, pady=(0,5))
        self.requestWindowOpen = True

    def validateFields(self):
        '''
        Validates the fields in creating a new request.
        Checks if the fields are empty, if the start time is before the end time,
        if the name input is alphanumeric and is less than 40 characters. Will show prompt
        error if otherwise.
        If the buffer time is empty, it sets it to 0.

        :return: Boolean: true if all of the fields are validated and consistent with the
        requirements, false if otherwise
        '''

        # Validation for input
        if self.nameInput.get() == '':
            Prompt(self, "Invalid Input", "Please provide a name for the request")
            return False
        if len(self.nameInput.get()) > 40:
            Prompt(self, "Invalid Input", "Name of the request must be less than 40 characters")
            return False
        if not self.nameInput.get().replace(" ", "").isalnum():
            Prompt(self, "Invalid Input", "Name of the request must only have alphanumeric characters")
            return False
        if self.monthInput.get() == '':
            Prompt(self, "Invalid Input", "Please provide a month for the request")
            return False
        if self.dayInput.get() == '':
            Prompt(self, "Invalid Input", "Please provide a day for the request")
            return False
        if self.startHourInput.get() == '' or self.startMinuteInput.get() == '':
            Prompt(self, "Invalid Input", "Please fill all of the fields for the start time for the request")
            return False
        if self.endHourInput.get() == '' or self.endMinuteInput.get() == '':
            Prompt(self, "Invalid Input", "Please fill all of the fields for the end time for the request")
            return False

        # If the end time is greater than the start time
        if self.startHourInput.get() + self.startMinuteInput.get() >= self.endHourInput.get() + self.endMinuteInput.get():
            Prompt(self, "Invalid Input", "Start time must happen before the end time of the request ")
            return False

        # If it passes all validation we are going to pass the request in, and set the buffer time to 0 from start
        if self.bufferStartInput.get() == '':
            self.bufferStartInput.current(0)
        if self.bufferEndInput.get() == '':
            self.bufferEndInput.current(0)
        return True

    def findStudents(self):
        '''
        Calls on the MainCalendar class to find the students that
        are available during the times entered in the new request window.

        :return:
        '''
        if self.validateFields() == False:
            return

        self.request = self.requests.Request(self.nameInput.get(),
                  self.monthInput.get()+"/"+self.dayInput.get()+"/"+str(self.currentYear),
                  str(self.startHourInput.get())+":"+str(self.startMinuteInput.get()),
                  str(self.endHourInput.get())+":"+str(self.endMinuteInput.get()),
                  "0:"+str(self.bufferStartInput.get()),
                  "0:"+str(self.bufferEndInput.get()))

        self.availableStudents = MainCalendar.find_available_students(self.students, self.request)
        self.availableView.delete(0, END)
        for student in self.availableStudents:
            self.availableView.insert(END, student)


    def assignStudent(self):
        '''
        Moves a student from the search window to the assigned student window

        :return:
        '''
        self.assignedView.insert(END, self.availableView.get(self.availableView.curselection()[0]))
        self.availableView.delete(self.availableView.curselection()[0])

    def removeStudent(self):
        '''
        Moves a student from the assigned window to the search student window

        :return:
        '''
        self.availableView.insert(END, self.assignedView.get(self.assignedView.curselection()[0]))
        self.assignedView.delete(self.assignedView.curselection()[0])

    def confirmRequest(self):
        '''
        Confirms a request. Validates all of the field data by calling validateFields(),
        assigns the student(s) to the request by calling on the MainCalendar function
        set_student_to_request

        :return:
        '''
        if self.validateFields() == False:
            return

        self.request = self.requests.Request(self.nameInput.get(),
                  self.monthInput.get()+"/"+self.dayInput.get()+"/"+str(self.currentYear),
                  str(self.startHourInput.get())+":"+str(self.startMinuteInput.get()),
                  str(self.endHourInput.get())+":"+str(self.endMinuteInput.get()),
                  "0:"+str(self.bufferStartInput.get()),
                  "0:"+str(self.bufferEndInput.get()))

        studentSchedules = MainCalendar.load_all_student()
        self.requests.add_request(self.request)
        for student in self.assignedView.get(0, END):
            MainCalendar.set_student_to_request(studentSchedules[student], self.request)
        self.closeWindow()
        self.updateCalendar()

    def nextMonth(self):
        '''
        Calculates the next month from currentMonth and
        displays it by updating the calendar view calling updateCalendar()

        :return:
        '''
        if self.currentMonth == 12:
            self.currentMonth = 1
            self.currentYear += 1
        else:
            self.currentMonth += 1
        self.updateCalendar()

    def prevMonth(self):
        '''
        Calculates the previous month from currentMonth and
        displays it by updating the calendar view calling updateCalendar()

        :return:
        '''
        if self.currentMonth == 1:
            self.currentMonth = 12
            self.currentYear -=1
        else:
            self.currentMonth -= 1
        self.updateCalendar()

    def updateCalendar(self):
        '''
        Updates the calendar view with the requests and
        the attributes in MainWindow.

        :return:
        '''
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
                    curButton.configure(text=month+"/"+"0"+str(day)+"\n", command=lambda day=day: self.createNewPrompt(month+"/"+"0"+str(day)))
                else:
                    curButton.configure(text=month+"/"+str(day)+"\n", command=lambda day=day: self.createNewPrompt(month+"/"+str(day)))
            index += 1

        style = ttk.Style()
        style.configure("Blue.TButton", foreground="blue")
        for button in self.buttons:
            button.configure(style="default.TButton")
            for request in MainCalendar.load_all_requests():
                if button['text'].strip()+"/"+str(self.currentYear) == request:
                    button.configure(style="Blue.TButton", command= lambda request=request: self.viewPrompt(request))

        self.monthLabel.configure(text=self.months[self.currentMonth-1]+" "+str(self.currentYear))
