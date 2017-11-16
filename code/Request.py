class Request():

    def __init__(self, date, start_time, end_time, buffer_start, buffer_end):
        """

        :param date: request's date
        :param start_time: request's start time
        :param end_time: request's end time
        :param buffer_start: request's buffer start
        :param buffer_end: request's date
        """
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
        self.actual_start_time = float('%s.%s' % hour, minute)
        minute = int(end_time.split(':')[1]) + int(buffer_end.split(':')[1])
        if minute > 60:
            minute -= 60
            hour = int(end_time.split(':')[0]) + int(buffer_end.split(':')[0]) + 1
        else:
            hour = int(end_time.split(':')[0]) + int(buffer_end.split(':')[0])
        self.actual_end_time = float('%s.%s' % hour, minute)

        self.available_students = []
        self.assigned_student = ''

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
