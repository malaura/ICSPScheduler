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
            directory_of_one_student = os.path.join('Students', name)
            print(directory_of_one_student)
            student_name = name[:3]
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


    def update_csv_file(self, filename):
        """
        Updates a csv file in the directory

        :param filename: string with the file name
        :return: boolean: true if it was successful, false if it wasn't
                 string: specifies the error encountered, empty if no error

        ex.
            False, 'file MariaRodriguez.csv not found in the directory'
            True, 'update succeeded'
        """
        directory_of_one_student = os.path.join('Students', filename)
        if os.system('open ./%s' % directory_of_one_student) != 0:
            return False, 'file %s not found in the directory' % filename
        else:
            return True, 'update succeeded'


    # Add button
    def add_csv_file_to_directory(self, filename):
        """
        Creates a csv file schedule in the directory for a new student

        :param filename: string with the file name
        :return:    boolean: true if it was successful, false if it wasn't
                    string: if boolean is true, string corresponding to csv file created, if false error encountered

        ex.
            True, 'MariaRodriguez.csv'
            False, 'MariaRodriguez.csv is already in the directory'
        """
        directory_of_one_student = os.path.join('Students', filename)
        if os.path.exists(directory_of_one_student):
            return False, '%s is already in the directory' % filename
        else:
            with open(directory_of_one_student, 'w') as new_file:
                fieldnames = ['Date', 'Start', 'End', 'Information']
                csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames, delimiter=',')
                csv_writer.writeheader()
        return True, '%s has been added' % filename


    # Don't want to do this right now
    def rename_csv_file(self, original_name, new_name):
        """
        Replaces csv file name with originalName with newName

        :param original_name: original file name in the directory
        :param new_name:  new file name in the directory
        :return: boolean: true if it was successful, false if it wasn't
                 string: if boolean is true, string corresponding to new csv file name, if false error encountered

        ex.
            True, 'MariaMoreno.csv'
            False, 'MariaRodriguez.csv is not in the directory'
        """
        directory_of_new_name = os.path.join('Students', new_name)
        directory_of_original_name = os.path.join('Students', original_name)
        if os.path.exists(directory_of_new_name):
            return False, '%s is already in the directory' % new_name
        if not os.path.exists(directory_of_original_name):
            return False, '%s is not in the directory' % directory_of_original_name
        shutil.move(directory_of_original_name, directory_of_new_name)
        os.remove(directory_of_original_name)
        return True, '%s is created' % new_name


    def delete_csv_file(self, file_name):
        """
        Delete csv file schedule in the directory

        :param filename: string with the file name
        :return: boolean: true if it was successful, false if it wasn't
                 string: if boolean is true, string is empty, if false error encountered

        ex.
            True, ''
            False, 'MariaRodriguez.csv is not in the directory'
        """
        directory_of_file_name = os.path.join('Students', file_name)
        if os.path.exists(directory_of_file_name):
            os.remove(directory_of_file_name)
            return True, 'Delete succeed'
        else:
            return False, '%s is not in the directory' % file_name


    def create_student(self, file_name=None):
        """
        Creates a student object. Validates if all of the data is correct if passed in a file name.
        # import csv file
        # Calls on csv_file_format_validator to validate filename
        # Calls on create_calendar to create calendar for the student

        :param file_name: csv file name of student's schedule
        :return:   boolean: true if it was successful, false if it wasn't
                   student object: student object creating
                   string: what is the error occurred

        ex.
            True, <student object>
            False, 'MariaRodriguez.csv is already in the directory'
        """
        list_name = os.listdir('Students')
        for name in list_name:
            if file_name == name:
                return False, '%s is already in the directory' % file_name
        directory_of_the_student = os.path.join('Students', file_name)
        student = Student(directory_of_the_student)
        return True, student


    def update_student(self, file_name, student):
        """
        Updates a student object. Validates if all of the data is correct if passed in a file name.

        # Calls on create_calendar to create calendar for the student

        :param filename: csv file name of student's schedule
        :return:   boolean: true if it was successful, false if it wasn't
                   student object: student object creating
                   string: what is the error occurred

        ex.
            True, <student object>
            False, 'MariaRodriguez.csv is already in the directory'
        """
        list_name = os.listdir('Students')
        for name in list_name:
            if file_name == name:
                return False, '%s is already in the directory' % file_name
        directory_of_file_name = os.path.join('Students', file_name)
        student = Student(directory_of_file_name)
        return True, student


    def delete_student(self, student):
        """
        Deletes a student object. Validates if all of the data is correct if passed in a file name.

        # Calls on delete_csv_file

        :param student: student object
        :return: boolean: true
                 optional string: if false, returns the error encountered

        ex.
            True, 'delete succeed'
            False, 'MariaRodriguez.csv is not in the directory'
        """
        directory_of_file_name = student.get_directory()
        if os.path.exists(directory_of_file_name):
            os.remove(directory_of_file_name)
            name = student.get_student_name()
            del student
            return True, '%s delete succeed' % name
        else:
            return False, '%s is not in the directory' % student.get_directory()


    def create_calendar(self, student):
        """
        Takes in a csv file that is already in the correct format, and returns a dictionary that represents a calendar.

        :param student: student object
        :return: dictionary: The key is a date
                            value is interval tree object.
                 dictionary: Monday, Tuesday, Wednesday ... keys
        """

        return student.get_dictionary_of_time_interval()

    @staticmethod
    def load_all_student():
        """
        Loads all of the students from a directory

        # Calls on:
        #load_csv_file
        #create_student

        :return: dictionary of students
        """
        students = MainCalendar.load_csv_files_in_directory('Students')
        # students['Jim'].get_dictionary_of_schedule()  # to get students' schedule list
        # students['Jim'].get_dictionary_of_time_interval()  # to get students' time interval object
        return students

    @staticmethod
    def find_available_students(students, request):
        """
        find the available student for a specific time
        :param request: object request
        :param students: dictionary that contains all the students
        :return: list of all available students
        """
        lis = []
        date = request.get_date()
        mon, day, year = request.get_date().split('/')
        weekly_date = calendar.day_name[datetime.datetime(int(year), int(mon), int(day)).weekday()]
        print(weekly_date)
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


    def set_student_to_request(self, student, request):
        """

        :param request: object request
        :param student: the student who is going to have the request
        :return: None
        """

        student.add_request(request)
        return

    def delete_request_from_student(self, student, request):
        """

        :param request: object request
        :param student: the student who is going to have the request
        :return: None
        """

        student.delete_request(request)

    @staticmethod
    def load_all_requests():
        """

        :return: dictionary of requests
        """

        requests = Requests()
        return requests.get_dictionary()

