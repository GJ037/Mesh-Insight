from .base_analyzer import BaseAnalyzer

class MeshAnalyzer(BaseAnalyzer):
    """Analyzes general mesh properties."""

    def analyze(self) -> dict:
        if self.mesh is None:
            raise RuntimeError("No mesh provided.")

        vertices = getattr(self.mesh, "vertices", None)
        if vertices is None or len(vertices) == 0:
            raise RuntimeError("Mesh has no vertices.")
        vertices = int(len(vertices))

        triangles = getattr(self.mesh, "triangles", None)
        if triangles is None or len(triangles) == 0:
            raise RuntimeError("Mesh has no faces.")
        triangles = int(len(triangles))

        surface = float(getattr(self.mesh, "area", 0.0))
        volume = float(getattr(self.mesh, "volume", 0.0))

        try:
            bbox_extents = getattr(self.mesh, "bounding_box", None)
            if bbox_extents is not None and hasattr(bbox_extents, "extents"):
                bbox = tuple(round(float(x), 5) for x in bbox_extents.extents)
            else:
                bbox = (0.0, 0.0, 0.0)
        except Exception:
            bbox = (0.0, 0.0, 0.0)

        try:
            center = getattr(self.mesh, "center_mass", None)
            if center is not None and len(center) == 3:
                center = tuple(round(float(x), 5) for x in center)
            else:
                center = (0.0, 0.0, 0.0)
        except Exception:
            center = (0.0, 0.0, 0.0)

        return {
            "vertices": vertices,
            "triangles": triangles,
            "surface": round(surface, 5),
            "volume": round(volume, 5),
            "bbox": bbox,
            "center": center,
        }
