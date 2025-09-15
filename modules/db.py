import psycopg2

con = psycopg2.connect(host="localhost", dbname="db_test", user="postgres", password="1234", port="5432")

cur = con.cursor()

cur.execute("""
insert into users(id, username, cargo) values (3, 'ssh login failed', '19:20')

""")

cur.execute("""
    SELECT * FROM users
""")


selectExport = []

for row in cur.fetchall():
    selectExport.append(row)
    print(row)

def exportSelect():
    return selectExport

con.commit()
cur.close()
con.close()