import sqlite3
import pandas as pd

# Connecting to the SQLite database
conn = sqlite3.connect('laliga.db')

# Reading data from the 'matches' table
df = pd.read_sql_query("SELECT * FROM matches", conn)

# Showing the first few rows of the DataFrame
print(df)

conn.close()
