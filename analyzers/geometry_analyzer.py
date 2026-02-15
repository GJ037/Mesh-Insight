from .base_analyzer import BaseAnalyzer
import numpy as np

class GeometryAnalyzer(BaseAnalyzer):
    """Analyzes geometric mesh properties."""

    def analyze(self) -> dict:
        if self.mesh is None:
            raise RuntimeError("No mesh provided.")

        vertices = getattr(self.mesh, "vertices", None)
        faces = getattr(self.mesh, "faces", None)

        if vertices is None or len(vertices) == 0:
            raise RuntimeError("Mesh has no vertices.")
        if faces is None or len(faces) == 0:
            raise RuntimeError("Mesh has no faces.")

        try:
            edge_lengths = np.concatenate([
                np.linalg.norm(vertices[faces[:, 0]] - vertices[faces[:, 1]], axis=1),
                np.linalg.norm(vertices[faces[:, 1]] - vertices[faces[:, 2]], axis=1),
                np.linalg.norm(vertices[faces[:, 2]] - vertices[faces[:, 0]], axis=1)
            ])
            edge_min = float(np.min(edge_lengths)) if len(edge_lengths) > 0 else 0.0
            edge_max = float(np.max(edge_lengths)) if len(edge_lengths) > 0 else 0.0
        except Exception:
            edge_min, edge_max = 0.0, 0.0

        area = float(getattr(self.mesh, "area", 1.0)) or 1.0
        volume = float(getattr(self.mesh, "volume", 1.0)) or 1.0

        dens_area = float(len(faces) / area)
        dens_volume = float(len(faces) / volume)

        aspect_ratios = []
        for face in faces:
            try:
                v0, v1, v2 = vertices[face]
                a = np.linalg.norm(v0 - v1)
                b = np.linalg.norm(v1 - v2)
                c = np.linalg.norm(v2 - v0)
                longest = max(a, b, c)
                shortest = min(a, b, c)
                ratio = longest / shortest if shortest > 0 else 0
                aspect_ratios.append(ratio)
            except Exception:
                continue

        aspect_avg = float(np.mean(aspect_ratios)) if len(aspect_ratios) > 0 else 0.0
        aspect_worst = float(np.max(aspect_ratios)) if len(aspect_ratios) > 0 else 0.0

        return {
            "edge_min": round(edge_min, 5),
            "edge_max": round(edge_max, 5),
            "dens_area": round(dens_area, 5),
            "dens_volume": round(dens_volume, 5),
            "aspect_avg": round(aspect_avg, 5),
            "aspect_worst": round(aspect_worst, 5),
        }
