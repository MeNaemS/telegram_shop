from sqlalchemy import DateTime, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class BroadcastMessage(Base):
    __tablename__ = "management_broadcastmessage"

    id: Mapped[int] = mapped_column(primary_key=True)
    message: Mapped[str] = mapped_column(Text)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    sent: Mapped[bool] = mapped_column(default=False)
