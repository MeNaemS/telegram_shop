from sqlalchemy import Text, BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class FAQ(Base):
    __tablename__ = "management_faq"

    id: Mapped[int] = mapped_column(primary_key=True)
    question: Mapped[str] = mapped_column(Text)
    answer: Mapped[str] = mapped_column(Text)


class UserSubscription(Base):
    __tablename__ = "management_usersubscription"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    is_subscribed: Mapped[bool] = mapped_column(default=False)
