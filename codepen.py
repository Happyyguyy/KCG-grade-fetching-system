import sqlite3

db = sqlite3.connect("db.db")
cur = db.cursor()

cur.execute("DROP TABLE test")
cur.execute("CREATE TABLE test (val1 INT PRIMARY KEY NOT NULL, val2 INT)")
cur.execute("INSERT INTO test (val1,val2) VALUES ('e',4);")
cur.execute("INSERT INTO test (val1,val2) VALUES (2,4);")
db.commit()

for row in cur.execute("SELECT * FROM test"):
    print(row)
