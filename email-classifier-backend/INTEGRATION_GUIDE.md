# 🚀 Guia de Integração - Backend com Frontend

Este guia mostra como integrar seu backend Flask com diferentes tipos de frontend.

## 📋 Pré-requisitos

1. **Backend rodando**: Certifique-se de que seu servidor Flask está rodando
2. **CORS habilitado**: Seu backend já tem CORS configurado ✅
3. **Endpoints disponíveis**: Todos os endpoints estão funcionando

## 🔧 Configuração do Backend

### 1. Iniciar o servidor
```bash
# No diretório do backend
python app.py
```

O servidor estará disponível em: `http://localhost:5000`

### 2. Verificar se está funcionando
```bash
curl http://localhost:5000/health
```

## 🌐 Integração com Frontend

### Opção 1: HTML/JavaScript Puro (Mais Simples)

Use o arquivo `frontend-example.html` que criamos:

1. **Abra o arquivo** `frontend-example.html` no navegador
2. **Ajuste a URL da API** se necessário (linha 108)
3. **Teste a integração**

**Vantagens:**
- ✅ Não precisa de build
- ✅ Funciona imediatamente
- ✅ Fácil de modificar

### Opção 2: React (Recomendado para projetos maiores)

#### 2.1 Criar projeto React
```bash
npx create-react-app email-classifier-frontend
cd email-classifier-frontend
npm install axios
```

#### 2.2 Usar o código de exemplo
Copie o conteúdo de `react-integration-example.js` para seu componente React.

#### 2.3 Configurar proxy (opcional)
No `package.json`:
```json
{
  "proxy": "http://localhost:5000"
}
```

### Opção 3: Vue.js

```javascript
// Exemplo básico para Vue.js
<template>
  <div>
    <textarea v-model="emailText" placeholder="Digite o email..."></textarea>
    <button @click="classifyEmail">Classificar</button>
    <div v-if="result">
      <h3>Resultado: {{ result.category }}</h3>
      <p>Confiança: {{ result.confidence }}%</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      emailText: '',
      result: null
    }
  },
  methods: {
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
  }
}
</script>
```

### Opção 4: Angular

```typescript
// email-classifier.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class EmailClassifierService {
  private apiUrl = 'http://localhost:5000';

  constructor(private http: HttpClient) { }

  classifyText(text: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/classify`, { text });
  }

  classifyFile(file: File): Observable<any> {
    const formData = new FormData();
    formData.append('file', file);
    return this.http.post(`${this.apiUrl}/classify-file`, formData);
  }
}
```

## 🔌 Endpoints da API

### 1. Classificar Texto
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

### 2. Classificar Arquivo
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

## 🛠️ Solução de Problemas

### Erro de CORS
Seu backend já tem CORS configurado, mas se houver problemas:

```python
# No app.py, verifique se esta linha existe:
CORS(app)
```

### Erro de Conexão
1. **Verifique se o servidor está rodando:**
   ```bash
   curl http://localhost:5000/health
   ```

2. **Verifique a porta:**
   - Backend padrão: porta 5000
   - Ajuste no frontend se necessário

3. **Verifique o firewall:**
   - Windows: Verificar se a porta 5000 está liberada
   - Linux/Mac: `sudo ufw allow 5000`

### Erro de Upload de Arquivo
1. **Verifique o tamanho do arquivo**
2. **Verifique o formato (.txt ou .pdf)**
3. **Verifique se o arquivo não está corrompido**

## 📱 Exemplo de Uso com Mobile

### React Native
```javascript
import axios from 'axios';

const classifyEmail = async (text) => {
  try {
    const response = await axios.post('http://localhost:5000/classify', {
      text: text
    });
    return response.data;
  } catch (error) {
    console.error('Erro:', error);
    throw error;
  }
};
```

### Flutter
```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

Future<Map<String, dynamic>> classifyEmail(String text) async {
  final response = await http.post(
    Uri.parse('http://localhost:5000/classify'),
    headers: {'Content-Type': 'application/json'},
    body: json.encode({'text': text}),
  );
  
  if (response.statusCode == 200) {
    return json.decode(response.body);
  } else {
    throw Exception('Falha na classificação');
  }
}
```

## 🚀 Deploy

### Backend (Heroku)
```bash
# Seu backend já tem Procfile configurado
git add .
git commit -m "Deploy"
git push heroku main
```

### Frontend (Netlify/Vercel)
1. **Build do projeto**
2. **Upload dos arquivos estáticos**
3. **Configurar variáveis de ambiente** (URL da API)

## 📊 Monitoramento

### Logs do Backend
```python
# Os logs já estão configurados no app.py
logger.info(f"Email classificado como: {category}")
```

### Métricas
- Use o endpoint `/stats` para estatísticas
- Monitore os logs para erros
- Configure alertas para downtime

## 🔒 Segurança

### Recomendações
1. **Use HTTPS em produção**
2. **Implemente rate limiting**
3. **Valide inputs no frontend e backend**
4. **Use variáveis de ambiente para senhas**

### Exemplo de Rate Limiting
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)
```

## 📞 Suporte

Se precisar de ajuda:
1. Verifique os logs do backend
2. Teste os endpoints com curl/Postman
3. Verifique a documentação da API em `/`

---

**🎉 Parabéns!** Seu backend está pronto para integração com qualquer frontend!
