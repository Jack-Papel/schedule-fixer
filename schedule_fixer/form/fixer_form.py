"""
Defines the form for handling user input for fixing the calendar.

:author Jack Papel
"""
import ctypes
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from schedule_fixer import fixer
from schedule_fixer.form.settings_pane import SettingsPane

# TODO: Verify this works on all systems
ctypes.cdll.shcore.SetProcessDpiAwareness(1)


class FixerForm:
    """
    A form for the user to select an iCal file and fix it.
    """

    def __init__(self):
        """
        Create the form.
        """
        # Create the root window
        self.root = tk.Tk()
        self.root.title('Schedule Fixer')
        self.root.resizable(False, False)

        # Create window elements
        file_selector_frame = ttk.Frame()
        filepath_label = ttk.Label(text="Select a Calendar:*")
        self.filepath_entry = ttk.Entry(width=30, state=tk.DISABLED)
        open_button = ttk.Button(
            self.root,
            text='Select',
            command=self.select_file,
        )

        file_selector_frame.pack(fill=tk.X, pady=10, padx=10, expand=True)
        filepath_label.pack(in_=file_selector_frame, padx=5, side=tk.TOP, anchor=tk.NW)
        self.filepath_entry.pack(in_=file_selector_frame, padx=5, side=tk.LEFT, fill=tk.X, expand=True)
        open_button.pack(in_=file_selector_frame, side=tk.RIGHT)

        settings_frame = ttk.Frame()
        settings_frame.pack(after=file_selector_frame, fill=tk.X, pady=20, padx=10, expand=True)

        advanced = tk.BooleanVar()
        advanced_mode_checkbox = ttk.Checkbutton(
            text="Advanced",
            variable=advanced,
            command=lambda: self.settings_pane.set_enabled(advanced.get())
        )

        advanced_mode_checkbox.pack(in_=settings_frame, side=tk.TOP, anchor=tk.NW)

        ttk.Separator(settings_frame, orient=tk.VERTICAL)\
            .pack(in_=settings_frame, side=tk.LEFT, fill=tk.Y, padx=10)

        advanced_settings_frame = ttk.Frame()
        advanced_settings_frame.pack(in_=settings_frame, fill=tk.X, expand=True, side=tk.LEFT, anchor=tk.W)

        advanced_settings_frame.pack(fill=tk.X, expand=True)

        self.settings_pane = SettingsPane(self, advanced_settings_frame)
        self.settings_pane.pack()

        ttk.Button(
            text='Cancel',
            command=self.root.destroy,
        ).pack(side=tk.RIGHT, anchor=tk.SE, padx=10, pady=10)
        ttk.Button(
            text='Confirm',
            command=lambda: self.try_close_and_fix(),
        ).pack(side=tk.RIGHT, anchor=tk.SE, pady=10)

    def get_filepath(self):
        """
        Get the filepath of the selected file
        """
        return self.filepath_entry.get()

    def start(self) -> None:
        """
        Show the form
        """
        self.root.mainloop()

    def try_close_and_fix(self) -> None:
        """
        Try to close the form and fix the file.
        If not all the fields are filled out, show an error message, and don't close
        """
        if self.filepath_entry.get() and self.settings_pane.get_hours_offset() is not None \
                and self.settings_pane.get_days_offset() is not None\
                and self.settings_pane.get_save_directory():
            self.close_and_fix()
        else:
            showinfo(
                title="Error",
                message="Please fill all fields!"
                        " (The asterisk next to the field name indicates it is required)"
                        "\n\nIncomplete fields:\n" + ",\n"
                .join(
                    [field_name for value, field_name in [(self.filepath_entry.get(), "Calendar"),
                                                          (self.settings_pane.get_hours_offset(), "Hours Offset"),
                                                          (self.settings_pane.get_days_offset(), "Days Offset"),
                                                          (self.settings_pane.get_save_directory(), "Save Directory")]
                     if value is None or value == ""])
            )

    def close_and_fix(self) -> None:
        """
        Close the form and fix the file.
        """
        filepath = self.filepath_entry.get()
        save_path = self.settings_pane.get_save_path()
        hours_offset = self.settings_pane.get_hours_offset()
        days_offset = self.settings_pane.get_days_offset()

        self.root.destroy()
        fixer.fix(filepath, save_path, days_offset, hours_offset)
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

        self.filepath_entry.delete(0, tk.END)
        filepath = fd.askopenfilename(
            title='Open a file',
            initialdir='~/Downloads',
            filetypes=filetypes
        )

        if filepath:
            self.filepath_entry.configure(state=tk.NORMAL)
            self.filepath_entry.delete(0, tk.END)
            self.filepath_entry.insert(0, filepath)
            self.filepath_entry.configure(state=tk.DISABLED)
            if not self.settings_pane.is_enabled():
                self.settings_pane.set_save_directory(False, filepath)
        else:
            showinfo(
                title="Invalid selection",
                message="Please make a valid file selection"
            )
