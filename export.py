from database.data_manager import DataManager
from config import OUTPUT_DIR
import csv, sys, os


class CSVExporter:
    """Exports model analysis results to a CSV file."""

    def __init__(self, file_name: str):
        self.file_name = file_name
        self.db = DataManager()

    def export(self):
        model = self.db.get_model_stats(self.file_name)
        if not model:
            print(f"No report found for model: {self.file_name}")
            return

        id, name, size = model
        mesh_stats = self.db.get_mesh_stats(id)
        quality_stats = self.db.get_quality_stats(id)
        geometry_stats = self.db.get_geometry_stats(id)
        performance_stats = self.db.get_performance_stats(id)

        os.makedirs(OUTPUT_DIR, exist_ok=True)
        file_name = f"{os.path.splitext(self.file_name)[0]}.csv"
        file_path = os.path.join(OUTPUT_DIR, file_name)

        with open(file_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            writer.writerow(["Model Stats"])
            writer.writerow(["id", "name", "size"])
            writer.writerow([id, name, size])
            writer.writerow([])

            if mesh_stats:
                writer.writerow(["Mesh Stats"])
                writer.writerow([
                    "vertices", "triangles", "surface", "volume",
                    "bbox_x", "bbox_y", "bbox_z", "center_x", "center_y", "center_z"
                ])
                writer.writerow(mesh_stats)
                writer.writerow([])

            if quality_stats:
                writer.writerow(["Quality Stats"])
                writer.writerow(["uniformity", "water_tight", "degen_faces", "dup_vertices"])
                writer.writerow(quality_stats)
                writer.writerow([])

            if geometry_stats:
                writer.writerow(["Geometry Stats"])
                writer.writerow([
                    "edge_min", "edge_max", "dens_area", "dens_volume",
                    "aspect_avg", "aspect_worst"
                ])
                writer.writerow(geometry_stats)
                writer.writerow([])

            if performance_stats:
                writer.writerow(["Performance Stats"])
                writer.writerow(["complexity", "memory_use", "load_time", "triangle_rate"])
                writer.writerow(performance_stats)

        print(f"[CSV] Report generated: {file_path}")

    def close(self):
        self.db.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python export.py <model_name.stl>")
        sys.exit(1)

    model_name = sys.argv[1]
    exporter = CSVExporter(model_name)
    try:
        print(f"\n--- Exporting Report for {model_name} ---")
        exporter.export()
        print("--- Export Completed ---")
    finally:
        exporter.close()
