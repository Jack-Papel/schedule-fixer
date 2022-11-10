"""
Defines the form for handling user input for fixing the calendar.

:author Jack Papel
"""
import tkinter as tk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from schedule_fixer import fixer, fs_util


class Form:
    """
    A form for the user to select an iCal file and fix it.
    """

    def __init__(self):
        """
        Create the form.
        """
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

        days_offset_entry = tk.Entry()
        hours_offset_entry = tk.Entry()

        file_selector_frame.pack(expand=True)
        offset_frame.pack(expand=True)
        self.filepath_label.pack(in_=file_selector_frame, side=tk.LEFT)
        open_button.pack(in_=file_selector_frame, side=tk.RIGHT)
        tk.Label(text="How many days offset is the calendar? (+): early, (-): late")\
            .pack(in_=offset_frame, after=file_selector_frame)
        days_offset_entry.pack(in_=offset_frame)
        tk.Label(text="How many hours offset is the calendar? (+): early, (-): late")\
            .pack(in_=offset_frame)
        hours_offset_entry.pack(in_=offset_frame)
        tk.Button(
            self.root,
            text='Fix!',
            command=lambda: self.try_close_and_fix(self.filename, hours_offset_entry.get(), days_offset_entry.get()),
            padx=20,
            pady=5
        ).pack(expand=True, side=tk.BOTTOM)

    def start(self) -> None:
        """
        Show the form
        """
        self.root.mainloop()

    def try_close_and_fix(self, filename: str, offset_hours: str, offset_days: str) -> None:
        """
        Try to close the form and fix the file.
        If not all the fields are filled out, show an error message, and don't close
        :param filename: The name of the file to fix
        :param offset_hours: The number of hours to offset the calendar by
        :param offset_days: The number of days to offset the calendar by
        """
        fail = False
        try:
            offset_hours = int(offset_hours)
            offset_days = int(offset_days)
        except ValueError:
            fail = True
        if not fail and filename and offset_hours is not None and offset_days is not None:
            self.close_and_fix(filename, offset_hours, offset_days)
        else:
            showinfo(
                title="Error",
                message="Please fill all fields!"
            )

    def close_and_fix(self, filename: str, offset_hours: int, offset_days: int) -> None:
        """
        Close the form and fix the file.
        :param filename: The file to fix
        :param offset_hours: The number of hours to offset the calendar by
        :param offset_days: The number of days to offset the calendar by
        """
        self.root.destroy()
        fixer.fix(filename, offset_days, offset_hours)
        showinfo(
            title="Fixed",
            message="The calendar has now been fixed!"
        )

    def select_file(self) -> None:
        """
        Open the file picker, and handle the file selection.
        """
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
            self.filepath_label.configure(text="Selected file: " + fs_util.name_and_extension(self.filename))
        else:
            showinfo(
                title="Invalid selection",
                message="Please make a valid file selection"
            )
