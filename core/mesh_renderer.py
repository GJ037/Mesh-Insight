from .base_core import BaseCore
from vispy import scene, app
import trimesh


class MeshRenderer(BaseCore):
    """Handles visualization of 3D models."""

    def __init__(self, filename: str):
        super().__init__(filename)

    def render(self, mode: str = "standard"):
        mesh = trimesh.load(self.file_path)

        if isinstance(mesh, trimesh.Scene):
            if not mesh.geometry:
                raise ValueError("Empty STL scene.")
            mesh = trimesh.util.concatenate(tuple(mesh.geometry.values()))

        if not isinstance(mesh, trimesh.Trimesh):
            raise ValueError("Invalid STL structure.")

        canvas = scene.SceneCanvas(keys='interactive', show=True, bgcolor='black')
        view = canvas.central_widget.add_view()
        view.camera = 'arcball'

        vertices = mesh.vertices
        faces = mesh.faces

        if mode == "standard":
            mesh_visual = scene.visuals.Mesh(vertices=vertices, faces=faces, color=(0.6, 0.6, 0.9, 1.0), shading='smooth')
            view.add(mesh_visual)

        elif mode == "wireframe":
            edges = mesh.edges_unique
            lines = scene.visuals.Line(pos=vertices[edges].reshape(-1, 3), color='white', connect='segments', width=1.0)
            view.add(lines)

        else:
            raise ValueError(f"Unknown render mode: {mode}")

        view.camera.set_range()
        app.run()
