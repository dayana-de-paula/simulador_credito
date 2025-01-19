from sqlalchemy import Column, Integer, Float
from app.database import Base

class Simulation(Base):
    __tablename__ = "simulacoes"

    id = Column(Integer, primary_key=True, index=True)
    valor_emprestimo = Column(Float, nullable=False)
    taxa_juros = Column(Float, nullable=False)
    num_parcelas = Column(Integer, nullable=False)
    valor_parcela = Column(Float, nullable=False)
    valor_total = Column(Float, nullable=False)
