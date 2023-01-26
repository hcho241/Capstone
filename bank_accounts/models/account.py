from pydantic import BaseModel
from bank_accounts.models.customer import Customer

class Account(BaseModel):
    id: int
    account_number: str 
    customer: Customer
    customer_id: int
    current_balance: float 