
from sqlalchemy import Column, Integer, String, Text, DateTime, func, Index
from app.db.base import Base

class Categoria(Base):
    __tablename__ = "categorias"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, nullable=False)
    descripcion = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

Index("ix_categorias_nombre_lower", func.lower(Categoria.nombre))
