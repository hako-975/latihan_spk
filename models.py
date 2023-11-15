from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass

class SportsCar(Base):
    __tablename__ = "sports_car"
    id: Mapped[int] = mapped_column(primary_key=True)
    brand: Mapped[str] = mapped_column(String(30))
    type: Mapped[str] = mapped_column(String(30))
    country: Mapped[str] = mapped_column(String(30))
    top_speed: Mapped[int] = mapped_column()

    def __repr__(self) -> str:
        return f"SportsCar(brand={self.brand!r}, type={self.type!r})"

class House(Base):
    __tablename__ = 'house'
    id: Mapped[int] = mapped_column(primary_key=True)
    developer: Mapped[str] = mapped_column(String(50))
    lb: Mapped[int] = mapped_column()
    lt: Mapped[int] = mapped_column()
    price: Mapped[int] = mapped_column()

    def __repr__(self) -> str:
        return f"House(id={self.id!r}, developer={self.developer!r})"