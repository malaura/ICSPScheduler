from code import Student
import unittest


class TestStudent(unittest.TestCase):
    def test_get_directory(self):
        mockDirectory = 'test.csv'
        student = Student(mockDirectory)
        directory = student.get_directory()
        self.assertEqual(directory, mockDirectory)

    def test_get_student_name(self):
        mockDirectory = 'test.csv'
        student = Student(mockDirectory)
        name = student.get_student_name()
        self.assertEqual(name, 'test')

    def test_get_validation_info(self):
        mockDirectory = 'test.csv'
        student = Student(mockDirectory)
        validation_info = student.get_validation_info()
        self.assertEqual(validation_info, "Format is correct")

    def test_get_validation(self):
        mockDirectory = 'test.csv'
        student = Student(mockDirectory)
        get_validation = student.get_validation()
        self.assertEqual(get_validation, True)

    def test_get_dictionary_of_schedule(self):
        mockDirectory = 'test.csv'
        student = Student(mockDirectory)
        get_dictionary_of_schedule = student.get_dictionary_of_schedule()
        self.assertEqual(get_dictionary_of_schedule, {})

    def test_get_dictionary_of_time_interval(self):
        mockDirectory = 'test.csv'
        student = Student(mockDirectory)
        get_dictionary_of_time_interval = student.get_dictionary_of_time_interval()
        self.assertEqual(get_dictionary_of_time_interval, {})

