import streamlit as st
import requests

st.set_page_config(page_title="Imperium TV - API Gateway", layout="centered")

st.title("📲 Imperium TV - Gateway Próprio Ativo")
st.caption("Disparando mensagens automáticas usando o SEU WhatsApp.")

# Configurações do seu robô próprio (Instalado no Render)
EVOLUTION_API_URL = "http://localhost:8080"  # Vamos conectar direto na sua rede
INSTANCE_NAME = "ImperiumBot"
INSTANCE_TOKEN = "ImperiumMaster2026"

API_TOKEN = "ImperiumMaster2026@#"

params = st.query_params

if "token" in params and params["token"] == API_TOKEN:
    numero = params.get("number", "").strip()
    mensagem = params.get("text", "").strip()
    
    if numero and mensagem:
        try:
            # Garante formato internacional
            if not numero.startswith("55"):
                numero = f"55{numero}"
                
            # Endpoint oficial para envio de texto da sua API própria
            url_envio = f"{EVOLUTION_API_URL}/message/sendText/{INSTANCE_NAME}"
            
            headers = {
                "Content-Type": "application/json",
                "apikey": INSTANCE_TOKEN
            }
            
            payload = {
                "number": numero,
                "text": mensagem
            }
            
            response = requests.post(url_envio, json=payload, headers=headers)
            
            if response.status_code in [200, 201]:
                st.success(f"🚀 Mensagem enviada pelo seu número para: {numero}")
            else:
                print(f"⚠️ Erro no envio. Retorno: {response.text}")
                
        except Exception as e:
            print(f"❌ Erro crítico no gateway: {e}")
else:
    st.warning("Aguardando conexões do painel principal...")
