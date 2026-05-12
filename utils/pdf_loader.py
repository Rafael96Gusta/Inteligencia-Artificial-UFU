import fitz  # PyMuPDF
import base64
from openai import OpenAI

client = OpenAI()

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


def extract_text_from_image(file_bytes: bytes, mime_type: str = "image/png") -> str:
    """
    Usa a API da OpenAI (modelo com visão) para extrair o texto presente em uma imagem.
    """
    try:
        b64 = base64.b64encode(file_bytes).decode("utf-8")
        data_url = f"data:{mime_type};base64,{b64}"

        resp = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Você extrai texto de imagens. Devolva apenas o texto contido na imagem, em português, sem comentários extras.",
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": "Transcreva todo o texto legível desta imagem.",
                        },
                        {
                            "type": "input_image",
                            "image_url": {
                                "url": data_url,
                            },
                        },
                    ],
                },
            ],
        )

        content = resp.choices[0].message.content or ""
        return content.strip()
    except Exception as e:
        print(f"[ERRO] Falha ao extrair texto da imagem: {e}")
        return ""
