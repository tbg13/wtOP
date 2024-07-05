import os, duckdb

db_file = "database.duckdb"
full_path = "./" + db_file

conn = duckdb.connect(full_path)
conn.close()

print(f"DuckDB database created at {full_path}")
