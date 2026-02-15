from core.mesh_loader import MeshLoader
from analyzers.mesh_analyzer import MeshAnalyzer
from analyzers.geometry_analyzer import GeometryAnalyzer
from analyzers.quality_analyzer import QualityAnalyzer
from analyzers.performance_analyzer import PerformanceAnalyzer
from database.data_manager import DataManager
import sys


class AnalyzerRunner:
    """Handles sequential execution of all analyzers."""

    def __init__(self, file_name: str):
        self.file_name = file_name
        self.db = DataManager()

    def run(self):
        """Loads the mesh and performs all analyses."""
        loader = MeshLoader(self.file_name)
        mesh = loader.load()

        print("--- Loading Model Stats ---")
        model_stats = loader.stats()

        print("--- Running Mesh Analysis ---")
        mesh_stats = MeshAnalyzer(mesh, loader.file_path).analyze()

        print("--- Running Geometry Analysis ---")
        geometry_stats = GeometryAnalyzer(mesh).analyze()

        print("--- Running Quality Analysis ---")
        quality_stats = QualityAnalyzer(mesh).analyze()

        print("--- Running Performance Analysis ---")
        perf_stats = PerformanceAnalyzer(mesh, loader.file_path, loader.load_time).analyze()

        model_id, is_new = self.db.insert_model_stats(model_stats["model_name"], model_stats["model_size"])

        self.db.insert_mesh_stats(model_id, mesh_stats)
        self.db.insert_geometry_stats(model_id, geometry_stats)
        self.db.insert_quality_stats(model_id, quality_stats)
        self.db.insert_performance_stats(model_id, perf_stats)
        self.db.close()

        if is_new:
            print("\nStats successfully saved to database.")
        else:
            print("\nStats successfully updated in database.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze.py <model_name.stl>")
        sys.exit(1)

    model_name = sys.argv[1]
    runner = AnalyzerRunner(model_name)
    runner.run()
