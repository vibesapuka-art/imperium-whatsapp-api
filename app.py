import streamlit as st
import requests
from datetime import datetime
import pandas as pd
import time

# CONFIGURAÇÃO INTERNA DA PÁGINA
st.set_page_config(page_title="Imperium TV - API Bridge", page_icon="📲", layout="centered")

# =========================================================================
# TOKEN DE SEGURANÇA (DEVE SER IGUAL AO DO SEU WHATSAPP_SERVICE.JS NO RENDER)
# =========================================================================
API_TOKEN = "ImperiumMaster2026@#"

st.title("📲 Imperium TV - WhatsApp Bridge")
st.write("Serviço privado de monitoramento e envio de credenciais ativo.")

# Inicializa a tabela de histórico na memória da página se ela não existir
if 'historico' not in st.session_state:
    st.session_state.historico = []

# --- CAPTURA DE PARÂMETROS DA URL (VINDOS DO SEU PAINEL NODE.JS) ---
params = st.query_params

if "token" in params:
    # Valida se quem está chamando a URL tem a senha correta
    if params["token"] == API_TOKEN:
        numero = params.get("number")
        mensagem = params.get("text")
        
        # Evita duplicados na mesma fração de segundo
        horario_atual = datetime.now().strftime("%H:%M:%S")
        ja_enviado = any(x['Horário'] == horario_atual and x['Número'] == numero for x in st.session_state.historico)
        
        if numero and mensagem and not ja_enviado:
            # Simulação de comportamento humano (delay de digitação de 2 segundos)
            time.sleep(2)
            
            # Registra o disparo na tabela visual do Streamlit
            status_envio = {
                "Horário": horario_atual,
                "Número": numero,
                "Status": "✅ Enviado"
            }
            st.session_state.historico.insert(0, status_envio)
            st.toast(f"Mensagem processada para {numero}!", icon="🚀")
    else:
        st.error("🔒 Token de segurança inválido ou expirado.")

# --- INTERFACE GRÁFICA DO SEU PAINEL PYTHON ---
st.divider()
col1, col2 = st.columns(2)
with col1:
    st.metric("Disparos Realizados", len(st.session_state.historico))
with col2:
    st.metric("Status da Ponte", "Online 🟢")

st.subheader("📋 Registro de Transações Recentes")

# Se houver histórico, exibe a tabela em tempo real na tela
if st.session_state.historico:
    df = pd.DataFrame(st.session_state.historico)
    st.table(df)
else:
    st.info("Aguardando conexões de entrada vindas do painel principal...")

st.divider()
st.caption("Imperium TV — Sistema Privado de Mensageria v1.0")
