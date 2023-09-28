import sqlite3
import psycopg2

# Connect to the SQLite database
sqlite_conn = sqlite3.connect('C:/Users/Ishaan/Documents/Text to SQL/dev_20230613/dev_databases/thrombosis_prediction/thrombosis_prediction.sqlite')
sqlite_cursor = sqlite_conn.cursor()

# Connect to the PostgreSQL database
pg_conn = psycopg2.connect(
    dbname='thrombosis_prediction',
    user='postgres',
    password='root',
    host='localhost',
    port='5432'
)
pg_cursor = pg_conn.cursor()

# Define a list of tables in the order you want to insert data
# You need to determine this order based on your foreign key constraints
table_order = ['Patient', 'Examination', 'Laboratory']

# Iterate through tables and transfer data
sqlite_cursor.execute(f"SELECT ID FROM Patient")
rows = sqlite_cursor.fetchall()
r = []
for row in rows:
    r.append(row[0])

print(r)
# Extract data from SQLite
sqlite_cursor.execute(f"SELECT * FROM Examination")
rows = sqlite_cursor.fetchall()



# PostgreSQL INSERT query
insert_query = """
INSERT INTO Examination (
    ID, "Examination Date", "aCL IgG", "aCL IgM", ANA, "ANA Pattern", "aCL IgA",
    Diagnosis, KCT, RVVT, LAC, Symptoms, Thrombosis
) VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
);
"""


# Iterate over rows and insert into PostgreSQL
used = set()
for row in rows:
    if row[0] in r and row[0] not in used:
        used.add(row[0])
        pg_cursor.execute(insert_query, row)
    else:
        print("FK Error")


# Commit changes and close connections
pg_conn.commit()
pg_cursor.close()
pg_conn.close()

sqlite_cursor.close()
sqlite_conn.close()
