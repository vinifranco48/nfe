from pydantic import BaseModel

class InvoiceData(BaseModel):
    chave_acesso: str
    categoria: str = "Geral"  # Exemplo: "Veículos", "Serviços", "Compras", etc.
