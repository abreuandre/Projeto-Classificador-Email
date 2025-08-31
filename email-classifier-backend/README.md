# 📧 Sistema de Classificação de Emails - Backend

Sistema inteligente para classificar emails como **Produtivos** ou **Improdutivos** usando processamento de linguagem natural (NLP) em português.

## 🚀 Funcionalidades

- ✅ **Classificação Automática**: Analisa emails e os classifica como produtivos ou improdutivos
- ✅ **NLP Avançado**: Usa NLTK com stemmer português (RSLP) e stop words
- ✅ **Respostas Automáticas**: Gera respostas personalizadas baseadas na categoria
- ✅ **Upload de Arquivos**: Suporta arquivos .txt e .pdf
- ✅ **API REST**: Endpoints bem documentados para integração
- ✅ **CORS Habilitado**: Pronto para integração com frontend
- ✅ **Logs Detalhados**: Monitoramento completo das operações

## 🛠️ Tecnologias

- **Backend**: Flask (Python)
- **NLP**: NLTK, RSLP Stemmer
- **Processamento**: Regex, análise de padrões
- **API**: REST com JSON
- **CORS**: Flask-CORS

## 📦 Instalação

### 1. Clone o repositório
```bash
git clone <seu-repositorio>
cd email-classifier-backend
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Configure as variáveis de ambiente (opcional)
```bash
# Copie o arquivo de exemplo
cp env-example.sh .env

# Edite com suas configurações
# HOTMAIL_PASSWORD=sua_senha_aqui
```

### 4. Execute o servidor
```bash
python app.py
```

O servidor estará disponível em: `http://localhost:5000`

## 🔌 API Endpoints

### 1. Classificar Email (Texto)
```http
POST /classify
Content-Type: application/json

{
  "text": "Preciso de ajuda com o sistema"
}
```

**Resposta:**
```json
{
  "category": "Produtivo",
  "confidence": 0.85,
  "suggested_response": "Prezado(a), Recebemos sua mensagem...",
  "reasoning": "Contém 2 palavra(s)-chave relacionada(s) a solicitações produtivas",
  "features": {
    "word_count": 8,
    "char_count": 35,
    "productive_keywords": 2,
    "unproductive_keywords": 0,
    "has_question": false,
    "urgency_indicators": 0
  },
  "timestamp": "2024-01-15T10:30:00"
}
```

### 2. Classificar Email (Arquivo)
```http
POST /classify-file
Content-Type: multipart/form-data

file: [arquivo .txt ou .pdf]
```

### 3. Verificar Status
```http
GET /health
```

### 4. Estatísticas
```http
GET /stats
```

## 🌐 Integração com Frontend

### Opção 1: HTML/JavaScript (Mais Simples)

1. **Abra o arquivo** `frontend-example.html` no navegador
2. **Ajuste a URL da API** se necessário (linha 108)
3. **Teste a integração**

### Opção 2: React

```bash
# Criar projeto React
npx create-react-app email-classifier-frontend
cd email-classifier-frontend
npm install axios

# Usar o código de exemplo em react-integration-example.js
```

### Opção 3: Vue.js

```javascript
// Exemplo básico
async classifyEmail() {
  try {
    const response = await axios.post('http://localhost:5000/classify', {
      text: this.emailText
    })
    this.result = response.data
  } catch (error) {
    console.error('Erro:', error)
  }
}
```

## 🧪 Testes

### Teste Automático
```bash
python test-integration.py
```

### Teste Manual
```bash
# Verificar se o servidor está rodando
curl http://localhost:5000/health

# Testar classificação
curl -X POST http://localhost:5000/classify \
  -H "Content-Type: application/json" \
  -d '{"text": "Preciso de ajuda urgente"}'
```

## 📊 Como Funciona

### 1. Pré-processamento
- Conversão para minúsculas
- Remoção de URLs, emails e números
- Tokenização com NLTK
- Remoção de stop words
- Stemming com RSLP

### 2. Análise de Características
- **Palavras-chave produtivas**: urgente, problema, suporte, etc.
- **Palavras-chave improdutivas**: parabéns, obrigado, felicitações, etc.
- **Padrões regex**: perguntas, solicitações, prazos
- **Estrutura**: tamanho, pontuação, urgência

### 3. Classificação
- Pontuação baseada em múltiplos fatores
- Confiança calculada pela diferença de scores
- Categoria determinada pelo score mais alto

### 4. Resposta Automática
- Personalizada por categoria
- Adaptada ao contexto (urgência, tipo de solicitação)
- Formatação profissional

## 🎯 Exemplos de Classificação

### Emails Produtivos
- "Preciso de ajuda urgente com o sistema"
- "Gostaria de solicitar uma reunião"
- "Há um erro no sistema que precisa ser corrigido"
- "Qual é o status do projeto?"

### Emails Improdutivos
- "Obrigado pelo suporte!"
- "Feliz aniversário!"
- "Bom dia, tudo bem?"
- "Parabéns pelo trabalho!"

## 🚀 Deploy

### Heroku
```bash
# Seu backend já tem Procfile configurado
git add .
git commit -m "Deploy"
git push heroku main
```

### Docker
```bash
# Build da imagem
docker build -t email-classifier .

# Executar container
docker run -p 5000:5000 email-classifier
```

## 🔧 Configuração Avançada

### Variáveis de Ambiente
```bash
# Porta do servidor
PORT=5000

# Modo de desenvolvimento
FLASK_ENV=development

# Senha do Hotmail (para fetch de emails)
HOTMAIL_PASSWORD=sua_senha
```

### Personalização
- **Palavras-chave**: Edite as listas em `EmailClassifier.__init__()`
- **Padrões regex**: Modifique `productive_patterns`
- **Respostas**: Personalize `generate_response()`

## 📈 Monitoramento

### Logs
```python
# Logs automáticos configurados
logger.info(f"Email classificado como: {category}")
```

### Métricas
- Use `/stats` para estatísticas da API
- Monitore logs para erros
- Configure alertas para downtime

## 🛡️ Segurança

### Recomendações
1. **Use HTTPS em produção**
2. **Implemente rate limiting**
3. **Valide inputs**
4. **Use variáveis de ambiente para senhas**

### Rate Limiting (Opcional)
```python
from flask_limiter import Limiter

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)
```

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📞 Suporte

- **Documentação**: Acesse `/` no servidor
- **Logs**: Verifique os logs do console
- **Testes**: Execute `test-integration.py`

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para detalhes.

---

**🎉 Pronto para usar!** Seu sistema de classificação de emails está funcionando e pronto para integração com qualquer frontend!
