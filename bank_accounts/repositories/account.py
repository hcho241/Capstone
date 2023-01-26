import psycopg2
from bank_accounts.models.account import Account
from bank_accounts.models.address import Address
from bank_accounts.models.customer import Customer 

class AccountRepository():
    host = "localhost"
    database = "postgres"
    user = "postgres"
    password = "test"

    def insert(self, account: Account): # open account 
        with psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password) as db:
            with db.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO account 
                        (AccountNumber, CustomerID, CurrentBalance) VALUES
                        (%(account_number)s, %(customer_id)s, %(current_balance)s)
                        RETURNING id
                    """, {
                        'account_number': account.account_number,
                        'customer_id': account.customer_id,
                        'current_balance': account.current_balance
                }
                )
                account.id = cursor.fetchone()[0]
        return account

    def get_all_accounts(self) -> list(Account):
        res = []
        with psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password) as db:
            with db.cursor() as cursor:
                cursor.execute("""
                    SELECT * FROM account 
                    """
                )
                rows = cursor.fetchall()
                for row in rows : 
                    customer = Customer(id=row[2], first_name='', last_name='', address_id=row[2], email='')
                    res.append(Account(id=row[0], account_number=row[1], customer=customer, current_balance=round(row[3], 2)))
        return res 

    def get_account_info(self, account_number: str):
        with psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password) as db:
            with db.cursor() as cursor:
                cursor.execute("""
                    SELECT ID, AccountNumber, CustomerID, CurrentBalance FROM account WHERE AccountNumber=%(account_number)s
                    """, {
                        'account_number': account_number
                }
                )
                row = cursor.fetchone()
                if row:
                    customer = Customer(id=row[2], first_name='', last_name='', address_id=row[2], email='')
                    return Account(id=row[0], account_number=row[1], customer=customer, current_balance=round(row[3], 2))
                else:
                    return None

    def update_account(self, account: Account):
        with psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password) as db:
            with db.cursor() as cursor:
                cursor.execute("""
                    UPDATE account SET AccountNumber=%(account_number)s, CustomerID=%(customer_id)s, CurrentBalance=%(current_balance)s WHERE ID=%(id)s
                    """, {
                        'account_number':account.account_number,
                        'customer_id':account.customer_id,
                        'current_balance':account.current_balance,
                        'id': account.id
                }
                )

    def delete_account(self, account_number: str):
        with psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password) as db:
            with db.cursor() as cursor:
                cursor.execute("""
                    DELETE FROM account WHERE AccountNumber=%(account_number)s
                    """, {
                        'account_number': account_number
                }
                )