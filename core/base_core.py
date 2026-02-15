from config import MODEL_DIR
import os, time


class BaseCore:
    """Base structure for mesh loaders with validation and timing."""
    
    def __init__(self, file_name: str):
        self.mesh = None
        self.scene = None
        self.file_size = None
        self.load_time = None

        try:
            if os.path.isabs(file_name):
                self.file_path = file_name
                self.file_name = os.path.basename(file_name)
            else:
                base_dir = os.path.dirname(__file__)
                model_dir = os.path.join(base_dir, "..", MODEL_DIR)
                self.file_path = os.path.join(model_dir, file_name)
                self.file_name = file_name

        except Exception as e:
            raise RuntimeError(f"Initialization failed for '{file_name}': {e}")

        if not self.file_path.lower().endswith(".stl"):
            raise ValueError("Unsupported format: Only STL files supported.")
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File not found: {os.path.abspath(self.file_path)}")
        self.file_size = os.path.getsize(self.file_path)

    def time(self, func):
        start = time.perf_counter()
        result = func()
        end = time.perf_counter()
        self.load_time = round(end - start, 5)
        return result
