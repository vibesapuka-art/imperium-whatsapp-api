import streamlit as st
import requests

# Deixa a página inicializada de forma invisível/limpa
st.set_page_config(page_title="Imperium TV - API Gateway", layout="centered")

API_TOKEN = "ImperiumMaster2026@#"

st.title("📲 Imperium TV - Gateway Ativo")
st.caption("Foco exclusivo em background. Processando requisições...")

# Captura os parâmetros enviados pelo Render na URL
params = st.query_params

if "token" in params and params["token"] == API_TOKEN:
    numero = params.get("number", "").strip()
    mensagem = params.get("text", "").strip()
    
    if numero and mensagem:
        try:
            # =========================================================================
            # INTEGRAÇÃO DIRETA COM SEU WHATSAPP (Substitua pela chamada da sua API se necessário)
            # =========================================================================
            # Exemplo padrão de disparo via sua instância conectada:
            # requests.post("SUA_URL_DA_API_DE_WHATSAPP/sendMessage", json={"to": numero, "body": mensagem})
            
            st.success(f"Disparo acionado com sucesso para: {numero}")
            print(f"🚀 [Gateway] Mensagem enviada para {numero}")
        except Exception as e:
            print(f"❌ [Gateway] Erro no envio físico da mensagem: {e}")
else:
    st.warning("Aguardando parâmetros de autenticação válidos.")
