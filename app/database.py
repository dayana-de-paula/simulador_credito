from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decouple import config

# Carregar a URL do banco de dados a partir do arquivo .env
DATABASE_URL = config("DATABASE_URL")

# Criação do motor do SQLAlchemy
engine = create_engine(DATABASE_URL)

# Sessão do banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos do SQLAlchemy
Base = declarative_base()
