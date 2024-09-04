from pydantic import BaseModel


class AllItem(BaseModel):
    id: int
    user_id: int
    item_id: int
    price: int
    title: str
    url: str

    class Config:
        orm_mode = True  # Позволяет Pydantic работать с SQLAlchemy моделями