from tkinter import *
from tkinter import ttk

class Prompt():
    def __init__(self, parent, title, text, action=None):
        '''
        parent - reference to the parent's tkinter object
        title - text containing the title of prompt
        text - text containing the description of prompt
        action - action the prompt will do perform if button is pressed
        '''
        self.parent = parent
        self.title = title
        self.text = text
        self.action = action

        self.createPrompt()

    def createPrompt(self):
        '''
        Creates a window prompt with the specified information if there is not current prompt
        window open.

        :return:
        '''
        if self.parent.promptWindowOpen:
            return
        self.prompt = Toplevel(self.parent.root)
        self.prompt.attributes("-topmost", True)
        self.prompt.minsize(width=225, height=75)
        self.prompt.maxsize(width=450, height=200)
        self.prompt.title(self.title)
        messageLabel = Label(self.prompt, text=self.text)

        if self.action == None:
            self.action = self.closePrompt
        okButton = Button(self.prompt, text="Ok", command=self.action, width=10)
        cancelButton = Button(self.prompt, text="Cancel", command=self.closePrompt, width=10)

        messageLabel.grid(row=0, column=0, columnspan=2, sticky=EW, pady=5)
        okButton.grid(row=1, column=1, padx=5, pady=(0,5))
        cancelButton.grid(row=1, column=0, padx=5, pady=(0,5))
        self.prompt.columnconfigure(0, weight=1)
        self.prompt.columnconfigure(1, weight=1)
        self.prompt.rowconfigure(1, weight=1)
        self.prompt.protocol("WM_DELETE_WINDOW", self.closePrompt)
        self.parent.promptWindowOpen = True

    def closePrompt(self):
        '''
        Closes the window prompt.
        Sets the promptWindowOpen attribute from MainWindow to false

        :return:
        '''

        self.parent.promptWindowOpen = False
        self.prompt.destroy()
