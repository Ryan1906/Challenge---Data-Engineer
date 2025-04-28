import sqlite3
import pandas as pd

# Conectar
conn = sqlite3.connect('laliga.db')

# Leer tabla
df = pd.read_sql_query("SELECT * FROM matches", conn)

# Mostrar
print(df)

# Cerrar conexión
conn.close()
