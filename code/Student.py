import csv
import os
import shutil
from datetime import datetime


class Student:
    def __init__(self, directory):
        self.directory = directory
        self.dictionary = {}
        self.name = directory.split('/')[1].split('.')[0]
        self.validation, self.validation_info = self.csv_file_format_validator()
        self.fieldnames = ['Date', 'Start', 'End', 'Information']
        self.csv_file_format_validator()
        if self.validation:
            self.load()

    def load(self):
        """
        :return: a dictionary that contains information of the student
        """

        with open(self.directory, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for line in csv_reader:
                self.dictionary['%s' % line['Date']] = []
                self.dictionary['%s' % line['Date']].append(line['Start'])
                self.dictionary['%s' % line['Date']].append(line['End'])
                self.dictionary['%s' % line['Date']].append(line['Information'])

    def get_directory(self):
        return self.directory

    def get_validation_info(self):
        return self.validation_info

    def get_validation(self):
        return self.validation

    def get_dictionary(self):
        return self.dictionary

    def get_student_name(self):
        return self.name

    def edit_file(self):
        """
        open the file with the default application
        :return: None
        """
        os.system('open ./%s' % self.directory)

    def delete_file(self):
        """
        delete the file
        :return: None
        """
        os.remove(self.directory)

    def add_request(self, date, start, end, info):
        """
        add a request to Student's calendar
        :param date: request's date
        :param start: request's date
        :param end: request's date
        :param info: request's date
        :return: None
        """

        with open(self.directory, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            with open(os.path.join('Students', 'temp.csv'), 'w') as new_file:
                csv_writer = csv.DictWriter(new_file, fieldnames=self.fieldnames, delimiter=',')
                csv_writer.writeheader()
                for line in csv_reader:
                    csv_writer.writerow(line)
                request = {'Information': info, 'Start': start, 'End': end, 'Date': date}
                csv_writer.writerow(request)

        shutil.move(os.path.join('Students', 'temp.csv'), self.directory)

    def delete_request(self, date, start, end, info):
        """
        delete the request from the calendar
        :param date: request's date
        :param start: request's date
        :param end: request's date
        :param info: request's date
        :return: None
        """
        with open(self.directory, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            with open(os.path.join('Students', 'temp.csv'), 'w') as new_file:
                csv_writer = csv.DictWriter(new_file, fieldnames=self.fieldnames, delimiter=',')
                csv_writer.writeheader()
                request = {'Information': info, 'Start': start, 'End': end, 'Date': date}
                for line in csv_reader:
                    if line != request:
                        csv_writer.writerow(line)

        shutil.move(os.path.join('Students', 'temp.csv'), self.directory)

    def csv_file_format_validator(self):
        """
        Validates if csv file is in the correct standard format.

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
        method to validate the date
        :param date_text:
        :return:
        """
        try:
            datetime.strptime(date_text, '%d/%m/%Y')
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
        method to validate the start or end format
        :param text:
        :return:
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
