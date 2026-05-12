from openai import OpenAI

client = OpenAI()

MODEL_NAME = "gpt-5"

DEFAULT_ACADEMIC_AREA = "Relações Internacionais"

BASE_PROMPT = """
Você é uma inteligência analítica acadêmica especializada na área de <{academic_area}> estudos acadêmicos.

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
8. Produza a análise de maneira coesa em relação à área de estudo do usuário.
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

BASE_PROMPT_EXACTAS = """
Você é um tutor acadêmico especializado em áreas de exatas (<{academic_area}>), com foco em prática por exercícios.

Leia o material abaixo. Sua tarefa principal é produzir uma LISTA DE EXERCÍCIOS para fixação e estudo, derivada dos conceitos, definições, exemplos, demonstrações e resultados que aparecem no texto.

Regras para os exercícios:
1. Cada enunciado deve poder ser abordado usando apenas o que está no material (ou consequências imediatas explícitas). Se faltar dado essencial que não conste no texto, declare essa lacuna e não invente valores numéricos nem resultados teóricos externos.
2. Varie os tipos: rápidos de conceito, cálculos com passos, pequenas demonstrações quando o texto permitir, interpretação de dados/gráficos/tabelas se existirem no trecho.
3. Fórmulas e notação: se o texto contiver equações, identidades, leis, expressões algébricas, notação científica ou símbolos matemáticos/físicos/químicos (incluindo LaTeX ou texto linear tipo x^2, ∫, Σ, √), pelo menos metade dos exercícios deve:
   - exigir uso direto ou reorganização dessas expressões;
   - propor substituição de variáveis, isolamento de grandezas ou verificação de unidades/dimensões quando fizer sentido;
   - propor variantes coerentes com os exemplos já dados no texto.
   Se quase não houver fórmulas no material, concentre-se em exercícios conceituais e de modelagem qualitativa estritamente ancorados no que foi lido.

Formato da resposta:
A) Resumo em tópicos do que o material cobre.
B) Lista numerada de exercícios (mínimo 8; aumente se o texto for extenso), cada um com etiqueta de nível [básico], [intermediário] ou [avançado].
C) Seção "Gabarito e comentários": soluções ou dicas; nos itens mais difíceis, guie o raciocínio sem eliminar todo o desafio.
D) Última linha: responda explicitamente: "Todos os enunciados são fiéis ao texto fornecido?" — sim ou não; se não, indique o que ajustar.

Use notação matemática legível (LaTeX entre \\( \\) ou $$ quando ajudar).

Texto:
\"\"\"{text}\"\"\"
"""


def generate_critical_analysis_full(
    text: str,
    academic_area: str | None = None,
    *,
    exact_sciences: bool = False,
) -> str:
    mode = "exatas (exercícios)" if exact_sciences else "humanidades/análise crítica"
    print(f"[IA Acadêmica] Modo: {mode}. Enviando texto ({len(text)} caracteres)...")

    area = (academic_area or "").strip() or DEFAULT_ACADEMIC_AREA
    tpl = BASE_PROMPT_EXACTAS if exact_sciences else BASE_PROMPT
    prompt = tpl.format(academic_area=area, text=text[:120000])

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

   
    output = response.choices[0].message.content

    print("[IA Acadêmica] Análise concluída com sucesso.")
    return output.strip()


# Teste 
if __name__ == "__main__":
    path = "sample_text.txt"
    with open(path, "r", encoding="utf-8") as f:
        txt = f.read()

    result = generate_critical_analysis_full(txt)

    print("\n=== RESULTADO FINAL ===\n")
    print(result[:20000])
