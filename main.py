# main.py
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
import traceback

# Importa funções utilitárias
from utils.pdf_loader import extract_text_from_pdf, extract_text_from_image
from utils.analysis import generate_critical_analysis_full  # ✅ função correta


def _form_bool_flag(value: str | None) -> bool:
    if value is None:
        return False
    return str(value).strip().lower() in ("1", "true", "yes", "on")

# ------------------------------------------------------------
# Configuração principal da API
# ------------------------------------------------------------
app = FastAPI(
    title="IA Acadêmica UFU - ReadWise AI by Rafael Gustavo Nogueira (12511RIT027)",
    description=(
        "Sistema de análise crítica automatizada de textos acadêmicos, "
        "desenvolvido para auxiliar estudos e pesquisas na Universidade Federal de Uberlândia (UFU)."
    ),
    version="1.1.0",
)

# ------------------------------------------------------------
# Middleware para permitir acesso externo (CORS)
# ------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------
# Rota raiz (teste rápido de status)
# ------------------------------------------------------------
@app.get("/")
async def root():
    return {
        "status": "ok",
        "message":  "API da ReadWise AI rodando com sucesso!",
        "author": "Rafael Gustavo Nogueira - 12511RIT027",
    }

# ------------------------------------------------------------
# Upload de arquivo PDF para análise crítica
# ------------------------------------------------------------
@app.post("/upload/")
async def upload_file(
    file: UploadFile = File(...),
    academic_area: str = Form(""),
    exact_sciences: str = Form("false"),
):
    try:
        # Lê o arquivo enviado
        content = await file.read()
        if not content:
            raise HTTPException(status_code=400, detail="Arquivo vazio ou corrompido.")

        print(f"Recebido arquivo: {file.filename} ({len(content)} bytes) tipo={file.content_type}")

        # Decide se é PDF ou imagem
        content_type = (file.content_type or "").lower()
        if content_type.startswith("image/"):
            text = extract_text_from_image(content, mime_type=content_type)
        else:
            text = extract_text_from_pdf(content)

        print(f"Texto extraído com {len(text)} caracteres.")

        # Gera análise crítica detalhada (sem verbose)
        print("Iniciando análise crítica completa...")
        analysis = generate_critical_analysis_full(
            text,
            academic_area=academic_area,
            exact_sciences=_form_bool_flag(exact_sciences),
        )

        print("Análise crítica concluída com sucesso.")
        return {"analysis": analysis}

    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={
                "error": "Erro interno ao processar upload.",
                "details": str(e),
            },
        )

# ------------------------------------------------------------
# Rota para chat interativo com a IA (modo pergunta-resposta)
# ------------------------------------------------------------
@app.post("/chat/")
async def chat_query(
    query: str = Form(...),
    academic_area: str = Form(""),
    exact_sciences: str = Form("false"),
):
    """
    Chat acadêmico IA: interpreta perguntas e responde com base teórica e crítica.
    """
    try:
        if not query or query.strip() == "":
            raise HTTPException(status_code=400, detail="A pergunta não pode estar vazia.")

        print(f"Pergunta recebida: '{query}'")

        # IA responde com base teórica
        response = generate_critical_analysis_full(
            query,
            academic_area=academic_area,
            exact_sciences=_form_bool_flag(exact_sciences),
        )

        print("Resposta gerada com sucesso.")
        return {"response": response}

    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={
                "error": "Erro interno no servidor ao processar o chat IA.",
                "details": str(e),
            },
        )
