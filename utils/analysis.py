from openai import OpenAI

client = OpenAI()

MODEL_NAME = "gpt-5"

BASE_PROMPT = """
Você é uma inteligência analítica acadêmica especializada na área de <Relações Internacionais> estudos acadêmicos.

Leia atentamente o texto a seguir e produza uma análise crítica densa e fundamentada.
A análise deve incluir:
1. Resumo interpretativo: síntese das ideias centrais, com foco na coerência interna.
2. Citações literais: use trechos curtos presentes no texto fornecido entre aspas para sustentar interpretações.
3. Referências teóricas: relacione com autores, escolas de pensamento e teorias relevantes.
4. Análise crítica: destaque contribuições, limitações e contradições conceituais, políticas ou epistemológicas.
5. Debate contemporâneo: situe o texto em debates atuais dentro das áreas de estudo indicadas.
6. Conclusão verificável: finalize respondendo:  
   “Todas as afirmações presentes na resposta são verificáveis, apoiadas em fontes reais e confiáveis?”
   Se não, indique o que faltaria.
7. Referências bibliográficas: liste todas as fontes acadêmicas citadas na análise, seguindo normas ABNT. 
8. Produza a analise de maneira coesa em relação à área de estudo do úsuario.
9. Resumo final: elabore um resumo final para estudos do livro, DEVE conter conceitos chaves, fundamentação/escola teórica e DESEJAVEL um "mapa mental" para estudos.

Diretrizes obrigatórias:    
- Nunca invente ou especule.
- Baseie todas as afirmações em fontes acadêmicas verificáveis.
- Declare claramente quando “não é possível confirmar” algo.
- Priorize precisão e fundamentação teórica em detrimento da fluidez textual.

Agora leia o texto a seguir:

Texto:
\"\"\"{text}\"\"\"
"""

def generate_critical_analysis_full(text: str) -> str:
    """
    Gera uma análise crítica completa do texto inteiro, sem dividir em chunks.
    """
    print(f"[IA Acadêmica] Enviando texto completo ({len(text)} caracteres) para análise...")

    prompt = BASE_PROMPT.format(text=text[:120000])  #128k tokens

    response = client.responses.create(
        model=MODEL_NAME,
        input=prompt
    )

    # Extrai o texto da resposta
    output = ""
    if hasattr(response, "output") and response.output:
        for item in response.output:
            if getattr(item, "content", None):
                for c in item.content:
                    if getattr(c, "text", None):
                        output += c.text + "\n"
    elif getattr(response, "text", None):
        output = response.text

    print("[IA Acadêmica]  Análise concluída com sucesso.")
    return output.strip()


# Test
if __name__ == "__main__":
    path = "sample_text.txt"
    with open(path, "r", encoding="utf-8") as f:
        txt = f.read()
    result = generate_critical_analysis_full(txt)
    print("\n=== RESULTADO FINAL ===\n")
    print(result[:20000])
