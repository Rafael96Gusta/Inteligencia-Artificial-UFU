import fitz  # PyMuPDF

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extrai texto de um arquivo PDF a partir dos bytes.
    Retorna uma string com o conteúdo textual concatenado.
    """
    try:
        with fitz.open(stream=file_bytes, filetype="pdf") as doc:
            text = ""
            for page in doc:
                text += page.get_text("text") or ""
        return text.strip()
    except Exception as e:
        print(f"[ERRO] Falha ao extrair texto do PDF: {e}")
        return ""
