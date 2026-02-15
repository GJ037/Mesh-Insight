from interface.base_frame import BaseFrame
from analyze import AnalyzerRunner
from tkinter import ttk, filedialog, messagebox
import tkinter as tk, os


class AnalyzeInterface(BaseFrame):
    """Interface for running model analysis."""

    def __init__(self, parent, controller):
        super().__init__(parent, controller, title="Model Analyzer", show_console=True)
        self.selected_file = tk.StringVar()
        self._build_ui()

    def _build_ui(self):
        file_frame = ttk.Frame(self)
        file_frame.pack(pady=10, fill="x")

        ttk.Label(file_frame, text="Select STL Model:").pack(side="left", padx=5)
        ttk.Entry(file_frame, textvariable=self.selected_file, width=40).pack(side="left", padx=5)
        ttk.Button(file_frame, text="Browse", command=self._browse_file).pack(side="left", padx=5)

        ttk.Button(self, text="Run Analysis", command=self._run_analysis, width=25).pack(pady=10)

    def _browse_file(self):
        file_path = filedialog.askopenfilename(title="Select STL File",
            filetypes=[("STL files", "*.stl"), ("All files", "*.*")])
        if file_path:
            self.selected_file.set(file_path)

    def _run_analysis(self):
        file_path = self.selected_file.get().strip()
        if not file_path or not os.path.exists(file_path):
            messagebox.showerror("Invalid File", "Please select a valid STL file.")
            return

        file_name = os.path.basename(file_path)
        self.log(f"Running analysis on: {file_name} ...")

        try:
            runner = AnalyzerRunner(file_path)
            runner.run()
            self.log("Analysis completed successfully.")
            messagebox.showinfo("Success", "Model analysis finished successfully.")
        except Exception as e:
            self.log(f"Error: {e}")
            messagebox.showerror("Error", f"An error occurred:\n{e}")
