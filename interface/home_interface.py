from tkinter import ttk


class HomeInterface(ttk.Frame):
    """Home screen of the 3D Model Stats application."""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self._build_ui()

    def _build_ui(self):
        ttk.Label(self, text="🏠 Mesh Insight - Home", font=("Segoe UI", 18, "bold")).pack(pady=(30, 15))

        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="🔍 Analyze Models", command=lambda: self.controller.show_frame("AnalyzeInterface"),
            width=30).pack(pady=8)

        ttk.Button(button_frame, text="📊 View Reports", command=lambda: self.controller.show_frame("ReportInterface"),
            width=30).pack(pady=8)

        ttk.Button(button_frame, text="📁 Export Data (CSV)", command=lambda: self.controller.show_frame("ExportInterface"),
            width=30).pack(pady=8)

        ttk.Button(button_frame, text="🎨 Render Model", command=lambda: self.controller.show_frame("RenderInterface"),
            width=30).pack(pady=8)

        ttk.Separator(self, orient="horizontal").pack(fill="x", pady=20)
        ttk.Button(self, text="❌ Exit Application", command=self.controller.exit_app, width=25).pack(pady=10)

        ttk.Label(self, text="© 2025 Mesh Insight — All Rights Reserved", font=("Segoe UI", 9),
            foreground="#555").pack(side="bottom", pady=10)
