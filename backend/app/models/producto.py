
from sqlalchemy import Column, Integer, String, Numeric, Boolean, ForeignKey, DateTime, func, Index
from sqlalchemy.orm import relationship
from app.db.base import Base

class Producto(Base):
    __tablename__ = "productos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(120), unique=True, nullable=False)
    precio = Column(Numeric(10, 2), nullable=False)
    categoria_id = Column(Integer, ForeignKey("categorias.id", ondelete="CASCADE"), nullable=False)
    presentacion_id = Column(Integer, ForeignKey("presentaciones.id", ondelete="CASCADE"), nullable=False)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    categoria = relationship("Categoria", backref="productos")
    presentacion = relationship("Presentacion", backref="productos")

Index("ix_productos_nombre_lower", func.lower(Producto.nombre))
