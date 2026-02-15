from database.data_manager import DataManager
import tkinter as tk
from tkinter import ttk


class BaseInterface(tk.Tk):
    """Main App window that manages navigation and shared resources."""

    def __init__(self, title="3D Model Stats App", size="800x600"):
        super().__init__()
        self.title(title)
        self.geometry(size)
        self.resizable(False, False)
        self.db = DataManager()

        self.style = ttk.Style()
        self.style.configure("TButton", font=("Segoe UI", 10), padding=5)
        self.style.configure("TLabel", font=("Segoe UI", 10))

        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}
        self.container = container

    def add_frame(self, name, frame_class):
        frame = frame_class(self.container, self)
        self.frames[name] = frame
        frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, name):
        frame = self.frames.get(name)
        if frame:
            frame.tkraise()

    def get_db(self):
        return self.db

    def exit_app(self):
        try:
            if self.db:
                self.db.close()
        finally:
            self.destroy()
