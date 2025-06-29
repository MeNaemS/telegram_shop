from sqlalchemy import ForeignKey, String, Text, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from decimal import Decimal
from .base import Base


class Category(Base):
    __tablename__ = "management_category"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    
    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("management_category.id", ondelete="CASCADE"), nullable=True)
    parent: Mapped[Optional["Category"]] = relationship("Category", remote_side=[id], back_populates="subcategories")
    subcategories: Mapped[List["Category"]] = relationship("Category", back_populates="parent")

    def __str__(self):
        return self.name


class Product(Base):
    __tablename__ = "management_product"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text, default="", nullable=True)
    image: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    category_id: Mapped[int] = mapped_column(ForeignKey("management_category.id", ondelete="RESTRICT"))

    category: Mapped["Category"] = relationship(backref="products")

    def __str__(self):
        return self.name
