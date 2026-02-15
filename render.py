from core.mesh_renderer import MeshRenderer
import sys


class RenderRunner:
    """Executes model rendering."""

    def run(filename: str, mode: str):
        renderer = MeshRenderer(filename)
        renderer.render(mode)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python render.py <filename.stl> [mode]")
        sys.exit(1)

    if len(sys.argv) > 3:
        print("Usage: python render.py <filename.stl> [mode]")
        sys.exit(1)
    
    filename = sys.argv[1]
    mode = sys.argv[2]

    RenderRunner.run(filename, mode)
