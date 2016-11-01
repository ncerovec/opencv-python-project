# The code for changing pages was derived from: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# License: http://creativecommons.org/licenses/by-sa/3.0/

import Tkinter as tk
from GUI import uiTemplate
from GUI import uiFiltering
from GUI import uiBasicSub
from GUI import uiBgndModel


LARGE_FONT = ("Verdana", 12)


class mainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.iconbitmap(default='transparent.ico')
        self.resizable(False, False)
        self.title("Main")
        container = tk.Frame(self)

        buttonFiltering = tk.Button(self, text="Filtering Method", width=26, command=lambda : self.methodWindow(uiFiltering))
        buttonFiltering.grid(row=0, column=0, padx=3, pady=3)

        buttonBasicSub = tk.Button(self, text="Background subtraction", width=26, command=lambda: self.methodWindow(uiBasicSub))
        buttonBasicSub.grid(row=1, column=0, padx=3, pady=3)

        buttonBackModel = tk.Button(self, text="Background model", width=26, command=lambda: self.methodWindow(uiBgndModel))
        buttonBackModel.grid(row=2, column=0, padx=3, pady=3)

        buttonTemplate = tk.Button(self, text="Template Method", width=26, command=lambda: self.methodWindow(uiTemplate))
        buttonTemplate.grid(row=3, column=0, padx=3, pady=3)

    def methodWindow(self, UI):
        self.withdraw()
        self.top = tk.Toplevel()
        UI(self.top)
        self.top.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        self.top.destroy()
        self.deiconify()
