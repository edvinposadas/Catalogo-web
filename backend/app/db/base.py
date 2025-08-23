
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:Posadas123@localhost:5432/catalogoweb")

engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)
Base = declarative_base()

def init_db():
    from app.models.user import User  # noqa: F401
    from app.models.categoria import Categoria  # noqa: F401
    from app.models.presentacion import Presentacion  # noqa: F401
    from app.models.producto import Producto  # noqa: F401
    Base.metadata.create_all(bind=engine)
