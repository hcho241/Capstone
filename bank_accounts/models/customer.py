from pydantic import BaseModel
from bank_accounts.models.address import Address

class Customer(BaseModel):
    id: int
    first_name: str 
    last_name: str
    address: Address
    address_id: int
    email: str