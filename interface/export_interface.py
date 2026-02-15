from interface.base_frame import BaseFrame
from export import CSVExporter
from tkinter import ttk, messagebox
import tkinter as tk


class ExportInterface(BaseFrame):
    """Interface for exporting model analysis data as CSV."""

    def __init__(self, parent, controller):
        super().__init__(parent, controller, title="Model Report Exporter", show_console=True)
        self.selected_model = tk.StringVar()
        self._build_ui()

    def _build_ui(self):
        select_frame = ttk.Frame(self)
        select_frame.pack(pady=10)

        ttk.Label(select_frame, text="Select Model:").pack(side="left", padx=5)
        self.model_dropdown = ttk.Combobox(select_frame, textvariable=self.selected_model, width=40, state="readonly")
        self.model_dropdown.pack(side="left", padx=5)
        ttk.Button(select_frame, text="Refresh", command=self._load_model_list).pack(side="left", padx=5)
        ttk.Button(self, text="Export CSV", command=self._export_csv, width=20).pack(pady=10)

        self._load_model_list()

    def _load_model_list(self):
        try:
            models = self.get_db().get_model_name()
            if not models:
                self.model_dropdown["values"] = []
                self.model_dropdown.set("")
                messagebox.showinfo("Info", "No analyzed models found.")
            else:
                names = [m[0] for m in models]
                self.model_dropdown["values"] = names
                self.model_dropdown.set(names[0])
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def _export_csv(self):
        model_name = self.selected_model.get()
        if not model_name:
            messagebox.showwarning("Select Model", "Please select a model to export.")
            return

        self.log(f"Exporting {model_name} to CSV...")
        try:
            exporter = CSVExporter(model_name)
            exporter.export()
            exporter.close()
            self.log(f"Export completed successfully for {model_name}")
            messagebox.showinfo("Export Complete", f"{model_name} exported successfully.")
        except Exception as e:
            self.log(f"Export failed: {e}")
            messagebox.showerror("Export Error", f"Failed to export model:\n{e}")
