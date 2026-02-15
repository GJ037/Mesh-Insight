class BaseAnalyzer:
    """Base class providing common initialization for all analyzers."""

    def __init__(self, mesh=None, filepath=None, load_time=0.0, render_stats=None):
        self.mesh = mesh
        self.filepath = filepath
        self.load_time = load_time
        self.render_stats = render_stats

    def analyze(self) -> dict:
        """Must be implemented by all derived analyzers."""
        raise NotImplementedError("Subclasses must implement analyze()")
