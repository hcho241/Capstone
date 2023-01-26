# app(API) - services - repositories(Sql) - db
import uvicorn
from fastapi import FastAPI
from bank_accounts.models.account import Account 
from bank_accounts.services.account import AccountServices
from bank_accounts.repositories.account import AccountRepository
from bank_accounts.repositories.address import AddressRepository
from bank_accounts.repositories.customer import CustomerRepository
from typing import List 

app = FastAPI()
account_repository = AccountRepository()
address_repository = AddressRepository()
customer_repository = CustomerRepository()
account_service = AccountServices(account_repository, address_repository, customer_repository)

@app.post('/api/accounts')
async def open_account(account: Account) -> Account:
    if account.current_balance < 25.0:
        raise ValueError('Minimum of $25.00 is required to open a new account.')
    return account_service.open_account(account)

@app.get('/api/accounts', response_model=List[Account])
async def retrieve_accounts() -> List[Account]: 
   return account_service.get_all_accounts()

@app.get("/api/accounts/retrieval/{account_number}")
async def retrieve_account_info(account_number: str) -> Account: 
   return account_service.get_account_info(account_number)

# Prevent specification of invalid values (positive decimal numbers only)
# Prevent a withdrawal that would result in an overdraw
@app.put('/api/accounts/{account_number}/withdrawal/{amount}')
async def withdrawal(account_number: str, amount: float) -> Account:
    account = account_service.get_account_info(account_number)
    if amount <= 0.00 :
        raise ValueError('Overdraw --- Enter the withdrawal amount bigger than $0.00')
    elif account.current_balance - amount < 0.00 :
        raise ValueError('Remaining balance will be below $0.00')
    else :
        return account_service.withdrawal(account_number, amount)

# Prevent specification of invalid values (positive decimal numbers only)
@app.put('/api/accounts/{account_number}/deposit/{amount}')
async def deposit(account_number: str, amount: float) -> Account:
    if amount <= 0.00 :
        raise ValueError('Enter the deposit amount bigger than $0.00')
    else :
        return account_service.deposit(account_number, amount)

@app.delete('/api/accounts/{account_number}')
async def delete_account(account_number: str) -> None:
    account_service.delete_account(account_number)

if __name__ == "__main__":
   uvicorn.run("app:app",host="127.0.0.1",port=8080,reload=True) 