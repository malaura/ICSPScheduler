import csv
import os
import shutil
import sys
from datetime import datetime

from intervaltree import IntervalTree, Interval


class Student:
    def __init__(self, directory):
        '''
        name - students name
        directory - the directory of the student's schedule
        dictionary_of_schedule - student's schedule
        dictionary_of_time_interval - student's available times
        validation - specifies if the student's schedule is in the correct format
        validation_info - specifies detailed information on student's schedule
        fieldnames - headers of the student's schedule
        '''
        self.directory = directory
        self.dictionary_of_schedule = {}
        self.dictionary_of_time_interval = {}
        self.name = os.path.split(directory)[1].split('.')[0]
        self.validation, self.validation_info = self.csv_file_format_validator()
        self.fieldnames = ['Date', 'Start', 'End', 'Information']
        if self.validation:
            self.load()

    def open_file(self):
        """
        Open file with default application
        :return: None
        """
        if sys.platform == 'darwin':
            os.system("open " + self.directory)
        else:
            os.system("start " + self.directory)

    def load(self):
        """
        Gets the csv file corresponding to the student schedule and loads
        the information to the dictionary_of_schedule
        """

        with open(self.directory, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for line in csv_reader:
                lis = [line['Start'], line['End'], line['Information']]
                if line['Date'] not in ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
                                        'Saturday', 'Sunday'):
                    try:
                        date_obj = datetime.strptime(line['Date'], '%m/%d/%y')
                        line['Date'] = datetime.strftime(date_obj, '%m/%d/%Y')
                    except:
                        pass
                try:
                    self.dictionary_of_schedule['%s' % line['Date']].append(lis)
                except:
                    self.dictionary_of_schedule['%s' % line['Date']] = []
                    self.dictionary_of_schedule['%s' % line['Date']].append(lis)

        for key in self.dictionary_of_schedule:
            self.dictionary_of_time_interval[key] = IntervalTree()
            for event in self.dictionary_of_schedule[key]:
                start = float(event[0].replace(':', '.'))
                end = float(event[1].replace(':', '.'))
                self.dictionary_of_time_interval[key][start:end] = True

    def get_directory(self):
        '''
        Getter for the student's schedule file directory

        :return: dictionary
        '''
        return self.directory

    def get_validation_info(self):
        '''
        Getter for the validation info of the student

        :return: validation_info - string
        '''
        return self.validation_info

    def get_validation(self):
        '''
        Getter for validation of the student

        :return: validation - boolean
        '''
        return self.validation

    def get_dictionary_of_schedule(self):
        '''
        Getter for the dictionary of schedule of the student

        :return: dictionary_of_schedule - dictionary
        '''
        return self.dictionary_of_schedule

    def get_dictionary_of_time_interval(self):
        '''
        Getter for the dictionary of time interval of the student

        :return: dictionary_of_time_interval - dictionary
        '''
        return self.dictionary_of_time_interval

    def get_student_name(self):
        '''
        Getter for the student name

        :return: name - string
        '''
        return self.name

    def edit_file(self):
        """
        Opens the student's schedule with the default application

        :return: None
        """
        os.system('open ./%s' % self.directory)

    def delete_file(self):
        """
        Deletes the student's schedule file from the directory

        :return: None
        """
        os.remove(self.directory)

    def add_request(self, request):
        """
        Adds a request to Student's calendar. Sets the time as unavailable in the dictionary_of_schedule
        and dictionary_of_time_interval.

        :param request: request object
        :return: None
        """

        with open(self.directory, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            with open(os.path.join('Students', 'temp.csv'), 'w', newline='') as new_file:
                csv_writer = csv.DictWriter(new_file, fieldnames=self.fieldnames, delimiter=',')
                csv_writer.writeheader()
                for line in csv_reader:
                    csv_writer.writerow(line)
                requests = {'Information': request.get_name(), 'Start': request.get_start_time(),
                           'End': request.get_end_time(), 'Date': request.get_date()}
                csv_writer.writerow(requests)

        shutil.move(os.path.join('Students', 'temp.csv'), self.directory)
        # dictionary_of_schedule
        lis = [request.get_start_time(), request.get_end_time(), request.get_name()]
        try:
            self.dictionary_of_schedule[request.get_date()].append(lis)
        except:
            self.dictionary_of_schedule[request.get_date()] = []
            self.dictionary_of_schedule[request.get_date()].append(lis)

        # dictionary_of_time_interval
        try:
            self.dictionary_of_time_interval[request.get_date()][float(request.get_start_time().replace(':','.')):float(request.get_end_time().replace(':','.'))] = True
        except:
            self.dictionary_of_time_interval[request.get_date()]= IntervalTree()
            self.dictionary_of_time_interval[request.get_date()][
            float(request.get_start_time().replace(':', '.')):float(request.get_end_time().replace(':', '.'))] = True


    def check_request(self, name):
        """
        Checks if the request is assigned to this student

        :param name: the request's name
        :return: True if the request is assigned to this student, otherwise False.
        """
        with open(self.directory, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for line in csv_reader:
                if line['Information'] == name:
                    return True
        return False

    def delete_request(self, request):
        """
        Deletes a request from the student's calendar

        :param request: request object
        :return: None
        """
        with open(self.directory, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            with open(os.path.join('Students', 'temp.csv'), 'w', newline='') as new_file:
                csv_writer = csv.DictWriter(new_file, fieldnames=self.fieldnames, delimiter=',')
                csv_writer.writeheader()
                old_request = {'Information': request.get_name(), 'Start': request.get_start_time(),
                           'End': request.get_end_time(), 'Date': request.get_date()}
                for line in csv_reader:
                    if line != old_request:
                        csv_writer.writerow(line)

        shutil.move(os.path.join('Students', 'temp.csv'), self.directory)
        self.load()

    def csv_file_format_validator(self):
        """
        Validates if csv file is in the correct standard format for our schedule.
        Check the wiki to see what is the current format we are accepting.

        :return: boolean - true if the file is in the successful format, false if otherwise
                 list - first index file name, second index is string that specifies the first error it encountered

        ex.
            False, [MariaRodriguez.csv, 'Date wasn't in the correct format']
        """

        with open(self.directory, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            headers = next(csv_reader)
            if headers[0] != 'Date' and headers[1] != 'Start' and headers[2] != 'End' and headers[3] != 'Information':
                return False
            for i in csv_reader:
                if not self.validate_date(i[0]):
                    return False, "Date Date wasn't in the correct format"
                if not self.validate_start_or_end(i[1]):
                    return False, "Start date wasn't in the correct format"
                if not self.validate_start_or_end(i[2]):
                    return False, "End date wasn't in the correct format"
        return True, "Format is correct"

    @staticmethod
    def validate_date(date_text):
        """
        Method to validate the date field is in the correct format. Accepts mm/dd/yy or a day of the week
        (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday)

        :param date_text - string
        :return: boolean - true if it is in the correct format false if otherwise
        """
        try:
            datetime.strptime(date_text, '%m/%d/%Y')
        except ValueError:
            try:
                datetime.strptime(date_text, '%m/%d/%y')
            except ValueError:
                if (date_text == 'Monday' or date_text == 'Tuesday' or date_text == 'Wednesday' or date_text == 'Thursday'
                        or date_text == 'Friday' or date_text == 'Saturday' or date_text == 'Sunday'):
                    return True
                else:
                    return False
        return True

    @staticmethod
    def validate_start_or_end(text):
        """
        Method to validate the start or end time format of a request.
        Time should be between 00:00 and 23:59.

        :param text - string: time
        :return: boolean - true if it is valid false if otherwise
        """
        try:
            hour, minute = text.split(':')
            if len(hour) != 2 and len(minute) != 2:
                return False
            if int(hour) < 0 or int(hour) > 23:
                return False
            if int(minute) < 0 or int(minute) > 59:
                return False
        except:
            return False
        return True
