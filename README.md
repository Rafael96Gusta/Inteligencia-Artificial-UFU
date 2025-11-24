````markdown
# ReadWise AI – Projeto Alpha de Inteligência Artificial Acadêmica

<p align="center">  
  <img src="docs/logo.png" alt="ReadWise AI Logo" width="200"/>  
</p>

##  Visão Geral

O **ReadWise AI** é uma ferramenta sofisticada de inteligência artificial voltada para o ambiente acadêmico, projetada para transformar textos complexos em conteúdos estruturados, analíticos e orientados para estudo. A versão **Alpha** desse projeto serve como prova de conceito para:

- Realizar **análise crítica** de textos enviados pelo usuário;  
- Extrair **conceitos-chave** e categorias conceituais;  
- Gerar **resumos interpretativos** com profundidade teórica;  
- Propor **planos de estudo personalizados**, adaptados à área de conhecimento especificada (como Relações Internacionais, Sociologia, Economia, etc.).

O sistema tem foco em facilitar a leitura ativa, mapear ideias centrais e organizar caminhos de aprofundamento para pesquisadores, estudantes e profissionais.

---

##  Funcionalidades Principais

1. **Upload ou Input de Texto**  
   Usuários podem colar trechos acadêmicos, capítulos de livros, artigos ou relatórios, que serão processados pela IA.

2. **Parâmetro de Área de Estudo**  
   Permite definir a disciplina ou campo (por exemplo, Relações Internacionais, Direito, Ciências Sociais), ajustando a análise para o jargão e as categorias teóricas específicas.

3. **Análise Argumentativa**  
   A IA identifica a estrutura argumentativa principal, avaliando coerência, proposições, pressupostos e implicações.

4. **Resumo Interpretativo**  
   Gera uma síntese densa e contextualizada, que não é apenas abstrato, mas destaca relações teóricas, tensões e possíveis lacunas.

5. **Conceitos-Chave**  
   Extração de termos centrais, conceitos teóricos, variáveis importantes e suas interrelações.

6. **Plano de Estudos**  
   Sugestão de etapas para aprofundamento: leituras complementares, exercícios de reflexão, tópicos para pesquisa e expansão teórica.

---

##  Arquitetura e Tecnologias

- **Linguagem**: Python  
- **Back-end de IA**: API da OpenAI (chat / completions)  
- **Estrutura modular**: separação entre pré-processamento de texto, análise semântica, síntese e geração de planos  
- **Configuração configurável**: é possível ajustar o “nível de detalhe” do plano de estudos ou da análise

---

2. **Instalar Dependências**

   ```bash
   python3 -m venv venv  
   source venv/bin/activate  
   pip install -r requirements.txt  
   ```

3. **Configurar a API da OpenAI**

   * Crie um arquivo `.env` com sua chave da OpenAI (`OPENAI_API_KEY`).
   * Ajuste, se necessário, parâmetros de modelo, temperatura, limites de tokens etc.

4. **Executar a Análise**

   * Implemente ou use um script de entrada: por exemplo, `analyze_text.py`
   * Envie o texto + parâmetro de área de estudo
   * Receba a análise, resumo e plano de estudos gerados pela IA

---

## Roadmap (Visão Futura):

* **Versão Beta**:

  * Interface web (front-end) para input de texto e visualização de saídas;
  * Histórico de análises;
  * Possibilidade de upload de PDFs / DOCX.

* **Versão Completa**:

  * Exportação de relatórios em PDF / Markdown;
  * Integração com plataformas de estudo (como Notion, Readwise, etc.);
  * Suporte a idiomas adicionais;
  * Ajuste dinâmico de profundidade teórica (por exemplo: “nível de graduação”, “mestrado”, “PhD”).

* **Colaborações e Contribuições**:

  * Adicionar módulos para recomendação bibliográfica automática;
  * Criar agentes de revisão crítica de argumentação;
  * Construir dashboards de métricas de aprendizado (quem usa, quais temas mais estudados, etc.).

---

## Contribuidores

* **Rafael Gustavo Nogueira** — Graduando de Relações Internacionais da Universidade Federal de Uberlândia, idealizador e Dev jr (12511RIT027)
* **@LRV Web** — parceria no desenvolvimento do projeto final / infraestrutura

Se você quiser ajudar com código, testes, documentação ou expansão de funcionalidade, contribuições são bem-vindas.

---

## Licença:

Todos os direitos reservados - LRV Web e Rafael Gustavo Nogueira
