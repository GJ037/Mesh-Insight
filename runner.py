from interface.base_interface import BaseInterface
from interface.home_interface import HomeInterface
from interface.analyze_interface import AnalyzeInterface
from interface.report_interface import ReportInterface
from interface.export_interface import ExportInterface
from interface.render_interface import RenderInterface

if __name__ == "__main__":
    app = BaseInterface()

    app.add_frame("HomeInterface", HomeInterface)
    app.add_frame("AnalyzeInterface", AnalyzeInterface)
    app.add_frame("ReportInterface", ReportInterface)
    app.add_frame("ExportInterface", ExportInterface)
    app.add_frame("RenderInterface", RenderInterface)

    app.show_frame("HomeInterface")
    app.mainloop()
