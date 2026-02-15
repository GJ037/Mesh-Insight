from .base_core import BaseCore
import trimesh

class MeshLoader(BaseCore):
    """Handles loading and validation of STL mesh files."""

    def __init__(self, file_name):
        super().__init__(file_name)

    def load(self):
        def load_mesh():
            mesh = trimesh.load(self.file_path)
            
            if isinstance(mesh, trimesh.Scene):
                if not mesh.geometry:
                    raise ValueError("Empty STL scene.")
                mesh = trimesh.util.concatenate(tuple(mesh.geometry.values()))
            if not isinstance(mesh, trimesh.Trimesh):
                raise ValueError("Invalid STL structure.")
            
            self.mesh = mesh
            return mesh

        return self.time(load_mesh)

    def stats(self):
        return {
            "model_name": self.file_name,
            "model_size": self.file_size,
            "load_time": self.load_time
        }
