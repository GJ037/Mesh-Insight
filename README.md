Mesh Insight ALPHA
3D Model Analyzer – MySQL Edition
-----------------------------------

Mesh Insight is a desktop application for automated analysis,
evaluation, and visualization of 3D STL mesh models.

Features:
- Mesh statistics analysis (vertices, triangles, surface, volume)
- Geometry metrics (edge lengths, density, aspect ratios)
- Quality validation (watertightness, degeneracy, duplicates)
- Performance analysis (load time, memory usage, complexity)
- CSV export
- 3D rendering (Standard and Wireframe mode)
- MySQL-backed data persistence

-----------------------------------
SYSTEM REQUIREMENTS

- Windows 10 or later
- MySQL Server installed and running
- MySQL accessible on localhost
- Default credentials (can be modified in config.py):
    user: root
    password: mysql123
    database: mesh_insight

-----------------------------------
SETUP INSTRUCTIONS

1. Install MySQL Server if not already installed.

2. Open MySQL Command Line Client and run:

   CREATE DATABASE mesh_insight;
   USE mesh_insight;

3. Run the schema file:

   SOURCE schema.sql;

4. Ensure MySQL is running.

5. Open the MeshInsight folder and run:

   MeshInsight.exe

-----------------------------------
FOLDER STRUCTURE

MeshInsight/
    MeshInsight.exe
    models/       ← STL storage
    outputs/      ← CSV exports
    (system DLLs and dependencies)

-----------------------------------
KNOWN LIMITATIONS

- Requires MySQL server (not standalone)
- Rendering opens in separate window
- Large STL files (50MB+) may take longer to process
- CPU-bound mesh computation (no multithreading yet)



