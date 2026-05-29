import asyncio


async def corrigir_resposta_com_ia(resposta_texto: str, gabarito_texto: str, descricao_avaliacao: str) -> dict:
    """
    Mock: Simula a correção de resposta do aluno usando IA.
    Aguarda 2 segundos e retorna um JSON estático.
    TODO: Integrar com OpenAI quando a chave estiver disponível.
    """
    await asyncio.sleep(2)

    return {
        "nota": 8.5,
        "feedback": "Resposta estruturada corretamente, mas faltou aprofundar no conceito central."
    }
