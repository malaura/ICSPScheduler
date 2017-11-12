from tkinter import *
from tkinter import ttk

class Prompt():
    def __init__(self, parent, title, text, action=None):
        self.parent = parent
        self.title = title
        self.text = text
        self.action = action

        self.createPrompt()

    def createPrompt(self):
        self.prompt = Toplevel(self.parent.root)
        self.prompt.minsize(width=225, height=75)
        self.prompt.maxsize(width=225, height=75)
        self.prompt.title(self.title)
        messageLabel = Label(self.prompt, text=self.text)
        okButton = Button(self.prompt, text="Ok", command=self.action, width=10)
        cancelButton = Button(self.prompt, text="Cancel", command=self.prompt.destroy, width=10)

        messageLabel.grid(row=0, column=0, columnspan=2, sticky=EW, pady=5)
        okButton.grid(row=1, column=1, padx=5, pady=(0,5))
        cancelButton.grid(row=1, column=0, padx=5, pady=(0,5))
        self.prompt.columnconfigure(0, weight=1)
        self.prompt.columnconfigure(1, weight=1)
        self.prompt.rowconfigure(1, weight=1)
