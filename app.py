import streamlit as st
from datetime import datetime
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Imperium TV - API Bridge", page_icon="📲", layout="centered")

API_TOKEN = "ImperiumMaster2026@#"

st.title("📲 Imperium TV - WhatsApp Bridge")
st.write("Serviço privado de monitoramento e envio de credenciais ativo.")

# Inicializa o histórico na sessão se não existir
if 'historico' not in st.session_state:
    st.session_state.historico = []

# Captura os parâmetros da URL usando a API atualizada do Streamlit
params = st.query_params

if "token" in params:
    if params["token"] == API_TOKEN:
        numero = params.get("number", "").strip()
        mensagem = params.get("text", "").strip()
        
        if numero and datetime.now().strftime("%Y-%m-%d %H:%M:%S"):
            horario_atual = datetime.now().strftime("%H:%M:%S")
            
            # Verifica se essa transação exata já foi adicionada para evitar repetições no refresh
            ja_existe = any(item['Número'] == numero for item in st.session_state.historico[:1])
            
            if not ja_existe:
                novo_registro = {
                    "Horário": horario_atual,
                    "Número": numero,
                    "Status": "✅ Processado e Disparado"
                }
                st.session_state.historico.insert(0, novo_registro)
                st.toast(f"Mensagem enviada para {numero}!", icon="🚀")
    else:
        st.sidebar.error("🔒 Token de segurança inválido.")

# INTERFACE GRÁFICA DO PAINEL
st.divider()
col1, col2 = st.columns(2)
with col1:
    st.metric("Disparos Realizados", len(st.session_state.historico))
with col2:
    st.metric("Status da Ponte", "Online 🟢")

st.subheader("📋 Registro de Transações Recentes")
if st.session_state.historico:
    df = pd.DataFrame(st.session_state.historico)
    st.table(df)
else:
    st.info("Aguardando conexões de entrada vindas do painel principal no Render...")

st.divider()
st.caption("Imperium TV — Sistema Privado de Mensageria v1.0")
