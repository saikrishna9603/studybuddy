import sqlite3

cnx = sqlite3.connect('data/preppulse.db')
cursor = cnx.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = cursor.fetchall()
print('Database Tables:')
for table in tables:
    print(f'  - {table[0]}')
cnx.close()
