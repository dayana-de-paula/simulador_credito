from fastapi import FastAPI, Depends, Form
from sqlalchemy.orm import Session
from app.models import Simulation
from app.schemas import SimulationCreate, SimulationResponse
from app.database import SessionLocal
from app.openai_utils import gerar_resumo, responder_pergunta

app = FastAPI(
    title="Simulador de Empréstimos",
    description="API para simular empréstimos e utilizar IA para fornecer explicações e responder perguntas.",
    version="1.0.0",
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/simular-emprestimo", tags=["Simulações"], summary="Simular Empréstimo", response_model=SimulationResponse)
def simular_emprestimo(
    valor_emprestimo: float = Form(default=100000, description="Valor do empréstimo (R$)"),
    taxa_juros: float = Form(default=1.5, description="Taxa de juros mensal (%)"),
    num_parcelas: int = Form(default=36, description="Número de parcelas"),
    db: Session = Depends(get_db)
):
    """
    Endpoint para calcular os valores de um empréstimo com base no valor, taxa de juros e número de parcelas.
    """
    simulacao_data = SimulationCreate(
        valor_emprestimo=valor_emprestimo,
        taxa_juros=taxa_juros,
        num_parcelas=num_parcelas
    )

    taxa_mensal = simulacao_data.taxa_juros / 100
    valor_parcela = (simulacao_data.valor_emprestimo * taxa_mensal * (1 + taxa_mensal) ** simulacao_data.num_parcelas) / (
        (1 + taxa_mensal) ** simulacao_data.num_parcelas - 1
    )
    valor_total = valor_parcela * simulacao_data.num_parcelas

    simulacao = Simulation(
        valor_emprestimo=simulacao_data.valor_emprestimo,
        taxa_juros=simulacao_data.taxa_juros,
        num_parcelas=simulacao_data.num_parcelas,
        valor_parcela=round(valor_parcela, 2),
        valor_total=round(valor_total, 2),
    )
    db.add(simulacao)
    db.commit()
    db.refresh(simulacao)

    return SimulationResponse(
        valor_emprestimo=simulacao.valor_emprestimo,
        taxa_juros=simulacao.taxa_juros,
        num_parcelas=simulacao.num_parcelas,
        valor_parcela=simulacao.valor_parcela,
        valor_total=simulacao.valor_total,
    )

@app.get("/simulacoes", tags=["Simulações"], summary="Listar Simulações")
async def listar_simulacoes(db: Session = Depends(get_db)):
    """
    Lista todas as simulações de empréstimos registradas no banco de dados.
    """
    simulacoes = db.query(Simulation).all()
    return simulacoes

@app.post("/gerar-resumo", tags=["IA"], summary="Gerar Resumo")
def gerar_resumo_endpoint(
    valor_emprestimo: float = Form(default=100000, description="Valor do empréstimo (R$)"),
    taxa_juros: float = Form(default=1.5, description="Taxa de juros mensal (%)"),
    num_parcelas: int = Form(default=36, description="Número de parcelas")
):
    """
    Gera um resumo explicativo sobre o empréstimo solicitado.
    """
    prompt = (
        f"Explique ao cliente como funcionará o empréstimo de R${valor_emprestimo:.2f} "
        f"em {num_parcelas} parcelas, com uma taxa de juros de {taxa_juros}% ao mês. "
        "Seja direto, amigável e breve, limitando a explicação a no máximo 3 parágrafos. Comece falando: Veja como funcionará seu empréstimo..."
        "Inclua o valor aproximado da parcela e o custo total, destacando qualquer ponto importante de forma resumida."
    )
    resumo = gerar_resumo(prompt)
    return {"resumo": resumo}

@app.post("/pergunta-emprestimo", tags=["IA"], summary="Responder Pergunta")
def responder_pergunta_endpoint(
    pergunta: str = Form(
        default="Como é calculada a taxa de juros do empréstimo?",
        description="Pergunta sobre empréstimos"
    )
):
    """
    Responde a perguntas relacionadas a empréstimos usando IA.
    """
    response = responder_pergunta(pergunta)
    return {"resposta": response}
