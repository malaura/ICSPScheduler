'''
Back End
'''
import os

from code.Student import Student


def load_csv_files_in_directory(directory):
    '''
    Loads all of the csv files in a current directory.
    Calls student object

    :param directory: os directory
    :return: dictionary - key is string name, value is student objects (that were loaded successfully)
             list of lists - file names that were not loaded successfully
    ex.
        [[MariaRodriguez.csv, 'Date wasn't in the correct format'], [Jim.csv, 'Munday is not a day of the week']]
    '''
    list_name = os.listdir(directory)
    dictionary = {}
    list_of_wrong_name = []
    for name in list_name:
        directory_of_one_student = os.path.join('Students', name)
        print(directory_of_one_student)
        student_name = name[:3]
        print('ready')
        student = Student(directory_of_one_student)
        # print(dictionary[student_name.load())
        if student.get_validation():
            dictionary[student_name] = student
        else:
            list_of_wrong_name.append(name)

    if len(list_of_wrong_name) != 0:
        return list_of_wrong_name
    else:
        return dictionary

def update_csv_file(filename):
    '''
    Updates a csv file in the directory

    :param filename: string with the file name
    :return: boolean: true if it was successful, false if it wasn't
             string: specifies the error encountered, empty if no error

    ex.
        False, 'file MariaRodriguez.csv not found in the directory'
        True, ''
    '''
    return

#Add button
def add_csv_file_to_directory(filename):
    '''
    Creates a csv file schedule in the directory for a new student

    :param filename: string with the file name
    :return:    boolean: true if it was successful, false if it wasn't
                string: if boolean is true, string corresponding to csv file created, if false error encountered

    ex.
        True, 'MariaRodriguez.csv'
        False, 'MariaRodriguez.csv is already in the directory'
    '''
    return

#Don't want to do this right now
def rename_csv_file(originalName, newName):
    '''
    Replaces csv file name with originalName with newName

    :param originalName: original file name in the directory
    :param newName:  new file name in the directory
    :return: boolean: true if it was successful, false if it wasn't
             string: if boolean is true, string corresponding to new csv file name, if false error encountered

    ex.
        True, 'MariaMoreno.csv'
        False, 'MariaRodriguez.csv is not in the directory'
    '''
    return


def delete_csv_file(fileName):
    '''
    Delete csv file schedule in the directory

    :param filename: string with the file name
    :return: boolean: true if it was successful, false if it wasn't
             string: if boolean is true, string is empty, if false error encountered

    ex.
        True, ''
        False, 'MariaRodriguez.csv is not in the directory'
    '''
    return

def create_student(filename = None):
    '''
    Creates a student object. Validates if all of the data is correct if passed in a file name.
    # import csv file
    # Calls on csv_file_format_validator to validate filename
    # Calls on create_calendar to create calendar for the student

    :param filename: csv file name of student's schedule
    :return:   boolean: true if it was successful, false if it wasn't
               student object: student object creating
               string: what is the error occurred

    ex.
        True, <student object>
        False, 'MariaRodriguez.csv is already in the directory'
    '''
    student = Student(filename)
    return

def update_student(filename, student):
    '''
    Updates a student object. Validates if all of the data is correct if passed in a file name.

    # Calls on create_calendar to create calendar for the student

    :param filename: csv file name of student's schedule
    :return:   boolean: true if it was successful, false if it wasn't
               student object: student object creating
               string: what is the error occurred

    ex.
        True, <student object>
        False, 'MariaRodriguez.csv is already in the directory'
    '''
    return

def delete_student(student):
    '''
    Deletes a student object. Validates if all of the data is correct if passed in a file name.

    # Calls on delete_csv_file

    :param student: student object
    :return: boolean: true
             optional string: if false, returns the error encountered

    ex.
        True
        False, 'MariaRodriguez.csv is not in the directory'
    '''
    return

def create_calendar(filename):
    '''
    Takes in a csv file that is already in the correct format, and returns a dictionary that represents a calendar.

    :param filename: csv filename with schedule
    :return: dictionary: The key is a date
                        value is interval tree object.
             dictionary: Monday, Tuesday, Wednesday ... keys
    '''

    return

'''
MainCalendar Class


Students: dictionary with name as the key and the value as student object
Calendar: dictionary containing a calendar schedule

'''




def load_all_student():
    '''
    Loads all of the students from a directory

    # Calls on:
    #load_csv_file
    #create_student

    :return:
    '''

def find_available_students(students, startTime, endTime, bufferStart, bufferEnd):
    '''

    :param students:
    :param startTime:
    :param endTime:
    :param bufferStart:
    :param bufferEnd:
    :return:
    '''


def set_student_to_request():

    return

load_csv_files_in_directory('Students')