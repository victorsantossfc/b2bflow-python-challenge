import os
import requests
from dotenv import load_dotenv
from supabase import create_client

# Carrega as variáveis de ambiente
load_dotenv()

# Configurações do Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Configurações da Z-API
ZAPI_INSTANCE = os.getenv("ZAPI_INSTANCE_ID")
ZAPI_TOKEN = os.getenv("ZAPI_TOKEN")

def enviar_mensagem_whatsapp(numero, nome):
    """Envia a mensagem personalizada utilizando a API da Z-API"""
    url = f"https://api.z-api.io/instances/{ZAPI_INSTANCE}/token/{ZAPI_TOKEN}/send-text"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    # Garante o DDI 55 do Brasil na frente do número
    numero_formatado = f"55{numero}" if not numero.startswith("55") else numero

    payload = {
        "phone": numero_formatado,
        "message": f"Olá, {nome} tudo bem com você?"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            print(f"✅ Mensagem enviada com sucesso para {nome} ({numero})")
        else:
            print(f"❌ Erro ao enviar para {nome}: Status {response.status_code} - {response.text}")
    except Exception as e:
        print(f"💥 Erro de conexão ao tentar enviar para {nome}: {e}")

def main():
    print("🚀 Buscando contatos no Supabase...")
    
    try:
        # Busca os contatos limitando a no máximo 3 registros (Regra do Desafio)
        response = supabase.table("contatos").select("*").limit(3).execute()
        contatos = response.data

        if not contatos:
            print("⚠️ Nenhum contato encontrado na tabela.")
            return

        print(f"📋 Encontrados {len(contatos)} contato(s). Iniciando disparos...")

        for contato in contatos:
            nome = contato.get("nome")
            telefone = contato.get("telefone") 

            if nome and telefone:
                enviar_mensagem_whatsapp(str(telefone), nome)
            else:
                print("⚠️ Contato ignorado por falta de nome ou telefone no registro.")

    except Exception as e:
        print(f"❌ Erro ao interagir com o Supabase: {e}")

if __name__ == "__main__":
  main()
