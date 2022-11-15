import tkinter as tk
from tkinter import ttk, filedialog as fd

from schedule_fixer import fs_util


# noinspection PyArgumentList
def enable_or_disable_widgets(advanced: bool, *widgets: tk.Widget) -> None:
    """
    Toggle the disabled state of the given widgets.
    :param advanced: Whether the widgets should be disabled
    :param widgets: The widgets to toggle
    """
    for widget in widgets:
        if advanced:
            widget.configure(state=tk.NORMAL)
        else:
            widget.configure(state=tk.DISABLED)


class SettingsPane:
    def __init__(self, parent, root: tk.Frame):
        self._parent = parent
        self._root = root

        self._offset_text = ttk.Label(text="Note: If the calendar is later than it is supposed "
                                           "\nto be, you can input a negative number.")

        self._days_frame = ttk.Frame()
        self._days_offset_label = ttk.Label(text="How many days early is the calendar?")
        self._days_offset_entry = ttk.Entry(width=5)

        self._hours_frame = ttk.Frame()
        self._hours_offset_label = ttk.Label(text="How many hours early is the calendar?")
        self._hours_offset_entry = ttk.Entry(width=5)

        self._save_dir_label = ttk.Label(text="Custom save location:")
        self._save_entry = ttk.Entry()
        self._select_dir_button = ttk.Button(
            text="Select",
            command=lambda: self._save_entry.insert(0, fd.askdirectory(
                initialdir="~/Downloads",
                mustexist=True
            ))
        )

        self._enabled = False
        self.set_enabled(False)

    def pack(self) -> None:
        """
        Pack the form.
        """
        self._offset_text.pack(in_=self._root, anchor=tk.W, padx=5, pady=5)

        self._days_frame.pack(in_=self._root, pady=(10, 0), anchor=tk.W, fill=tk.X, expand=True)
        self._days_offset_label.pack(in_=self._days_frame, anchor=tk.W, padx=5, side=tk.LEFT)
        self._days_offset_entry.pack(in_=self._days_frame, anchor=tk.E, padx=5, side=tk.RIGHT)

        self._hours_frame.pack(in_=self._root, pady=(0, 10), anchor=tk.W, fill=tk.X, expand=True)
        self._hours_offset_label.pack(in_=self._hours_frame, anchor=tk.W, padx=5, side=tk.LEFT)
        self._hours_offset_entry.pack(in_=self._hours_frame, anchor=tk.E, padx=5, side=tk.RIGHT)

        self._save_dir_label.pack(in_=self._root, pady=(10, 0), padx=5, anchor=tk.W)
        self._save_entry.pack(in_=self._root, side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self._select_dir_button.pack(in_=self._root, side=tk.RIGHT)

    def is_enabled(self) -> bool:
        return self._enabled

    def set_enabled(self, enabled: bool) -> None:
        """
        Toggle the manual mode of the form.
        :param enabled: Whether the form should be in manual mode
        """
        self._enabled = enabled

        if not enabled:
            self._days_offset_entry.delete(0, tk.END)
            self._hours_offset_entry.delete(0, tk.END)
            self._days_offset_entry.insert(0, '1')
            self._hours_offset_entry.insert(0, '0')
            self._save_entry.delete(0, tk.END)
            if self._parent.get_filepath():
                self._save_entry.insert(0, fs_util.fixed_path(None, self._parent.get_filepath()))

        enable_or_disable_widgets(enabled,
                                  self._offset_text,
                                  self._days_offset_label, self._days_offset_entry,
                                  self._hours_offset_label, self._hours_offset_entry,
                                  self._save_dir_label, self._save_entry,
                                  self._select_dir_button)

    def get_days_offset(self) -> int:
        """
        Get the days offset from the form.
        :return: The days offset
        """
        try:
            return int(self._days_offset_entry.get())
        except ValueError:
            return None

    def get_hours_offset(self) -> int:
        """
        Get the hours offset from the form.
        :return: The hours offset
        """
        try:
            return int(self._hours_offset_entry.get())
        except ValueError:
            return None

    def get_save_directory(self) -> str:
        """
        Get the save directory from the form.
        :return: The save directory
        """
        return self._save_entry.get()

    def get_save_path(self) -> str:
        """
        Get the save path from the form.
        :return: The save path
        """
        return fs_util.fixed_path(self.get_save_directory(), self._parent.get_filepath())

    def set_save_directory(self, enabled: bool, filename: str) -> None:
        """
        Set the save directory to the given filename.
        :param enabled: Whether the advanced settings panel is enabled
        :param filename: The filename to set the save directory to
        """
        enable_or_disable_widgets(True, self._save_entry)
        self._save_entry.delete(0, tk.END)
        self._save_entry.insert(0, fs_util.get_dir(filename))
        if not enabled:
            enable_or_disable_widgets(False, self._save_entry)
