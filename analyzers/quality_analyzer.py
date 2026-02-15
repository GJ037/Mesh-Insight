from .base_analyzer import BaseAnalyzer
import numpy as np

class QualityAnalyzer(BaseAnalyzer):
    """Analyzes mesh quality metrics."""

    def analyze(self) -> dict:
        if self.mesh is None:
            raise RuntimeError("No mesh provided.")

        vertices = getattr(self.mesh, "vertices", None)
        if vertices is None or len(vertices) == 0:
            raise RuntimeError("Mesh has no vertices.")

        face_areas = getattr(self.mesh, "area_faces", None)
        if face_areas is None or len(face_areas) == 0:
            raise RuntimeError("Mesh has no face area information.")

        mean_area = np.mean(face_areas)
        uniformity = round(float(np.std(face_areas) / mean_area), 5) if mean_area > 0 else 0.0

        water_tight = bool(getattr(self.mesh, "is_watertight", False))
        degen_faces = int(np.sum(face_areas < 1e-12))
        dup_vertices = int(len(vertices) - len(np.unique(vertices.round(6), axis=0)))

        return {
            "uniformity": uniformity,
            "water_tight": water_tight,
            "degen_faces": degen_faces,
            "dup_vertices": dup_vertices
        }
