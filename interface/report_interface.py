from interface.base_frame import BaseFrame
from report import ReportViewer
from tkinter import ttk, messagebox
import tkinter as tk, io, sys


class ReportInterface(BaseFrame):
    """Interface for viewing reports."""

    def __init__(self, parent, controller):
        super().__init__(parent, controller, title="Model Report Viewer", show_console=True)
        self.report_viewer = None
        self.selected_model = tk.StringVar()
        self._build_ui()

    def _build_ui(self):
        select_frame = ttk.Frame(self)
        select_frame.pack(fill="x", pady=10)

        ttk.Label(select_frame, text="Select Model:").pack(side="left", padx=5)
        self.model_dropdown = ttk.Combobox(select_frame, textvariable=self.selected_model, width=40, state="readonly")
        self.model_dropdown.pack(side="left", padx=5)
        ttk.Button(select_frame, text="Load", command=self._load_report).pack(side="left", padx=5)
        ttk.Button(select_frame, text="Refresh", command=self._load_model_list).pack(side="left", padx=5)

        self._load_model_list()

    def _load_model_list(self):
        try:
            models = self.get_db().get_model_name()
            if not models:
                self.model_dropdown["values"] = []
                self.model_dropdown.set("")
                messagebox.showinfo("Info", "No analyzed models found.")
            else:
                model_list = [m[0] for m in models]
                self.model_dropdown["values"] = model_list
                self.model_dropdown.set(model_list[0])
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def _load_report(self):
        model_name = self.selected_model.get()
        if not model_name:
            messagebox.showwarning("Select Model", "Please select a model first.")
            return

        try:
            self.log(f"Loading report for: {model_name} ...")
            self.report_viewer = ReportViewer(model_name)

            buffer = io.StringIO()
            sys_stdout_backup = sys.stdout
            sys.stdout = buffer

            self.report_viewer.display()

            sys.stdout = sys_stdout_backup
            report_text = buffer.getvalue()
            buffer.close()

            self.log(report_text)
            self.log("Report loaded successfully.")
        except Exception as e:
            sys.stdout = sys.__stdout__
            messagebox.showerror("Error", f"Failed to load report:\n{e}")
        finally:
            if self.report_viewer:
                self.report_viewer.close()
