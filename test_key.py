import os
from openai import OpenAI
print("Chave definida:", bool(os.getenv("OPENAI_API_KEY")))
try:
    client = OpenAI()
    print("Cliente OK!")
except Exception as e:
    print(f"Erro: {e}")
