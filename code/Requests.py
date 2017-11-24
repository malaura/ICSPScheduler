import csv
import os
import shutil


class Requests:
    class Request:
        def __init__(self, name, date, start_time, end_time, buffer_start, buffer_end):
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
            return self.name

        def get_date(self):
            return self.date

        def get_start_time(self):
            return self.start_time

        def get_end_time(self):
            return self.end_time

        def get_buffer_start(self):
            return self.buffer_start

        def get_buffer_end(self):
            return self.buffer_end

        def get_actual_start_time(self):
            return self.actual_start_time

        def get_actual_end_time(self):
            return self.actual_end_time

    def __init__(self):

        self.dictionary = {}
        if not os.path.exists('requests.csv'):
            with open('requests.csv', 'w', newline='') as new_file:
                fieldnames = ['name', 'date', 'start_time', 'end_time', 'buffer_start', 'buffer_end']
                csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames, delimiter=',')
                csv_writer.writeheader()
        else:
            with open('requests.csv', 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for line in csv_reader:
                    request = Requests.Request(line['name'], line['date'], line['start_time'], line['end_time'], line['buffer_start'], line['buffer_end'])
                    try:
                        self.dictionary['%s' % line['date']].append(request)
                    except:
                        self.dictionary['%s' % line['date']] = []
                        self.dictionary['%s' % line['date']].append(request)

    def add_request(self, request):
        """
        add request to requests.csv and dictionary
        :param request: object request
        :return: None
        """

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

    def delete_request(self, request):
        """
        delete request from requests.csv and dictionary
        :param request: object request
        :return: None
        """

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

        self.dictionary[date].remove(request)

        if not self.dictionary[date]:
            del self.dictionary[date]

    def get_dictionary(self):
        return self.dictionary
