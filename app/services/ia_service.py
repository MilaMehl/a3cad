import asyncio


import asyncio


async def corrigir_resposta_com_ia(resposta_texto: str, gabarito_texto: str, descricao_avaliacao: str) -> dict:
    """
    Mock: Simula a correção de resposta do aluno usando IA.
    Aguarda 2 segundos e retorna um resultado baseado em palavras-chave.
    TODO: Integrar com OpenAI quando a chave estiver disponível.
    """
    await asyncio.sleep(2)

    texto = resposta_texto.lower()

    if "14" in texto or "perfeito" in texto:
        return {
            "nota": 10.0,
            "feedback": "Excelente! Resolução correta e raciocínio lógico impecável."
        }

    if "não sei" in texto or "errado" in texto:
        return {
            "nota": 0.0,
            "feedback": "Resposta insuficiente. É necessário revisar as operações matemáticas básicas."
        }

    return {
        "nota": 6.5,
        "feedback": "Desenvolvimento parcial. A estrutura está correta, mas houve erro na conclusão final."
    }
