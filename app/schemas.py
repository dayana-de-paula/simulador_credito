from fastapi import Form
from pydantic import BaseModel, Field


class SimulationCreate:
    def __init__(
        self,
        valor_emprestimo: float = Form(..., example=100000),
        taxa_juros: float = Form(..., example=1.5),
        num_parcelas: int = Form(..., example=36),
    ):
        self.valor_emprestimo = valor_emprestimo
        self.taxa_juros = taxa_juros
        self.num_parcelas = num_parcelas


class SimulationResponse(BaseModel):
    valor_emprestimo: float
    taxa_juros: float
    num_parcelas: int
    valor_parcela: float
    valor_total: float

    class Config:
        json_schema_extra = {
            "example": {
                "valor_emprestimo": 100000,
                "taxa_juros": 1.5,
                "num_parcelas": 36,
                "valor_parcela": 3500.50,
                "valor_total": 126018.00,
            }
        }
