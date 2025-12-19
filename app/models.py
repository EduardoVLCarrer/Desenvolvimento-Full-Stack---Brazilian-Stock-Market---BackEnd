from sqlalchemy import String, DateTime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column, Mapped
from datetime import datetime

class Base(DeclarativeBase):
    pass

class AnaliseAcoes(Base):
    __tablename__ = "analise_acoes"
    acao: Mapped[str] = mapped_column(String(5), primary_key=True)
    analise: Mapped[str] = mapped_column(String(3))
    data_analise: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)