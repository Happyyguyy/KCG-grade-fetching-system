import _thread
import time
from tkinter import *


class Startup(Tk):
    def __init__(self):
        super().__init__()
        self.title("Config...")
        label = Label(master=self, text="Confirm Assembly number")
        label.pack()

        self.entry = Entry(master=self)
        self.entry.insert("0", self.get_assembly())
        self.entry.pack()

        frame = Frame(master=self)
        frame.pack()

        confirm = Button(
            master=frame, command=self.confirm_assembly, text="Confirm...")
        confirm.pack(side=LEFT)

        cancel = Button(master=frame, command=quit, text="Quit...")
        cancel.pack(side=LEFT)

    def get_assembly(self):
        with open("assembly.config") as f:
            num = f.read()
            print(num)
            self.assembly = num

        return self.assembly

    def confirm_assembly(self):
        if self.entry.get() != self.assembly:
            with open("assembly.config", "w") as f:
                f.write(self.entry.get())
                print(self.entry.get())

        self.destroy()


startup = Startup()
assembly = startup.assembly
startup.mainloop()
