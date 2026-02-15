from .base_analyzer import BaseAnalyzer
import psutil, os

class PerformanceAnalyzer(BaseAnalyzer):
    """Analyzes performance-related mesh properties."""

    def analyze(self) -> dict:
        if self.mesh is None:
            raise RuntimeError("No mesh provided.")

        faces = getattr(self.mesh, "faces", None)
        vertices = getattr(self.mesh, "vertices", None)

        if faces is None or len(faces) == 0:
            raise RuntimeError("Mesh has no faces.")
        if vertices is None or len(vertices) == 0:
            raise RuntimeError("Mesh has no vertices.")

        num_faces = int(len(faces))
        num_vertices = int(len(vertices))

        try:
            process = psutil.Process(os.getpid())
            memory_use = round(process.memory_info().rss / (1024 * 1024), 2)
        except Exception:
            memory_use = 0.0

        complexity = round(0.5 * num_vertices + 0.5 * num_faces, 2)
        triangle_rate = round(num_faces / (self.load_time * 1000.0), 5) if self.load_time > 0 else 0.0

        return {
            "memory_use": memory_use,
            "complexity": complexity,
            "load_time": float(self.load_time),
            "triangle_rate": triangle_rate
        }
