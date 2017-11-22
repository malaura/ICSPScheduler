from code import Student
import unittest


class TestStudent(unittest.TestCase):
    def test_get_directory(self):
        mockDirectory = 'Students/Jim.csv'
        student = Student(mockDirectory)
        directory = student.get_directory()
        self.assertEqual(directory, mockDirectory)

    def test_get_student_name(self):
        mockDirectory = 'Students/Jim.csv'
        student = Student(mockDirectory)
        name = student.get_student_name()
        self.assertEqual(name, 'Jim')
