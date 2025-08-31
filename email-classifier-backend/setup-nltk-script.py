#!/usr/bin/env python3
"""
Script de configuração dos recursos NLTK
Execute este script uma vez antes de rodar a aplicação
"""

import nltk
import os
import sys

def download_nltk_resources():
    """Baixa todos os recursos NLTK necessários"""
    print("🔧 Configurando recursos NLTK...")
    
    # Lista de recursos necessários
    resources = [
        ('punkt', 'tokenizers/punkt'),
        ('stopwords', 'corpora/stopwords'), 
        ('rslp', 'stemmers/rslp')
    ]
    
    success_count = 0
    
    for resource_name, resource_path in resources:
        try:
            # Verificar se já existe
            try:
                nltk.data.find(resource_path)
                print(f"✅ {resource_name} - já instalado")
                success_count += 1
            except LookupError:
                # Baixar se não existir
                print(f"📥 Baixando {resource_name}...")
                nltk.download(resource_name, quiet=False)
                print(f"✅ {resource_name} - instalado com sucesso")
                success_count += 1
                
        except Exception as e:
            print(f"❌ Erro ao instalar {resource_name}: {e}")
    
    print(f"\n📊 Recursos instalados: {success_count}/{len(resources)}")
    
    if success_count == len(resources):
        print("🎉 Todos os recursos NLTK foram instalados com sucesso!")
        return True
    else:
        print("⚠️ Alguns recursos não foram instalados. A aplicação pode funcionar com limitações.")
        return False

def test_nltk_components():
    """Testa se os componentes NLTK estão funcionando"""
    print("\n🧪 Testando componentes NLTK...")
    
    try:
        # Testar tokenização
        from nltk.tokenize import word_tokenize
        tokens = word_tokenize("Este é um teste.", language='portuguese')
        print(f"✅ Tokenização: {tokens}")
    except Exception as e:
        print(f"❌ Erro na tokenização: {e}")
    
    try:
        # Testar stop words
        from nltk.corpus import stopwords
        stop_words = stopwords.words('portuguese')
        print(f"✅ Stop words: {len(stop_words)} palavras carregadas")
    except Exception as e:
        print(f"❌ Erro nas stop words: {e}")
    
    try:
        # Testar stemmer
        from nltk.stem import RSLPStemmer
        stemmer = RSLPStemmer()
        stemmed = stemmer.stem("correndo")
        print(f"✅ Stemmer: 'correndo' → '{stemmed}'")
    except Exception as e:
        print(f"❌ Erro no stemmer: {e}")

def check_python_version():
    """Verifica a versão do Python"""
    version = sys.version_info
    print(f"🐍 Versão do Python: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 8:
        print("✅ Versão do Python compatível")
        return True
    else:
        print("⚠️ Recomendamos Python 3.8 ou superior")
        return False

def main():
    """Função principal do script de configuração"""
    print("=" * 60)
    print("🚀 CONFIGURAÇÃO DO SISTEMA DE CLASSIFICAÇÃO DE EMAILS")
    print("=" * 60)
    
    # Verificar Python
    check_python_version()
    
    # Configurar NLTK
    print(f"\n📁 Diretório de dados NLTK: {nltk.data.path}")
    
    success = download_nltk_resources()
    
    if success:
        test_nltk_components()
        print("\n🎯 Configuração concluída! Agora você pode executar:")
        print("   python app.py")
    else:
        print("\n⚠️ Configuração concluída com avisos.")
        print("   A aplicação deve funcionar, mas com funcionalidades limitadas.")
        print("   Tente executar: python app.py")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()