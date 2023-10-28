from pydantic import BaseModel


class Product(BaseModel):
    store: str = 'store'
    title: str = 'title'
    price: str = 'price'
    price_kg: str = 'price_kg'

