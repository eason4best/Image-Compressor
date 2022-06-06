from tkinter import *

from application import Application
from main_frame import MainFrame

app = Application()
MainFrame(app, 600)
app.mainloop()