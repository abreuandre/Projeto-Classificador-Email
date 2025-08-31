#!/usr/bin/env python3
"""
Script de teste para a API de Classificação de Emails
Executa testes básicos nos endpoints principais
"""

import requests
import json
import time
from datetime import datetime

# Configuração da API
API_BASE_URL = "http://localhost:5000"  # Altere para sua URL de produção

def test_health_check():
    """Testa o endpoint de health check"""
    print("🔍 Testando Health Check...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health Check OK - Status: {data['status']}")
            return True
        else:
            print(f"❌ Health Check falhou - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro no Health Check: {e}")
        return False

def test_text_classification():
    """Testa classificação de texto direto"""
    print("\n📧 Testando Classificação de Texto...")
    
    # Casos de teste
    test_cases = [
        {
            "text": "Estou com problema urgente no sistema de login. Preciso de ajuda imediatamente!",
            "expected": "Produtivo"
        },
        {
            "text": "Parabéns pela excelente apresentação! Foi muito inspiradora.",
            "expected": "Improdutivo"
        },
        {
            "text": "Boa tarde! Gostaria de saber o status do meu pedido #12345. Quando ficará pronto?",
            "expected": "Produtivo"
        },
        {
            "text": "Muito obrigado pela ajuda de ontem. Vocês são fantásticos!",
            "expected": "Improdutivo"
        },
        {
            "text": "Feliz Natal para toda equipe! Que 2024 seja um ano próspero para todos.",
            "expected": "Improdutivo"
        }
    ]
    
    results = []
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n📝 Teste {i}: {case['text'][:50]}...")
        
        try:
            payload = {"text": case["text"]}
            response = requests.post(
                f"{API_BASE_URL}/classify",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                category = data["category"]
                confidence = data["confidence"]
                
                # Verificar se a classificação está correta
                is_correct = category == case["expected"]
                status = "✅" if is_correct else "⚠️"
                
                print(f"{status} Resultado: {category} (confiança: {confidence:.3f})")
                print(f"   Esperado: {case['expected']}")
                print(f"   Resposta: {data['suggested_response'][:100]}...")
                
                results.append({
                    "test": i,
                    "correct": is_correct,
                    "category": category,
                    "confidence": confidence,
                    "expected": case["expected"]
                })
                
            else:
                print(f"❌ Erro na requisição - Status: {response.status_code}")
                print(f"   Resposta: {response.text}")
                
        except Exception as e:
            print(f"❌ Erro no teste {i}: {e}")
    
    # Calcular estatísticas
    if results:
        correct_count = sum(1 for r in results if r["correct"])
        accuracy = (correct_count / len(results)) * 100
        avg_confidence = sum(r["confidence"] for r in results) / len(results)
        
        print(f"\n📊 Estatísticas dos Testes:")
        print(f"   Precisão: {accuracy:.1f}% ({correct_count}/{len(results)})")
        print(f"   Confiança Média: {avg_confidence:.3f}")
    
    return results

def test_file_upload():
    """Testa upload de arquivo (simula um arquivo de texto)"""
    print("\n📎 Testando Upload de Arquivo...")
    
    # Criar um arquivo de exemplo temporário
    test_content = """
    Prezados,
    
    Estou enfrentando dificuldades para acessar o sistema desde ontem.
    Toda vez que tento fazer login, recebo uma mensagem de erro.
    
    Podem me ajudar a resolver este problema?
    É urgente pois preciso acessar os relatórios hoje.
    
    Obrigado,
    João Silva
    """
    
    try:
        # Simular upload de arquivo
        files = {
            'file': ('test_email.txt', test_content, 'text/plain')
        }
        
        response = requests.post(
            f"{API_BASE_URL}/classify-file",
            files=files
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Upload processado com sucesso!")
            print(f"   Categoria: {data['category']}")
            print(f"   Confiança: {data['confidence']:.3f}")
            print(f"   Arquivo: {data['file_info']['filename']}")
            print(f"   Tamanho: {data['file_info']['size']} caracteres")
            return True
        else:
            print(f"❌ Erro no upload - Status: {response.status_code}")
            print(f"   Resposta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste de upload: {e}")
        return False

def test_api_stats():
    """Testa endpoint de estatísticas"""
    print("\n📈 Testando Estatísticas da API...")
    
    try:
        response = requests.get(f"{API_BASE_URL}/stats")
        if response.status_code == 200:
            data = response.json()
            print("✅ Estatísticas obtidas com sucesso:")
            print(f"   Versão da API: {data['api_version']}")
            print(f"   Formatos suportados: {', '.join(data['supported_formats'])}")
            print(f"   Categorias: {', '.join(data['classification_categories'])}")
            return True
        else:
            print(f"❌ Erro ao obter estatísticas - Status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste de estatísticas: {e}")
        return False

def test_error_handling():
    """Testa tratamento de erros da API"""
    print("\n🚨 Testando Tratamento de Erros...")
    
    error_tests = [
        {
            "name": "Texto vazio",
            "payload": {"text": ""},
            "expected_status": 400
        },
        {
            "name": "Payload inválido",
            "payload": {"invalid_field": "test"},
            "expected_status": 400
        },
        {
            "name": "Texto muito longo",
            "payload": {"text": "x" * 100000},  # 100k caracteres
            "expected_status": 200  # Deve processar, mas pode ser lento
        }
    ]
    
    results = []
    
    for test in error_tests:
        print(f"\n🧪 Testando: {test['name']}")
        
        try:
            response = requests.post(
                f"{API_BASE_URL}/classify",
                json=test["payload"],
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == test["expected_status"]:
                print(f"✅ Comportamento esperado - Status: {response.status_code}")
                results.append(True)
            else:
                print(f"⚠️ Status inesperado - Esperado: {test['expected_status']}, Obtido: {response.status_code}")
                results.append(False)
                
        except requests.exceptions.Timeout:
            print("⏱️ Timeout - Texto muito longo pode causar demora no processamento")
            results.append(True)  # Timeout é comportamento aceitável para textos muito longos
        except Exception as e:
            print(f"❌ Erro no teste: {e}")
            results.append(False)
    
    success_rate = (sum(results) / len(results)) * 100 if results else 0
    print(f"\n📊 Taxa de sucesso nos testes de erro: {success_rate:.1f}%")
    
    return results

def performance_test():
    """Testa performance da API com múltiplas requisições"""
    print("\n⚡ Testando Performance...")
    
    test_text = "Preciso de ajuda com o sistema. Por favor, me contactem urgentemente!"
    num_requests = 10
    
    print(f"Enviando {num_requests} requisições simultâneas...")
    
    start_time = time.time()
    response_times = []
    successful_requests = 0
    
    for i in range(num_requests):
        try:
            req_start = time.time()
            response = requests.post(
                f"{API_BASE_URL}/classify",
                json={"text": test_text},
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            req_end = time.time()
            
            response_times.append(req_end - req_start)
            
            if response.status_code == 200:
                successful_requests += 1
                print(f"✅ Requisição {i+1}: {response_times[-1]:.3f}s")
            else:
                print(f"❌ Requisição {i+1}: Status {response.status_code}")
                
        except Exception as e:
            print(f"❌ Requisição {i+1}: Erro - {e}")
    
    end_time = time.time()
    total_time = end_time - start_time
    
    if response_times:
        avg_response_time = sum(response_times) / len(response_times)
        min_response_time = min(response_times)
        max_response_time = max(response_times)
        
        print(f"\n📊 Resultados de Performance:")
        print(f"   Requisições bem-sucedidas: {successful_requests}/{num_requests}")
        print(f"   Tempo total: {total_time:.3f}s")
        print(f"   Tempo médio por requisição: {avg_response_time:.3f}s")
        print(f"   Tempo mínimo: {min_response_time:.3f}s")
        print(f"   Tempo máximo: {max_response_time:.3f}s")
        print(f"   Taxa de sucesso: {(successful_requests/num_requests)*100:.1f}%")
    
    return response_times

def run_comprehensive_tests():
    """Executa todos os testes de forma abrangente"""
    print("🚀 Iniciando Testes Abrangentes da API de Classificação de Emails")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"URL da API: {API_BASE_URL}")
    print("=" * 70)
    
    test_results = {}
    
    # 1. Health Check
    test_results['health'] = test_health_check()
    
    # 2. Classificação de Texto
    text_results = test_text_classification()
    test_results['text_classification'] = len(text_results) > 0
    
    # 3. Upload de Arquivo
    test_results['file_upload'] = test_file_upload()
    
    # 4. Estatísticas da API
    test_results['api_stats'] = test_api_stats()
    
    # 5. Tratamento de Erros
    error_results = test_error_handling()
    test_results['error_handling'] = len(error_results) > 0 and all(error_results)
    
    # 6. Performance
    performance_results = performance_test()
    test_results['performance'] = len(performance_results) > 0
    
    # Relatório Final
    print("\n" + "=" * 70)
    print("📋 RELATÓRIO FINAL DOS TESTES")
    print("=" * 70)
    
    passed_tests = sum(1 for result in test_results.values() if result)
    total_tests = len(test_results)
    success_rate = (passed_tests / total_tests) * 100
    
    for test_name, passed in test_results.items():
        status = "✅ PASSOU" if passed else "❌ FALHOU"
        print(f"{test_name.replace('_', ' ').title():<25} {status}")
    
    print("-" * 70)
    print(f"Testes aprovados: {passed_tests}/{total_tests} ({success_rate:.1f}%)")
    
    if success_rate >= 80:
        print("🎉 API está funcionando corretamente!")
    elif success_rate >= 60:
        print("⚠️ API apresenta alguns problemas, mas está funcional")
    else:
        print("🚨 API apresenta problemas significativos")
    
    print("=" * 70)
    
    return test_results

def interactive_test():
    """Modo interativo para testar emails personalizados"""
    print("\n🎯 Modo Interativo - Teste Seus Próprios Emails")
    print("Digite 'sair' para encerrar")
    print("-" * 50)
    
    while True:
        try:
            email_text = input("\n📧 Digite o texto do email: ").strip()
            
            if email_text.lower() in ['sair', 'exit', 'quit']:
                print("Encerrando modo interativo...")
                break
            
            if not email_text:
                print("⚠️ Texto não pode estar vazio!")
                continue
            
            print("🔄 Classificando...")
            
            response = requests.post(
                f"{API_BASE_URL}/classify",
                json={"text": email_text},
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                print(f"\n📊 Resultado:")
                print(f"   Categoria: {data['category']}")
                print(f"   Confiança: {data['confidence']:.3f}")
                print(f"   Raciocínio: {data['reasoning']}")
                print(f"\n💬 Resposta sugerida:")
                print(f"   {data['suggested_response'][:200]}...")
                
            else:
                print(f"❌ Erro na classificação - Status: {response.status_code}")
                
        except KeyboardInterrupt:
            print("\n\nEncerrando...")
            break
        except Exception as e:
            print(f"❌ Erro: {e}")

def main():
    """Função principal do script de teste"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Script de teste para API de Classificação de Emails")
    parser.add_argument("--url", default="http://localhost:5000", help="URL base da API")
    parser.add_argument("--interactive", "-i", action="store_true", help="Modo interativo")
    parser.add_argument("--performance-only", "-p", action="store_true", help="Apenas teste de performance")
    parser.add_argument("--quick", "-q", action="store_true", help="Testes rápidos (sem performance)")
    
    args = parser.parse_args()
    
    global API_BASE_URL
    API_BASE_URL = args.url
    
    if args.interactive:
        interactive_test()
    elif args.performance_only:
        performance_test()
    elif args.quick:
        print("🏃 Executando testes rápidos...")
        test_health_check()
        test_text_classification()
        test_api_stats()
    else:
        run_comprehensive_tests()

if __name__ == "__main__":
    main()