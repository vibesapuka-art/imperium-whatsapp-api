import streamlit as st
import requests
from datetime import datetime
import pandas as pd

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Imperium TV - API Bridge", page_icon="📲")

# --- SEGURANÇA ---
# Defina uma senha que você vai usar no Node.js para ninguém invadir seu Streamlit
API_TOKEN = "ImperiumMaster2026@#" 

st.title("📲 Imperium TV - WhatsApp Bridge")
st.write("Esta página deve ficar ativa para processar os envios do seu painel.")

# --- INICIALIZAÇÃO DO HISTÓRICO ---
if 'historico' not in st.session_state:
    st.session_state.historico = []

# --- CAPTURA DE PARÂMETROS DA URL (Vindo do Render) ---
# Exemplo de chamada: sua-url.streamlit.app/?token=...&number=55...&text=...
params = st.query_params

if "token" in params:
    if params["token"] == API_TOKEN:
        numero = params.get("number")
        mensagem = params.get("text")
        
        if numero and mensagem:
            # Aqui você conectará sua biblioteca de envio
            # Por enquanto, vamos simular o sucesso e registrar no painel
            status_envio = {
                "Horário": datetime.now().strftime("%H:%M:%S"),
                "Número": numero,
                "Status": "✅ Enviado"
            }
            st.session_state.historico.insert(0, status_envio)
            st.toast(f"Mensagem enviada para {numero}!", icon="🚀")
    else:
        st.error("🔒 Token de segurança inválido.")

# --- INTERFACE VISUAL ---
col1, col2 = st.columns(2)
with col1:
    st.metric("Envios Hoje", len(st.session_state.historico))
with col2:
    st.metric("Status do Servidor", "Ativo 🟢")

st.subheader("📋 Logs de Envios Recentes")
if st.session_state.historico:
    df = pd.DataFrame(st.session_state.historico)
    st.table(df)
else:
    st.info("Aguardando o primeiro envio do painel...")

st.divider()
st.caption("Imperium TV - Sistema Próprio de Mensageria v1.0")
