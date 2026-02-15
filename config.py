import os
import sys

# Detect base path
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Database Configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "YOUR PASSWORD",
    "database": "mesh_insight",
    "port": 3306,
}

# General Settings
MODEL_DIR = os.path.join(BASE_DIR, "models")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
