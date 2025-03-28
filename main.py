import streamlit as st
import requests
import json
import os

# Configurações iniciais do Streamlit
st.set_page_config(page_title="Processamento de Notas Fiscais", layout="centered")
st.title("Processamento de Notas Fiscais")

# URL da API com fallback para localhost
API_URL = os.getenv("API_URL", "http://api:8000/process_invoice")

# Formulário para entrada de dados
with st.form("invoice_form"):
    chave_acesso = st.text_input("Chave de Acesso da Nota Fiscal", max_chars=44, help="Informe os 44 dígitos da chave de acesso")
    categoria = st.selectbox("Categoria", options=["Geral", "Veículos", "Serviços", "Compras"])
    
    submitted = st.form_submit_button("Processar Nota Fiscal")

if submitted:
    if not chave_acesso or len(chave_acesso) != 44:
        st.error("Por favor, informe uma chave de acesso válida com 44 dígitos.")
    else:
        payload = {
            "chave_acesso": chave_acesso,
            "categoria": categoria
        }
        st.info("Enviando dados para a API...")
        try:
            response = requests.post(API_URL, json=payload)
            if response.status_code == 200:
                data = response.json()
                st.success("Nota fiscal processada com sucesso!")
                st.json(data)  # Exibe a resposta JSON de forma formatada
            else:
                st.error(f"Erro na API: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Erro ao se conectar com a API: {e}")
