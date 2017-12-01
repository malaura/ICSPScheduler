import calendar
import csv
import os
import shutil

from intervaltree import IntervalTree
import datetime

from code.Requests import Requests
from code.Student import Student

class MainCalendar():
    @staticmethod
    def load_csv_files_in_directory(directory):
        """
        Loads all of the csv files in a current directory. The default directory is Students
        Calls student object

        :param directory: os directory
        :return: dictionary - key is string name, value is student objects (that were loaded successfully)
                 list of lists - file names that were not loaded successfully
        ex.
            [[MariaRodriguez.csv, 'Date wasn't in the correct format'], [Jim.csv, 'Munday is not a day of the week']]
        """
        list_name = os.listdir(directory)
        dictionary = {}
        list_of_wrong_name = []
        for name in list_name:
            if not name.startswith('.'):
                directory_of_one_student = os.path.join('Students', name)
                student_name = name[:-4]
                student = Student(directory_of_one_student)
                if student.get_validation():
                    dictionary[student_name] = student
                else:
                    list_of_wrong_name.append(name)
                    list_of_wrong_name.append(student.get_validation_info())

        if len(list_of_wrong_name) != 0:
            return list_of_wrong_name
        else:
            return dictionary

    @staticmethod
    def load_all_student():
        """
        Loads all of the students from a directory

        # Calls on:
        #load_csv_file
        #create_student

        :return: dictionary of students objects
        """
        students = MainCalendar.load_csv_files_in_directory('Students')
        return students

    @staticmethod
    def find_available_students(students, request):
        """
        Finds the available student for a specific time.
        Uses the dictionary_of_time_interval to find if the specific time interval time is
        available for the student.

        :param request - request object
        :param students - dictionary of student objects
        :return: list of student object: list of all available students
        """
        lis = []
        date = request.get_date()
        mon, day, year = request.get_date().split('/')
        weekly_date = calendar.day_name[datetime.datetime(int(year), int(mon), int(day)).weekday()]
        for student in students.keys():
            if date in students[student].get_dictionary_of_time_interval():
                interval = students[student].get_dictionary_of_time_interval()[date]
                if interval[request.get_actual_start_time():request.get_actual_end_time()] == set():
                    if weekly_date in students[student].get_dictionary_of_time_interval():
                        interval = students[student].get_dictionary_of_time_interval()[weekly_date]
                        if interval[request.get_actual_start_time():request.get_actual_end_time()] == set():
                            lis.append(student)
                    else:
                        lis.append(student)
            else:
                if weekly_date in students[student].get_dictionary_of_time_interval():
                    interval = students[student].get_dictionary_of_time_interval()[weekly_date]
                    if interval[request.get_actual_start_time():request.get_actual_end_time()] == set():
                        lis.append(student)
                else:
                    lis.append(student)

        return lis

    @staticmethod
    def set_student_to_request(student, request):
        """
        Sets a student to a request by callind the add_request method in student.

        :param request - request object: request to be assigned
        :param student - student object: the student who is going to have the request
        :return: None
        """

        student.add_request(request)
        return

    @staticmethod
    def load_all_requests():
        """
        Loads all of the requests in dictionary format.

        :return: dictionary of request objects
        """

        requests = Requests()
        return requests.get_dictionary()

    @staticmethod
    def find_assigned_student(students, request):
        """
        Finds the assigned students for a particular request.
        Calls on the student's method check_request.

        :param students - dictionary of student objects
        :param request - request object
        :return: list of strings: the names of the assigned students
        """
        lis = []
        for student in students:
            if student.check_request(request.get_name()):
                lis.append(student.get_student_name())

        return lis