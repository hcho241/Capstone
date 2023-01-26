CREATE DATABASE capstone;

CREATE TABLE address (ID SERIAL PRIMARY KEY, Address VARCHAR(50), City VARCHAR(25), State VARCHAR(25), ZipCode VARCHAR(5));

CREATE TABLE customer (ID SERIAL PRIMARY KEY, FirstName VARCHAR(25), LastName VARCHAR(25), AddressID INT REFERENCES address(ID), Email VARCHAR(50));

CREATE TABLE account (ID SERIAL PRIMARY KEY, AccountNumber VARCHAR(10), CustomerID INT REFERENCES customer(ID), CurrentBalance FLOAT);

DO $$
BEGIN 
    INSERT INTO address (Address, City, State, Zipcode) VALUES ('1234 st', 'Irvine', 'CA', '92612');
    INSERT INTO customer (FirstName, LastName, AddressID, Email) VALUES ('Aaron', 'Smith', 1, 'aarons@gmail.com');
    INSERT INTO account (AccountNumber, CustomerID, CurrentBalance) VALUES ('54621', 1, 1000.00);
END $$;

DO $$
BEGIN 
    INSERT INTO address (Address, City, State, Zipcode) VALUES ('1234 st', 'Irvine', 'CA', '92612');
    INSERT INTO customer (FirstName, LastName, Email) VALUES ('James', 'Smith',  address(ID), 'james@gmail.com');
    INSERT INTO account (AccountNumber, CurrentBalance) VALUES ('12345', customer(ID), 1000.00);
END $$;

DO $$
BEGIN 
    INSERT INTO address (Address, City, State, Zipcode) VALUES ('456 st', 'Irvine', 'CA', '92612');
    INSERT INTO customer (FirstName, LastName, Email) VALUES ('John', 'Smith', 'john@gmail.com') RETURNING id;
    INSERT INTO account (AccountNumber, CurrentBalance) VALUES ('7894', 1000.00) RETURNING id;
END $$;