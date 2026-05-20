import streamlit as st
import requests
from datetime import datetime
import pandas as pd
import time

# CONFIGURAÇÃO INTERNA DA PÁGINA
st.set_page_config(page_title="Imperium TV - API Bridge", page_icon="📲", layout="centered")

# =========================================================================
# 1. SUAS CONFIGURAÇÕES DE SEGURANÇA E INTEGRADOR DE WHATSAPP
# =========================================================================
API_TOKEN = "ImperiumMaster2026@#"

# Aqui usamos um gateway open-source estável e gratuito para o envio
GATEWAY_URL = "https://api.z-api.io/instances/SUA_INSTANCIA/token/SEU_TOKEN/send-text"
# Nota: Se você preferir usar qualquer outro gateway gratuito ou o seu próprio
# servidor HTTP de WhatsApp futuramente, basta trocar essa URL acima.
# =========================================================================

st.title("📲 Imperium TV - WhatsApp Bridge")
st.write("Serviço privado de monitoramento e envio de credenciais ativo.")

# Inicializa a tabela de histórico na memória da página se ela não existir
if 'historico' not in st.session_state:
    st.session_state.historico = []

# --- FUNÇÃO INTERNA DE DISPARO REAL ---
def disparar_whatsapp_real(numero_destino, texto_mensagem):
    """ Envia a mensagem de forma assíncrona usando o motor do chip conectado """
    payload = {
        "phone": numero_destino,
        "message": texto_mensagem
    }
    headers = {
        "Content-Type": "application/json"
    }
    try:
        # Envia a requisição de parto para o chip entregar ao cliente
        resposta = requests.post(GATEWAY_URL, json=payload, headers=headers, timeout=8)
        if resposta.status_code == 200 or resposta.status_code == 201:
            return "✅ Enviado"
        return "❌ Erro no Gateway"
    except Exception as e:
        return f"❌ Falha: {str(e)}"

# --- CAPTURA DE PARÂMETROS DA URL (VINDOS DO SEU PAINEL NODE.JS NO RENDER) ---
params = st.query_params

if "token" in params:
    # Valida se quem está chamando a URL tem a senha correta
    if params["token"] == API_TOKEN:
        numero = params.get("number")
        mensagem = params.get("text")
        
        # Evita disparos duplicados na mesma fração de segundo
        horario_atual = datetime.now().strftime("%H:%M:%S")
        ja_enviado = any(x['Horário'] == horario_atual and x['Número'] == numero for x in st.session_state.historico)
        
        if numero and list(params.keys()) and not ja_enviado:
            # Simulação de comportamento humano (delay de digitação de 2 segundos)
            time.sleep(2)
            
            # CHAMA O MOTOR DE ENVIO REAL
            resultado_envio = disparar_whatsapp_real(numero, mensagem)
            
            # Registra o disparo na tabela visual do Streamlit com o status real
            status_envio = {
                "Horário": horario_atual,
                "Número": numero,
                "Status": resultado_envio
            }
            st.session_state.historico.insert(0, status_envio)
            
            if "✅" in resultado_envio:
                st.toast(f"Mensagem enviada para {numero}!", icon="🚀")
            else:
                st.toast(f"Falha ao entregar para {numero}", icon="⚠️")
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
    st.info("Aguardando conexões de entrada vindas do painel principal no Render...")

st.divider()
st.caption("Imperium TV — Sistema Privado de Mensageria v1.0")
