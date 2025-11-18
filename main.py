from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
import traceback

from utils.pdf_loader import extract_text_from_pdf
from utils.analysis import generate_critical_analysis_full 

app = FastAPI(
    title="IA Acadêmica UFU - ReadWise AI by Rafael Gustavo Nogueira (12511RIT027)",
    description=(
        "Sistema de análise crítica automatizada de textos acadêmicos, "
        "desenvolvido para auxiliar estudos e pesquisas na Universidade Federal de Uberlândia (UFU)."
    ),
    version="1.1.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "status": "ok",
        "message": "API da ReadWise AI rodando com sucesso!",
        "author": "Rafael Gustavo Nogueira - 12511RIT027",
    }

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        content = await file.read()
        if not content:
            raise HTTPException(status_code=400, detail="Arquivo vazio ou corrompido.")

        print(f"Recebido arquivo: {file.filename} ({len(content)} bytes)")

        text = extract_text_from_pdf(content)
        print(f"Texto extraído com {len(text)} caracteres.")

        print("Iniciando análise crítica completa...")
        analysis = generate_critical_analysis_full(text)

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

@app.post("/chat/")
async def chat_query(query: str = Form(...)):
    """
    Chat acadêmico IA: interpreta perguntas e responde com base teórica e crítica.
    """
    try:
        if not query or query.strip() == "":
            raise HTTPException(status_code=400, detail="A pergunta não pode estar vazia.")

        print(f"Pergunta recebida: '{query}'")

        response = generate_critical_analysis_full(query)

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
