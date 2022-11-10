"""
Defines the form for handling user input for fixing the calendar.

:author Jack Papel
"""
import ctypes
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from schedule_fixer import fixer, fs_util

# TODO: Verify this works on all systems
ctypes.cdll.shcore.SetProcessDpiAwareness(1)


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

        # Create window elements
        file_selector_frame = ttk.Frame()
        filepath_label = ttk.Label(text="Select a Calendar: *")
        self.filepath_entry = ttk.Entry(width=30, state=tk.DISABLED)
        open_button = ttk.Button(
            self.root,
            text='Select',
            command=self.select_file,
        )

        file_selector_frame.pack(fill=tk.X, pady=10, padx=10, expand=True)
        filepath_label.pack(in_=file_selector_frame, side=tk.TOP, anchor=tk.NW)
        self.filepath_entry.pack(in_=file_selector_frame, padx=5, side=tk.LEFT, fill=tk.X, expand=True)
        open_button.pack(in_=file_selector_frame, side=tk.RIGHT)

        settings_frame = ttk.Frame()
        settings_frame.pack(after=file_selector_frame, fill=tk.X, pady=10, padx=10, expand=True)

        manual = tk.IntVar()
        manual_mode_checkbox = ttk.Checkbutton(text="Advanced",
                                               variable=manual,
                                               command=lambda: self.set_manual_mode(manual.get() == 1,
                                                                                    days_offset_entry,
                                                                                    hours_offset_entry,
                                                                                    days_offset_label,
                                                                                    hours_offset_label),
                                               )

        manual_mode_checkbox.pack(in_=settings_frame, side=tk.TOP, anchor=tk.NW)

        ttk.Separator(settings_frame, orient=tk.VERTICAL)\
            .pack(in_=settings_frame, side=tk.LEFT, fill=tk.Y, padx=10)

        advanced_settings_frame = ttk.Frame()
        advanced_settings_frame.pack(in_=settings_frame, fill=tk.X, expand=True, side=tk.LEFT, anchor=tk.W)

        offset_text = ttk.Label(text="Note: If the calendar is later than it is supposed to be,"
                                     "\nyou can input a negative number.")
        offset_text.pack(in_=advanced_settings_frame, anchor=tk.W, padx=5, pady=5)

        days_frame = ttk.Frame()
        days_offset_label = ttk.Label(text="How many days early is the calendar?")
        days_offset_entry = ttk.Entry(width=5)

        days_frame.pack(in_=advanced_settings_frame, anchor=tk.W, fill=tk.X, expand=True)
        days_offset_label.pack(in_=days_frame, anchor=tk.W, padx=5, side=tk.LEFT)
        days_offset_entry.pack(in_=days_frame, anchor=tk.E, padx=5, side=tk.RIGHT)

        hours_frame = ttk.Frame()
        hours_offset_label = ttk.Label(text="How many hours early is the calendar?")
        hours_offset_entry = ttk.Entry(width=5)

        hours_frame.pack(in_=advanced_settings_frame, anchor=tk.W, fill=tk.X, expand=True)
        hours_offset_label.pack(in_=hours_frame, anchor=tk.W, padx=5, side=tk.LEFT)
        hours_offset_entry.pack(in_=hours_frame, anchor=tk.E, padx=5, side=tk.RIGHT)

        fixed_filepath_label = ttk.Label(text="Custom save location:")
        self.fixed_filepath_entry = ttk.Entry()
        fixed_filepath_label.pack(in_=advanced_settings_frame, padx=5, anchor=tk.W)
        self.fixed_filepath_entry.pack(in_=advanced_settings_frame, side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(
            text="Select",
            command=lambda: self.fixed_filepath_entry.insert(0, fd.askdirectory(
                initialdir="~/Downloads",
                mustexist=True
            ))
        ).pack(in_=advanced_settings_frame, side=tk.RIGHT)

        ttk.Button(
            text='Cancel',
            command=self.root.destroy,
        ).pack(side=tk.RIGHT, anchor=tk.SE, padx=10, pady=10)
        ttk.Button(
            text='Fix!',
            command=lambda: self.try_close_and_fix(self.filename, hours_offset_entry.get(), days_offset_entry.get()),
        ).pack(side=tk.RIGHT, anchor=tk.SE, pady=10)

        self.set_manual_mode(False, days_offset_entry, hours_offset_entry, days_offset_label, hours_offset_label)

    def start(self) -> None:
        """
        Show the form
        """
        self.root.mainloop()

    def set_manual_mode(self, manual: bool, days_offset_entry: tk.Entry, hours_offset_entry: tk.Entry, *widgets) -> None:
        """
        Toggle the manual mode of the form.
        :param manual: Whether the form should be in manual mode
        :param days_offset_entry: The entry for the days offset
        :param hours_offset_entry: The entry for the hours offset
        :param widgets: The other widgets to toggle
        """
        if not manual:
            days_offset_entry.delete(0, tk.END)
            hours_offset_entry.delete(0, tk.END)
            days_offset_entry.insert(0, '10')
            hours_offset_entry.insert(0, '0')
        self.disable_widgets(manual, days_offset_entry, hours_offset_entry, *widgets)

    # noinspection PyArgumentList
    def disable_widgets(self, manual: bool, *widgets: tk.Widget) -> None:
        """
        Toggle the disabled state of the given widgets.
        :param manual: Whether the widgets should be disabled
        :param widgets: The widgets to toggle
        """
        for widget in widgets:
            if manual:
                widget.configure(state=tk.NORMAL)
            else:
                widget.configure(state=tk.DISABLED)

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
            self.filepath_entry.configure(state=tk.NORMAL)
            self.filepath_entry.delete(0, tk.END)
            self.filepath_entry.insert(0, self.filename)
            self.filepath_entry.configure(state=tk.DISABLED)
            self.fixed_filepath_entry.delete(0, tk.END)
            self.fixed_filepath_entry.insert(0, fs_util.fixed_path(self.filename))
        else:
            showinfo(
                title="Invalid selection",
                message="Please make a valid file selection"
            )
