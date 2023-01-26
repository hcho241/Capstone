import psycopg2
from models.account import Account
from models.address import Address
from models.customer import Customer 

class AddressRepository():
    host = "localhost"
    database = "postgres"
    user = "postgres"
    password = "test"

    def insert(self, address: Address):
        with psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password) as db:
            with db.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO address 
                        (Address, City, State, ZipCode) VALUES
                        (%(address)s, %(city)s, %(state)s, %(zip_code)s)
                        RETURNING id
                    """, {
                    'address':address.address,
                    'city':address.city,
                    'state':address.state,
                    'zipcode':address.zip_code
                }
                )
                address.id = cursor.fetchone()[0]
        return address

    def get_by_id(self, id: int) -> Address:
        with psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password) as db:
            with db.cursor() as cursor:
                cursor.execute("""
                    SELECT * FROM address WHERE ID=%(address_id)s
                    """,{
                        'address_id':id
                    }
                )
                row = cursor.fetchone()
                if row:
                    return Address(id=row[0], address=row[1], city=row[2], state=row[3], zip_code=row[4])
                else:
                    return None 

    def update_address(self, address: Address):
        with psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password) as db:
            with db.cursor() as cursor:
                cursor.execute("""
                    UPDATE adddress SET Address=%(street_address)s, City=%(city)s, State=%(state)s, Zipcode=%(zipcode)s WHERE ID=%(address_id)s
                    """, {
                        'street_address':address.address,
                        'city':address.city,
                        'state':address.state,
                        'zipcode':address.zip_code,
                        'address_id':address.id
                }
                )

    def delete_address(self, id: int):
        with psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password) as db:
            with db.cursor() as cursor:
                cursor.execute("""
                    DELETE FROM address WHERE id=%(address_id)s
                    """, {
                    'address_id':id
                }
                )