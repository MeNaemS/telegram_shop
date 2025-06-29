from sqlalchemy import BigInteger, DateTime, ForeignKey, String, Text, func, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from decimal import Decimal
from .base import Base
from .products import Product


class Cart(Base):
    __tablename__ = "management_cart"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now())

    items: Mapped[List["CartItem"]] = relationship(back_populates="cart", cascade="all, delete-orphan")


class CartItem(Base):
    __tablename__ = "management_cartitem"

    id: Mapped[int] = mapped_column(primary_key=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey("management_cart.id", ondelete="CASCADE"))
    product_id: Mapped[int] = mapped_column(ForeignKey("management_product.id", ondelete="CASCADE"))
    quantity: Mapped[int] = mapped_column(default=1)

    cart: Mapped["Cart"] = relationship(back_populates="items")
    product: Mapped["Product"] = relationship()


class Order(Base):
    __tablename__ = "management_order"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    full_name: Mapped[str] = mapped_column(String(255))
    address: Mapped[str] = mapped_column(Text)
    phone: Mapped[str] = mapped_column(String(50))
    payment_method: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now())

    items: Mapped[List["OrderItem"]] = relationship(back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "management_orderitem"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("management_order.id", ondelete="CASCADE"))
    product_id: Mapped[int] = mapped_column(ForeignKey("management_product.id", ondelete="RESTRICT"))
    quantity: Mapped[int]
    price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))

    order: Mapped["Order"] = relationship(back_populates="items")
    product: Mapped["Product"] = relationship()
