from interface.base_frame import BaseFrame
from render import RenderRunner
from tkinter import ttk, messagebox
import tkinter as tk


class RenderInterface(BaseFrame):
    """Interface for rendering 3D models."""

    def __init__(self, parent, controller):
        super().__init__(parent, controller, title="Model Renderer", show_console=True)
        self.selected_model = tk.StringVar()
        self.render_mode = tk.StringVar(value="Standard")
        self.viewer_container = ttk.Frame(self)
        self.viewer_container.pack(fill="both", expand=True, padx=10, pady=10)

        self._build_ui()

    def _build_ui(self):
        select_frame = ttk.Frame(self)
        select_frame.pack(pady=10)

        ttk.Label(select_frame, text="Select Model:").pack(side="left", padx=5)
        self.model_dropdown = ttk.Combobox(select_frame, textvariable=self.selected_model, width=40, state="readonly")
        self.model_dropdown.pack(side="left", padx=5)
        ttk.Button(select_frame, text="Refresh", command=self._load_model_list).pack(side="left", padx=5)

        mode_frame = ttk.Frame(self)
        mode_frame.pack(pady=5)
        ttk.Label(mode_frame, text="Render Mode:").pack(side="left", padx=5)
        ttk.Combobox(mode_frame, textvariable=self.render_mode, values=["Standard", "Wireframe"], state="readonly", width=12).pack(side="left")

        ttk.Button(self, text="Render Model", command=self._render_model, width=20).pack(pady=15)
        self._load_model_list()

    def _load_model_list(self):
        try:
            models = self.get_db().get_model_name()
            if not models:
                self.model_dropdown["values"] = []
                self.model_dropdown.set("")
            else:
                names = [m[0] for m in models]
                self.model_dropdown["values"] = names
                self.model_dropdown.set(names[0])
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def _render_model(self):
        model_name = self.selected_model.get()
        if not model_name:
            messagebox.showwarning("Select Model", "Please select a model first.")
            return

        mode = self.render_mode.get().lower()
        self.log(f"Rendering '{model_name}' in {mode} mode...")
        try:
            RenderRunner.run(model_name, mode)
            self.log("Render completed successfully.")
            messagebox.showinfo("Render Complete", f"Rendering completed for {model_name}.")
        except Exception as e:
            self.log(f"Render failed: {e}")
            messagebox.showerror("Render Error", f"Failed to render model:\n{e}")
