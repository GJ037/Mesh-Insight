import tkinter as tk
from tkinter import ttk

class BaseFrame(ttk.Frame):
    """Base class for consistent layout and shared methods."""

    def __init__(self, parent, controller, title=None, show_console=False):
        super().__init__(parent)
        self.controller = controller
        self.title = title
        self.show_console = show_console
        self.console = None

        if self.title:
            ttk.Label(self, text=self.title, font=("Segoe UI", 16, "bold")).pack(pady=15)

        if self.show_console:
            ttk.Label(self, text="Console Log:", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=10)
            self.console = tk.Text(self, height=15, state="disabled", wrap="word", bg="#f7f7f7")
            self.console.pack(fill="both", expand=True, padx=10, pady=5)

        ttk.Separator(self, orient="horizontal").pack(fill="x", pady=10)
        ttk.Button(self, text="Return to Home", command=lambda: self.controller.show_frame("HomeInterface"),
            width=25).pack(pady=10)

    def log(self, text):
        if not self.console:
            return
        self.console.configure(state="normal")
        self.console.insert(tk.END, text + "\n")
        self.console.configure(state="disabled")
        self.console.see(tk.END)

    def get_db(self):
        return self.controller.get_db()
