import psycopg2
# any code you use to insert into the database - save that code and reuse it 
# if i kill the docker container running postgres, what will happen is that I will
# you will then lose your DB info
# some simple postgresql to insert into the database - write that a script 
# docker run --name postgres -e POSTGRES_PASSWORD=test -p 5432:5432 -d postgres

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="test")

conn.set_session(autocommit=True)
cursor = conn.cursor()

# sannity check - am i actually connected to the database??
# cursor.execute('SELECT * FROM information_schema.tables')

#cursor.execute('CREATE TABLE address (ID SERIAL PRIMARY KEY, Address VARCHAR(50), City VARCHAR(25), State VARCHAR(25), ZipCode VARCHAR(5));')
#cursor.execute('CREATE TABLE customer (ID SERIAL PRIMARY KEY, FirstName VARCHAR(25), LastName VARCHAR(25), AddressID INT REFERENCES address(ID), Email VARCHAR(50));')
#cursor.execute('CREATE TABLE account (ID SERIAL PRIMARY KEY, AccountNumber VARCHAR(10), CustomerID INT REFERENCES customer(ID), CurrentBalance FLOAT);')

cursor.execute('SELECT * FROM information_schema.tables')
rows = cursor.fetchall()
for table in rows:
    print(table)
cursor.close()
conn.close()