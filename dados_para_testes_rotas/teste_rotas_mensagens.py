#!/usr/bin/env python3
"""
Script de teste para verificar as rotas de mensagens implementadas
"""

import requests
import json
from datetime import datetime

# Configurações
BASE_URL = "http://127.0.0.1:8000"

def testar_rotas_mensagens():
    """Testa as rotas de mensagens implementadas"""
    
    print("🧪 Testando Rotas de Mensagens - Obratto")
    print("=" * 50)
    
    # Teste 1: Verificar se a rota GET /mensagens existe
    print("\n1. Testando rota GET /mensagens")
    try:
        response = requests.get(f"{BASE_URL}/mensagens", allow_redirects=False)
        if response.status_code == 303:
            print("✅ Rota existe e redireciona para login (comportamento esperado)")
            print(f"   Status: {response.status_code}")
            print(f"   Redirecionamento: {response.headers.get('location', 'N/A')}")
        else:
            print(f"⚠️  Status inesperado: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro ao testar rota: {e}")
    
    # Teste 2: Verificar se a rota GET /mensagens/nova existe
    print("\n2. Testando rota GET /mensagens/nova")
    try:
        response = requests.get(f"{BASE_URL}/mensagens/nova", allow_redirects=False)
        if response.status_code == 303:
            print("✅ Rota existe e redireciona para login (comportamento esperado)")
            print(f"   Status: {response.status_code}")
        else:
            print(f"⚠️  Status inesperado: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro ao testar rota: {e}")
    
    # Teste 3: Verificar se a rota GET /mensagens/conversa/{id} existe
    print("\n3. Testando rota GET /mensagens/conversa/1")
    try:
        response = requests.get(f"{BASE_URL}/mensagens/conversa/1", allow_redirects=False)
        if response.status_code == 303:
            print("✅ Rota existe e redireciona para login (comportamento esperado)")
            print(f"   Status: {response.status_code}")
        else:
            print(f"⚠️  Status inesperado: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro ao testar rota: {e}")
    
    # Teste 4: Verificar se a rota POST /mensagens/enviar existe
    print("\n4. Testando rota POST /mensagens/enviar")
    try:
        data = {
            "destinatario_id": "1",
            "conteudo": "Mensagem de teste"
        }
        response = requests.post(f"{BASE_URL}/mensagens/enviar", data=data, allow_redirects=False)
        if response.status_code == 303:
            print("✅ Rota existe e redireciona para login (comportamento esperado)")
            print(f"   Status: {response.status_code}")
        else:
            print(f"⚠️  Status inesperado: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro ao testar rota: {e}")
    
    # Teste 5: Verificar outras rotas importantes
    print("\n5. Testando outras rotas importantes")
    rotas_importantes = [
        "/",
        "/login", 
        "/escolha_cadastro"
    ]
    
    for rota in rotas_importantes:
        try:
            response = requests.get(f"{BASE_URL}{rota}")
            if response.status_code == 200:
                print(f"✅ {rota}: OK (Status: {response.status_code})")
            else:
                print(f"⚠️  {rota}: Status {response.status_code}")
        except Exception as e:
            print(f"❌ {rota}: Erro - {e}")

def verificar_servidor():
    """Verifica se o servidor está rodando"""
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        return True
    except:
        return False

if __name__ == "__main__":
    print("🚀 Verificando se o servidor está rodando...")
    
    if verificar_servidor():
        print("✅ Servidor está rodando!")
        testar_rotas_mensagens()
    else:
        print("❌ Servidor não está rodando!")
        print("\nPara executar o servidor:")
        print("cd obratto-manus/Obratto/OBRATTO")
        print("python3.11 main.py")
        print("\nEm seguida, execute este script novamente.")
    
    print("\n" + "=" * 50)
    print("🏁 Teste concluído!")
