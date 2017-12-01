import csv
import os
import shutil
from stat import S_IREAD, S_IRGRP, S_IROTH, S_IWUSR


class Requests:
    class Request:
        def __init__(self, name, date, start_time, end_time, buffer_start, buffer_end):
            '''
            name - request's name
            date - date of request
            start_time - start time of request
            end_time - end time of request
            buffer_start - extra time added before request
            buffer_end - extra time added after request
            actual_start_time - actual start time of request after adding buffer times
            actual_end_time - actual end time of request after adding buffer times
            '''
            self.name = name
            self.date = date
            self.start_time = start_time
            self.end_time = end_time
            self.buffer_start = buffer_start
            self.buffer_end = buffer_end
            minute = int(start_time.split(':')[1]) + int(buffer_start.split(':')[1])
            if minute > 60:
                minute -= 60
                hour = int(start_time.split(':')[0]) + int(buffer_start.split(':')[0]) + 1
            else:
                hour = int(start_time.split(':')[0]) + int(buffer_start.split(':')[0])
            self.actual_start_time = float('%s.%s' % (hour, minute))
            minute = int(end_time.split(':')[1]) + int(buffer_end.split(':')[1])
            if minute > 60:
                minute -= 60
                hour = int(end_time.split(':')[0]) + int(buffer_end.split(':')[0]) + 1
            else:
                hour = int(end_time.split(':')[0]) + int(buffer_end.split(':')[0])
            self.actual_end_time = float('%s.%s' % (hour, minute))

        def get_name(self):
            '''
            Getter for the request's name

            :return: name - string
            '''
            return self.name

        def get_date(self):
            '''
            Getter for the request's date

            :return: date - string
            '''
            return self.date

        def get_start_time(self):
            '''
            Getter for the request's start time

            :return: start_time - string
            '''
            return self.start_time

        def get_end_time(self):
            '''
            Getter for the request's end time

            :return: end_time - string
            '''
            return self.end_time

        def get_buffer_start(self):
            '''
            Getter for the request's buffer start time

            :return: start_time - string
            '''
            return self.buffer_start

        def get_buffer_end(self):
            '''
            Getter for the request's buffer end time

            :return: end_time - string
            '''
            return self.buffer_end

        def get_actual_start_time(self):
            '''
            Getter for the request's actual start time

            :return: actual_start_time - float
            '''
            return self.actual_start_time

        def get_actual_end_time(self):
            '''
            Getter for the request's actual end time

            :return: actual_end_time - float
            '''
            return self.actual_end_time

    def __init__(self):
        '''
        dictionary: contains all of the requests information
        '''

        self.dictionary = {}
        self.lis_of_duplicate_request = []
        if not os.path.exists('requests.csv'):
            with open('requests.csv', 'w', newline='') as new_file:
                fieldnames = ['name', 'date', 'start_time', 'end_time', 'buffer_start', 'buffer_end']
                csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames, delimiter=',')
                csv_writer.writeheader()
        else:
            with open('requests.csv', 'r') as csv_file:
                self.csv_reader = csv.DictReader(csv_file)
                for line in self.csv_reader:
                    request = Requests.Request(line['name'], line['date'], line['start_time'], line['end_time'],
                                               line['buffer_start'], line['buffer_end'])
                    if '%s' % line['date'] in self.dictionary:
                        self.lis_of_duplicate_request.append(self.dictionary['%s' % line['date']][0])
                    self.dictionary['%s' % line['date']] = []
                    self.dictionary['%s' % line['date']].append(request)
        os.chmod('requests.csv', S_IREAD|S_IRGRP|S_IROTH)
        for request in self.lis_of_duplicate_request:
            self.delete_request(request)

    def check_duplicate(self):
        """
        check if there are some requests in the same day.
        :param csv_reader: DictReader
        :return: True if the no duplicate happens, False if duplicate happens.
        """

        if len(self.lis_of_duplicate_request) == 0:
            return True,'Format is correct'
        else:
            return False, 'There are requests in the same day!'

    def add_request(self, request):
        """
        Adds request to requests.csv and dictionary

        :param request: object request
        :return: None
        """
        os.chmod('requests.csv', S_IWUSR | S_IREAD)
        with open('requests.csv', 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)

            with open('requests_new.csv', 'w', newline='') as new_file:
                fieldnames = ['name', 'date', 'start_time', 'end_time', 'buffer_start', 'buffer_end']
                csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames, delimiter=',')
                csv_writer.writeheader()

                for line in csv_reader:
                    csv_writer.writerow(line)

                csv_writer.writerow({'buffer_end': request.get_buffer_end(), 'start_time': request.get_start_time(),
                                     'date': request.get_date(), 'name': request.get_name(),
                                     'end_time': request.get_end_time(), 'buffer_start': request.get_buffer_start()})

        shutil.move('requests_new.csv', 'requests.csv')

        try:
            self.dictionary[request.get_date()].append(request)
        except:
            self.dictionary[request.get_date()] = []
            self.dictionary[request.get_date()].append(request)
        os.chmod('requests.csv', S_IREAD | S_IRGRP | S_IROTH)

    def delete_request(self, request):
        """
        Deletes a  request from requests.csv and dictionary

        :param request: object request
        :return: None
        """
        os.chmod('requests.csv', S_IWUSR | S_IREAD)
        with open('requests.csv', 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)

            with open('requests_new.csv', 'w', newline='') as new_file:
                fieldnames = ['name', 'date', 'start_time', 'end_time', 'buffer_start', 'buffer_end']
                csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames, delimiter=',')
                csv_writer.writeheader()

                for line in csv_reader:
                    if not line == {'buffer_end': request.get_buffer_end(), 'start_time': request.get_start_time(),
                                     'date': request.get_date(), 'name': request.get_name(),
                                     'end_time': request.get_end_time(), 'buffer_start': request.get_buffer_start()}:
                        csv_writer.writerow(line)

        shutil.move('requests_new.csv', 'requests.csv')
        date = request.get_date()
        try:
            self.dictionary[date].remove(request)
        except:
            pass

        if not self.dictionary[date]:
            del self.dictionary[date]
        os.chmod('requests.csv', S_IREAD | S_IRGRP | S_IROTH)

    def get_dictionary(self):
        '''
        Getter for a requests' dictionary

        :return: dictionary - dictionary
        '''
        return self.dictionary
