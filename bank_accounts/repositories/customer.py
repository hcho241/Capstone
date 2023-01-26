import psycopg2
from models.account import Account
from models.address import Address
from models.customer import Customer 

class CustomerRepository():
    host = "localhost"
    database = "postgres"
    user = "postgres"
    password = "test"

    def insert(self, customer: Customer):
        with psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password) as db:
            with db.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO customer 
                        (FirstName, LastName, AddressID, Email) VALUES
                        (%(first_name)s, %(last_name)s, %(address_id)s, %(email)s)
                        RETURNING id
                    """, {
                        'first_name':customer.first_name,
                        'last_name':customer.last_name,
                        'address_id':customer.address_id,
                        'email':customer.email
                }
                )
                customer.id = cursor.fetchone()[0]
        return customer

    def get_by_id(self, id: int):
        with psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password) as db:
            with db.cursor() as cursor:
                cursor.execute("""
                    SELECT * FROM customer WHERE ID=%(customer_id)s
                    """,{
                        'customer_id':id,
                    }
                )
                row = cursor.fetchone()
                if row:
                    address = Address(id=row[3], address='', city='', state='', zip_code='')
                    return Customer(id=row[0], first_name=row[1], last_name=row[2], address=address, email=row[4])
                else:
                    return None 

    def update_customer(self, customer: Customer):
        with psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password) as db:
            with db.cursor() as cursor:
                cursor.execute("""
                    UPDATE customer SET FirstName=%(first_name)s, LastName=%(last_name)s, AddressID=%(address_id)s, Email=%(email)s WHERE ID=%(id)s
                    """, {
                        'first_name':customer.first_name,
                        'last_name':customer.last_name,
                        'address_id':customer.address_id,
                        'email':customer.email,
                        'id': customer.id
                }
                )

    def delete_customer(self, id: int):
        with psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password) as db:
            with db.cursor() as cursor:
                cursor.execute("""
                    DELETE FROM customer WHERE id=%(id)s
                    """, {
                    'id':id
                }
                )