from database.data_manager import DataManager
import sys


class ReportViewer:
    """Displays saved analysis data in a readable report format."""

    def __init__(self, file_name: str):
        self.file_name = file_name
        self.db = DataManager()

    def display(self):
        model = self.db.get_model_stats(self.file_name)
        if not model:
            print(f"No report found for model: {self.file_name}")
            return

        id, name, size = model
        mesh_stats = self.db.get_mesh_stats(id)
        quality_stats = self.db.get_quality_stats(id)
        geometry_stats = self.db.get_geometry_stats(id)
        performance_stats = self.db.get_performance_stats(id)

        print(f"\nReport for Model: {name} (ID: {id})")
        print(f"File Size: {size} bytes")

        if mesh_stats:
            (vertices, triangles, surface, volume, bbox_x, bbox_y, bbox_z,
             center_x, center_y, center_z) = mesh_stats

            print("\n--- Mesh Stats ---")
            print(f"Vertices: {vertices}")
            print(f"Triangles: {triangles}")
            print(f"Surface Area: {surface:.5f}")
            print(f"Volume: {volume:.5f}")
            print(f"Bounding Box: ({bbox_x}, {bbox_y}, {bbox_z})")
            print(f"Center of Mass: ({center_x}, {center_y}, {center_z})")

        if quality_stats:
            (uniformity, water_tight, degen_faces, dup_vertices) = quality_stats
            print("\n--- Quality Stats ---")
            print(f"Area Uniformity: {uniformity:.5f}")
            print(f"Water tight: {water_tight}")
            print(f"Degenerate Faces: {degen_faces}")
            print(f"Duplicate Vertices: {dup_vertices}")

        if geometry_stats:
            (edge_min, edge_max, dens_area, dens_volume,
             aspect_avg, aspect_worst) = geometry_stats

            print("\n--- Geometry Stats ---")
            print(f"Min Edge Length: {edge_min:.5f}")
            print(f"Max Edge Length: {edge_max:.5f}")
            print(f"Polygon Density (per area): {dens_area:.5f}")
            print(f"Polygon Density (per volume): {dens_volume:.5f}")
            print(f"Average Aspect Ratio: {aspect_avg:.5f}")
            print(f"Worst Aspect Ratio: {aspect_worst:.5f}")

        if performance_stats:
            (complexity, memory_use, load_time, triangle_rate) = performance_stats
            print("\n--- Performance Stats ---")
            print(f"Complexity Score: {complexity:.2f}")
            print(f"Memory Use (MB): {memory_use:.2f}")
            print(f"Load Time (s): {load_time:.5f}")
            print(f"Triangle Rate: {triangle_rate:.5f}")

    def close(self):
        self.db.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python report.py <model_name.stl>")
        sys.exit(1)

    model_name = sys.argv[1]
    viewer = ReportViewer(model_name)
    
    try:
        viewer.display()
    finally:
        viewer.close()
