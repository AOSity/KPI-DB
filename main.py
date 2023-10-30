import psycopg2

# pip freeze > requirements.txt

# Connect to your postgres DB
conn = psycopg2.connect('dbname=postgres user=postgres password=postgres')

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a query
cur.execute('SELECT * FROM "User"')

# Retrieve query results
records = cur.fetchall()

print(records)