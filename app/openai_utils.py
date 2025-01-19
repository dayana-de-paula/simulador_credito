from openai import OpenAI
from decouple import config

client = OpenAI(api_key=config("OPENAI_API_KEY"))

def gerar_resumo(prompt: str) -> str:
    """
    Função para gerar um resumo explicativo sobre empréstimos.
    """
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",  
            messages=[
                {"role": "system", "content": "Você é um assistente especializado em finanças."},
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Erro ao gerar resposta: {str(e)}"


def responder_pergunta(pergunta: str) -> str:
    """
    Função para responder perguntas relacionadas a empréstimos.
    """
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",  
            messages=[
                {"role": "system", "content": "Você é um assistente financeiro especializado em empréstimos."},
                {"role": "user", "content": pergunta}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Erro ao responder pergunta: {str(e)}"
