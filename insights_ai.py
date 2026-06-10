import json
from google import genai

def gerar_metricas(visitas, vendas, preco):
    """Calcula a taxa de conversão e o faturamento com base nos dados informados."""

    taxa_conversao = round( (vendas/visitas) * 100, 2 ) if visitas > 0 else 0

    faturamento = round(vendas * preco, 2)

    return {
        "taxa_conversao": taxa_conversao,
        "faturamento": faturamento
    }

def classificar_conversao(taxa_conversao):
    if taxa_conversao < 1:
        return {
            "texto": "Abaixo da média",
            "classe": "status_baixo"
        }
    
    if taxa_conversao < 3:
        return {
            "texto": "Na média",
            "classe": "status_medio"
        }
    
    return {
            "texto": "Acima da média",
            "classe": "status_alto"
    }

def gerar_insights_gemini(analise):
    """
    Envia os dados calculados da análise para o Gemini e retorna insights personalizados.

    Caso a API falhe ou retorne uma resposta inválida, a função usa um fallback
    para manter o sistema funcionando sem quebrar a experiência do usuário.
    """
    prompt = f"""
Você é um consultor de vendas para pequenos empreendedores e creators.

Gere uma análise específica com base nos dados abaixo. Não use respostas genéricas.

Produto: {analise["produto"]}
Visitas: {analise["visitas"]}
Vendas: {analise["vendas"]}
Preço: R$ {analise["preco"]}
Origem do tráfego: {analise["origem"]}
Taxa de conversão: {analise["taxa_conversao"]}%
Faturamento: R$ {analise["faturamento"]}

Regras:
- Cite pelo menos um número informado.
- Relacione a recomendação com a origem do tráfego.
- Escreva em português do Brasil.
- Seja curto, prático e direto.
- Responda apenas em JSON válido, sem markdown e sem explicações fora do JSON.

Formato exato:
{{
  "pontos_fortes": "...",
  "recomendacoes": "...",
  "otimizacoes": "..."
}}
"""

    try:
        client = genai.Client()

        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt
        )

        texto = response.text.strip()

        if texto.startswith("```json"):
            texto = texto.replace("```json", "").replace("```", "").strip()
        elif texto.startswith("```"):
            texto = texto.replace("```", "").strip()

        print("RESPOSTA GEMINI:", texto)

        return json.loads(texto)

    except Exception as erro:
        print("ERRO AO CHAMAR GEMINI:", repr(erro))

        return {
            "pontos_fortes": f"Fallback usado. Erro Gemini: {type(erro).__name__}",
            "recomendacoes": "Verifique a chave da API, o modelo utilizado e a mensagem exibida no terminal.",
            "otimizacoes": "Se o erro persistir, mantenha insights fixos para preservar a entrega do protótipo."
        }

def preparar_analise(analise, usar_ia=False):
    """
    Combina os dados salvos no banco com métricas calculadas, status visual
    da conversão e, quando solicitado, insights gerados pela IA.
    """
    metricas = gerar_metricas(
        analise["visitas"],
        analise["vendas"],
        analise["preco"]
    )

    status = classificar_conversao(metricas["taxa_conversao"])

    analise_preparada = {
        "id": analise["id"],
        "produto": analise["produto"],
        "visitas": analise["visitas"],
        "vendas": analise["vendas"],
        "preco": analise["preco"],
        "origem": analise["origem"],
        "taxa_conversao": metricas["taxa_conversao"],
        "faturamento": metricas["faturamento"],
        "status_conversao": status["texto"],
        "classe_conversao": status["classe"]
    }

    if usar_ia:
        insights = gerar_insights_gemini(analise_preparada)
    else:
        insights = {
            "pontos_fortes": "Produto apresenta potencial de vendas.",
            "recomendacoes": "Aumentar tráfego qualificado.",
            "otimizacoes": "Testar novos criativos."
        }

    analise_preparada.update(insights)

    return analise_preparada