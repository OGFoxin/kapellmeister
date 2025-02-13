from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

# alchemy
class TickerModel(Base):
    __tablename__ = 'tickers'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    current_price: Mapped[float]

# pydentic
class TickerSchema(BaseModel):
    name: str
    current_price: float

class TickerGetSchema(BaseModel):
    id: int