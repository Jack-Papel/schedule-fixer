import tkinter as tk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from schedule_fixer import fixer


class Form:
    def __init__(self):
        # Initialize form inputs
        self.filename = None

        # Create the root window
        self.root = tk.Tk()
        self.root.title('Schedule Fixer')
        self.root.resizable(False, False)
        self.root.geometry('400x200')

        # Create window elements
        file_selector_frame = tk.Frame()
        self.filepath_label = tk.Label(text="Select calendar path:")
        open_button = tk.Button(
            self.root,
            text='Open',
            command=self.select_file,
            padx=10
        )

        offset_frame = tk.Frame()

        self.days_offset_entry = tk.Entry()
        self.hours_offset_entry = tk.Entry()

        file_selector_frame.pack(expand=True)
        offset_frame.pack(expand=True)
        self.filepath_label.pack(in_=file_selector_frame, side=tk.LEFT)
        open_button.pack(in_=file_selector_frame, side=tk.RIGHT)
        tk.Label(text="How many days offset is the calendar? (+): early, (-): late")\
            .pack(in_=offset_frame, after=file_selector_frame)
        self.days_offset_entry.pack(in_=offset_frame)
        tk.Label(text="How many hours offset is the calendar? (+): early, (-): late")\
            .pack(in_=offset_frame)
        self.hours_offset_entry.pack(in_=offset_frame)
        tk.Button(
            self.root,
            text='Fix!',
            command=lambda: self.try_close_and_fix(self.hours_offset_entry.get(), self.days_offset_entry.get()),
            padx=20,
            pady=5
        ).pack(expand=True, side=tk.BOTTOM)

    def start(self):
        self.root.mainloop()

    def try_close_and_fix(self, offset_hours: str, offset_days: str):
        fail = False
        try:
            offset_hours = int(offset_hours)
            offset_days = int(offset_days)
        except ValueError:
            fail = True
        if not fail and self.filename and offset_hours is not None and offset_days is not None:
            self.close_and_fix(offset_hours, offset_days)
        else:
            showinfo(
                title="Error",
                message="Please fill all fields!"
            )

    def close_and_fix(self, offset_hours, offset_days):
        self.root.destroy()
        fixer.fix(self.filename, offset_days, offset_hours)
        showinfo(
            title="Fixed",
            message="The calendar has now been fixed!"
        )

    def select_file(self):
        filetypes = (
            ('iCal files', '*.ics'),
            ('All files', '*.*')  # There are like, a million different iCal formats
        )

        self.filename = fd.askopenfilename(
            title='Open a file',
            initialdir='~/Downloads',
            filetypes=filetypes
        )

        if self.filename:
            # FIXME there's no way this split works for every path and OS:
            self.filepath_label.configure(text="Selected file path: " + self.filename.split("/")[-1])
        else:
            showinfo(
                title="Invalid selection",
                message="Please make a valid file selection"
            )
