
import csv
import os
import shutil

class Student:



    def __init__(self, directory):
        self.directory = directory
        self.dictionary = {}
        self.name = directory.split('/')[1].split('.')[0]
        self.validation = True
        self.fieldnames = ['Date', 'Start', 'End', 'Information']
        self.csv_file_format_validator()
        self.load()

    def load(self):
        '''
        :return: a dictionary that contains information of the student
        '''

        with open(self.directory, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for line in csv_reader:
                self.dictionary['%s'%line['Date']] = []
                self.dictionary['%s' % line['Date']].append(line['Start'])
                self.dictionary['%s' % line['Date']].append(line['End'])
                self.dictionary['%s' % line['Date']].append(line['Information'])

        #print(self.dictionary)
        #print(list(self.dictionary.keys())[0])

    def get_validation(self):
        return self.validation

    def get_dictionary(self):
        return self.dictionary

    def get_student_name(self):
        return self.name

    def edit_file(self):
        '''
        open the file with the default application
        :return: None
        '''
        os.system('open ./%s'%self.directory)

    def delete_file(self):
        '''
        delete the file
        :return: None
        '''
        os.remove(self.directory)

    def add_request(self, date, start, end, info):
        '''
        add a request to Student's calendar
        :param date: request's date
        :param start: request's date
        :param end: request's date
        :param info: request's date
        :return: None
        '''

        with open(self.directory, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            with open(os.path.join('Students', 'temp.csv'), 'w') as new_file:
                csv_writer = csv.DictWriter(new_file, fieldnames= self.fieldnames, delimiter=',')
                csv_writer.writeheader()
                for line in csv_reader:
                    csv_writer.writerow(line)
                request  = {}
                request['Information'] = info
                request['Start'] = start
                request['End'] = end
                request['Date'] = date
                csv_writer.writerow(request)

        shutil.move(os.path.join('Students', 'temp.csv'),self.directory)

    def delete_request(self,date, start, end, info):
        '''
        delete the request from the calendar
        :param date: request's date
        :param start: request's date
        :param end: request's date
        :param info: request's date
        :return: None
        '''
        with open(self.directory, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            with open(os.path.join('Students', 'temp.csv'), 'w') as new_file:
                csv_writer = csv.DictWriter(new_file, fieldnames= self.fieldnames, delimiter=',')
                csv_writer.writeheader()
                request = {}
                request['Information'] = info
                request['Start'] = start
                request['End'] = end
                request['Date'] = date
                for line in csv_reader:
                    if line != request:
                        csv_writer.writerow(line)

        shutil.move(os.path.join('Students', 'temp.csv'),self.directory)

    def csv_file_format_validator(self):
        '''
        Validates if csv file is in the correct standard format.

        :return: boolean - true if the file is in the successful format, false if otherwise
                 list - first index file name, second index is string that specifies the first error it encountered

        ex.
            False, [MariaRodriguez.csv, 'Date wasn't in the correct format']
        '''

        with open(self.directory, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            headers = next(csv_reader)
            if headers[0] != 'Date' and headers[1] != 'Start' and headers[2] != 'End' and headers[3] != 'Information':
                return False
            for i in csv_reader:
                print(i)
        return True



#s = Student('Jim')
#s.add_request('Saturday','14:44','16:00','Coding')
#s.delete_request('Saturday','14:44','16:00','Coding')
#s.edit_file()



