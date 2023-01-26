from bank_accounts.models.account import Account
from bank_accounts.repositories.account import AccountRepository
from bank_accounts.repositories.address import AddressRepository
from bank_accounts.repositories.customer import CustomerRepository

class AccountServices():
    def __init__(self, account_repository : AccountRepository, address_repository : AddressRepository, customer_repository : CustomerRepository) -> None:
        self.account_repository = AccountRepository
        self.address_repository = AddressRepository
        self.customer_repository = CustomerRepository

    def open_account(self, account: Account) -> Account:
        address = self.address_repository.insert(account.customer.address) 
        account.customer.address = address
        customer = self.customer_repository.insert(account.customer) 
        account.customer = customer 
        return self.account_repository.insert(account)

    def get_all_accounts(self) -> 'list[Account]' :
        accounts = self.account_repository.get_all_accounts()
        for account in accounts :
            account.customer = self.customer_repository.get_by_id(account.customer.id)
            account.customer.address = self.address_repository.get_by_id(account.customer.address.id)
        return accounts

    def get_account_info(self, account_number: str) -> Account :
        account = self.account_repository.get_account_info(account_number) 
        account.customer = self.customer_repository.get_by_id(account.customer.id)
        account.customer.address = self.address_repository.get_by_id(account.customer.address.id)
        return account 

    def withdrawal(self, account_number: str, withdrawal_amount: float) :
        account = self.account_repository.get_account_info(account_number)
        account.current_balance -= withdrawal_amount
        self.account_repository.withdrawal(account_number, withdrawal_amount) 
        return self.get_account_info(account_number) 

    def deposit(self, account_number: str, deposit_amount: float) :
        account = self.account_repository.get_account_info(account_number)  
        account.current_balance += deposit_amount
        self.account_repository.deposit(account_number, deposit_amount)     
        return self.get_account_info(account_number) 

    def delete_account(self, account_number: str) -> Account:
        account = self.get_account_info(account_number)  
        self.account_repository.delete_account(account_number)  
        self.customer_repository.delete_customer(account.customer.id)  
        self.address_repository.delete_address(account.customer.address.id)  