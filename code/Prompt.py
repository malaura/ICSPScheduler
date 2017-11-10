import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot


class Prompt(QWidget):

	def __init__(self, title, text, action=None):
		super().__init__()
		self.title = title
		self.text = text
		self.action = action
		self.left = 10 
		self.top = 10
		self.width = 320
		self.height = 200
		self.initializeInterface()

	def initializeInterface(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)

		prompt = QMessageBox.question(self, self.title, self.text, QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)
		if prompt == QMessageBox.Ok:
			self.action()

		self.show()

