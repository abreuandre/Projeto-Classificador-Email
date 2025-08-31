#!/usr/bin/env python3
"""
Script de teste para verificar a integração entre frontend e backend
"""

import requests
import json
import time
import sys

# Configuração
API_BASE_URL = "http://localhost:5000"
TEST_EMAILS = [
    {
        "text": "Preciso de ajuda urgente com o sistema. Está dando erro 404.",
        "expected_category": "Produtivo"
    },
    {
        "text": "Obrigado pelo suporte! Vocês são demais!",
        "expected_category": "Improdutivo"
    },
    {
        "text": "Gostaria de solicitar uma reunião para discutir o projeto.",
        "expected_category": "Produtivo"
    },
    {
        "text": "Feliz aniversário! Que Deus abençoe!",
        "expected_category": "Improdutivo"
    }
]

def test_health_endpoint():
    """Testa o endpoint de saúde da API"""
    print("🔍 Testando endpoint /health...")
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API está online - Status: {data.get('status')}")
            return True
        else:
            print(f"❌ API retornou status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao conectar com a API: {e}")
        return False

def test_classify_endpoint():
    """Testa o endpoint de classificação"""
    print("\n🔍 Testando endpoint /classify...")
    
    for i, test_case in enumerate(TEST_EMAILS, 1):
        print(f"\n📧 Teste {i}: {test_case['text'][:50]}...")
        
        try:
            response = requests.post(
                f"{API_BASE_URL}/classify",
                json={"text": test_case["text"]},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                category = data.get("category")
                confidence = data.get("confidence", 0)
                
                print(f"   Categoria: {category}")
                print(f"   Confiança: {confidence:.2%}")
                print(f"   Esperado: {test_case['expected_category']}")
                
                if category == test_case["expected_category"]:
                    print(f"   ✅ Resultado correto!")
                else:
                    print(f"   ⚠️ Resultado diferente do esperado")
                    
            else:
                print(f"   ❌ Erro HTTP {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Erro na requisição: {e}")

def test_stats_endpoint():
    """Testa o endpoint de estatísticas"""
    print("\n🔍 Testando endpoint /stats...")
    try:
        response = requests.get(f"{API_BASE_URL}/stats", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Estatísticas obtidas:")
            print(f"   Versão: {data.get('api_version')}")
            print(f"   Formatos suportados: {data.get('supported_formats')}")
            print(f"   Categorias: {data.get('classification_categories')}")
        else:
            print(f"❌ Erro ao obter estatísticas: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro na requisição: {e}")

def test_cors_headers():
    """Testa se os headers CORS estão configurados"""
    print("\n🔍 Testando headers CORS...")
    try:
        response = requests.options(f"{API_BASE_URL}/classify")
        cors_headers = response.headers.get('Access-Control-Allow-Origin')
        
        if cors_headers:
            print(f"✅ CORS configurado: {cors_headers}")
        else:
            print("⚠️ Headers CORS não encontrados")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao testar CORS: {e}")

def test_file_upload():
    """Testa upload de arquivo"""
    print("\n🔍 Testando upload de arquivo...")
    
    # Criar arquivo de teste
    test_content = "Este é um email de teste para verificar o sistema."
    
    try:
        files = {'file': ('test_email.txt', test_content, 'text/plain')}
        response = requests.post(f"{API_BASE_URL}/classify-file", files=files, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Arquivo processado com sucesso:")
            print(f"   Categoria: {data.get('category')}")
            print(f"   Confiança: {data.get('confidence', 0):.2%}")
        else:
            print(f"❌ Erro no upload: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro no upload: {e}")

def test_error_handling():
    """Testa tratamento de erros"""
    print("\n🔍 Testando tratamento de erros...")
    
    # Teste 1: Texto vazio
    try:
        response = requests.post(
            f"{API_BASE_URL}/classify",
            json={"text": ""},
            timeout=5
        )
        if response.status_code == 400:
            print("✅ Erro de texto vazio tratado corretamente")
        else:
            print(f"⚠️ Status inesperado para texto vazio: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro no teste: {e}")
    
    # Teste 2: Campo ausente
    try:
        response = requests.post(
            f"{API_BASE_URL}/classify",
            json={},
            timeout=5
        )
        if response.status_code == 400:
            print("✅ Erro de campo ausente tratado corretamente")
        else:
            print(f"⚠️ Status inesperado para campo ausente: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro no teste: {e}")

def main():
    """Função principal"""
    print("🚀 Iniciando testes de integração...")
    print(f"📍 API URL: {API_BASE_URL}")
    print("=" * 50)
    
    # Verificar se o servidor está rodando
    if not test_health_endpoint():
        print("\n❌ Servidor não está rodando!")
        print("Execute: python app.py")
        sys.exit(1)
    
    # Executar todos os testes
    test_classify_endpoint()
    test_stats_endpoint()
    test_cors_headers()
    test_file_upload()
    test_error_handling()
    
    print("\n" + "=" * 50)
    print("🎉 Testes de integração concluídos!")
    print("\n📋 Próximos passos:")
    print("1. Abra o arquivo frontend-example.html no navegador")
    print("2. Teste a interface manualmente")
    print("3. Verifique se a integração está funcionando")

if __name__ == "__main__":
    main()
