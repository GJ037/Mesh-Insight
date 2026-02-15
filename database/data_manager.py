from config import DB_CONFIG
import pymysql


class DataManager:
    """Stores mesh analyzes and stats in Database."""

    def __init__(self):
        try:
            self.conn = pymysql.connect(
                host=DB_CONFIG["host"],
                user=DB_CONFIG["user"],
                password=DB_CONFIG["password"],
                database=DB_CONFIG["database"],
                autocommit=True
            )
            self.cursor = self.conn.cursor()
        except Exception as e:
            raise RuntimeError(f"Database connection failed: {e}")

    def insert_model_stats(self, model_name, model_size):
        try:
            existing_id = self.get_model_id(model_name)

            sql = """
                INSERT INTO model_stats (name, size) VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE size = VALUES(size)
            """
            self.cursor.execute(sql, (model_name, model_size))
            self.conn.commit()

            model_id = self.get_model_id(model_name)
            is_new = existing_id is None
            return model_id, is_new
        except Exception as e:
            raise RuntimeError(f"Failed to insert model '{model_name}': {e}")

    def insert_mesh_stats(self, model_id, stats):
        try:
            sql = """
                REPLACE INTO mesh_stats 
                (model_id, vertices, triangles, surface, volume,
                 bbox_x, bbox_y, bbox_z, center_x, center_y, center_z)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            self.cursor.execute(sql, (
                model_id,
                stats["vertices"],
                stats["triangles"],
                stats["surface"],
                stats["volume"],
                stats["bbox"][0],
                stats["bbox"][1],
                stats["bbox"][2],
                stats["center"][0],
                stats["center"][1],
                stats["center"][2]
            ))
            self.conn.commit()
        except Exception as e:
            raise RuntimeError(f"Failed to insert mesh stats for model {model_id}: {e}")

    def insert_quality_stats(self, model_id, stats):
        try:
            sql = """
                REPLACE INTO quality_stats
                (model_id, uniformity, water_tight, degen_faces, dup_vertices)
                VALUES (%s,%s,%s,%s,%s)
            """
            self.cursor.execute(sql, (
                model_id,
                stats["uniformity"],
                stats["water_tight"],
                stats["degen_faces"],
                stats["dup_vertices"]
            ))
            self.conn.commit()
        except Exception as e:
            raise RuntimeError(f"Failed to insert quality stats for model {model_id}: {e}")

    def insert_geometry_stats(self, model_id, stats):
        try:
            sql = """
                REPLACE INTO geometry_stats
                (model_id, edge_min, edge_max, dens_area, dens_volume, aspect_avg, aspect_worst)
                VALUES (%s,%s,%s,%s,%s,%s,%s)
            """
            self.cursor.execute(sql, (
                model_id,
                stats["edge_min"],
                stats["edge_max"],
                stats["dens_area"],
                stats["dens_volume"],
                stats["aspect_avg"],
                stats["aspect_worst"]
            ))
            self.conn.commit()
        except Exception as e:
            raise RuntimeError(f"Failed to insert geometry stats for model {model_id}: {e}")

    def insert_performance_stats(self, model_id, stats):
        try:
            sql = """
                REPLACE INTO performance_stats
                (model_id, complexity, memory_use, load_time, triangle_rate)
                VALUES (%s,%s,%s,%s,%s)
            """
            self.cursor.execute(sql, (
                model_id,
                stats["complexity"],
                stats["memory_use"],
                stats["load_time"],
                stats["triangle_rate"]
            ))
            self.conn.commit()
        except Exception as e:
            raise RuntimeError(f"Failed to insert performance stats for model {model_id}: {e}")
        
    def get_model_id(self, model_name):
        try:
            sql = "SELECT id FROM model_stats WHERE name = %s"
            self.cursor.execute(sql, (model_name,))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            raise RuntimeError(f"Failed to fetch model ID for '{model_name}': {e}")

    def get_model_name(self):
        try:
            sql = "SELECT name FROM model_stats ORDER BY id DESC"
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except Exception as e:
            raise RuntimeError(f"Failed to fetch model list: {e}")

    def get_model_stats(self, model_name):
        try:
            sql = "SELECT id, name, size FROM model_stats WHERE name = %s"
            self.cursor.execute(sql, (model_name,))
            return self.cursor.fetchone()
        except Exception as e:
            raise RuntimeError(f"Failed to fetch model info for '{model_name}': {e}")

    def get_mesh_stats(self, model_id):
        try:
            sql = """SELECT vertices, triangles, surface, volume,
                     bbox_x, bbox_y, bbox_z, center_x, center_y, center_z
                     FROM mesh_stats WHERE model_id = %s"""
            self.cursor.execute(sql, (model_id,))
            return self.cursor.fetchone()
        except Exception as e:
            raise RuntimeError(f"Failed to fetch mesh stats for model {model_id}: {e}")

    def get_quality_stats(self, model_id):
        try:
            sql = """SELECT uniformity, water_tight, degen_faces, dup_vertices
                     FROM quality_stats WHERE model_id = %s"""
            self.cursor.execute(sql, (model_id,))
            return self.cursor.fetchone()
        except Exception as e:
            raise RuntimeError(f"Failed to fetch quality stats for model {model_id}: {e}")

    def get_geometry_stats(self, model_id):
        try:
            sql = """SELECT edge_min, edge_max, dens_area, dens_volume, aspect_avg, aspect_worst
                     FROM geometry_stats WHERE model_id = %s"""
            self.cursor.execute(sql, (model_id,))
            return self.cursor.fetchone()
        except Exception as e:
            raise RuntimeError(f"Failed to fetch geometry stats for model {model_id}: {e}")

    def get_performance_stats(self, model_id):
        try:
            sql = """SELECT complexity, memory_use, load_time, triangle_rate
                     FROM performance_stats WHERE model_id = %s"""
            self.cursor.execute(sql, (model_id,))
            return self.cursor.fetchone()
        except Exception as e:
            raise RuntimeError(f"Failed to fetch performance stats for model {model_id}: {e}")

    def close(self):
        try:
            self.cursor.close()
            self.conn.close()
        except Exception as e:
            raise RuntimeError(f"Error closing database connection: {e}")
