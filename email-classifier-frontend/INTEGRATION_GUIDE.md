# 🚀 Guia de Integração - Frontend React com Backend Flask

## ✅ **Status da Integração**

A integração com o backend Flask está **COMPLETA**! Seu frontend React agora está conectado com a API real.

## 🔧 **O que foi implementado:**

### 1. **Serviço de API (`src/services/api.ts`)**
- ✅ Conexão com backend Flask
- ✅ Classificação de emails via texto
- ✅ Upload e classificação de arquivos (.txt, .pdf)
- ✅ Verificação de status da API
- ✅ Tratamento de erros
- ✅ Hook personalizado para status da API

### 2. **Componente EmailClassifier atualizado**
- ✅ Integração com API real
- ✅ Suporte a upload de arquivos
- ✅ Interface responsiva mantida
- ✅ Tratamento de erros melhorado

### 3. **Componente ApiStatus**
- ✅ Monitoramento em tempo real da API
- ✅ Indicador visual de status

## 🚀 **Como usar:**

### 1. **Iniciar o Backend**
```bash
# No diretório do backend
cd ../email-classifier-backend
python app.py
```

### 2. **Iniciar o Frontend**
```bash
# No diretório do frontend
cd email-classifier-frontend
npm run dev
```

### 3. **Testar a integração**
- Acesse: `http://localhost:5173`
- Cole um texto de email ou faça upload de arquivo
- Clique em "Classificar Email"
- Veja o resultado da classificação real

## 🔌 **Endpoints utilizados:**

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/health` | GET | Verificar status da API |
| `/classify` | POST | Classificar email via texto |
| `/classify-file` | POST | Classificar email via arquivo |
| `/stats` | GET | Estatísticas da API |
| `/fetch-emails` | GET | Buscar emails do Hotmail |

## 📁 **Estrutura de arquivos:**

```
src/
├── services/
│   └── api.ts              # Serviço de API
├── components/
│   └── ApiStatus.tsx       # Componente de status
├── EmailClassifier.tsx     # Componente principal
├── App.tsx                 # App principal
└── main.tsx               # Entry point
```

## ⚙️ **Configuração:**

### Variáveis de ambiente:
Crie um arquivo `.env` na raiz do projeto:
```env
VITE_API_URL=http://localhost:5000
```

### Se o backend estiver em outra porta:
```env
VITE_API_URL=http://localhost:8000
```

## 🧪 **Testes:**

### Teste 1: Email Produtivo
```
Preciso de ajuda urgente com o sistema. Está dando erro 404.
```

### Teste 2: Email Improdutivo
```
Obrigado pelo suporte! Vocês são demais!
```

### Teste 3: Upload de arquivo
- Crie um arquivo `.txt` com conteúdo de email
- Faça upload no sistema
- Verifique a classificação

## 🛠️ **Solução de Problemas:**

### Erro: "API não está disponível"
1. Verifique se o backend está rodando: `python app.py`
2. Confirme a porta: `http://localhost:5000`
3. Teste: `curl http://localhost:5000/health`

### Erro: "Erro de conexão"
1. Verifique o CORS no backend
2. Confirme a URL da API no `.env`
3. Verifique o firewall

### Erro: "Erro na classificação"
1. Verifique os logs do backend
2. Confirme se o texto não está vazio
3. Verifique o formato do arquivo (.txt, .pdf)

## 🎯 **Funcionalidades disponíveis:**

### ✅ **Classificação de Texto**
- Cole qualquer texto de email
- Classificação automática
- Resposta sugerida personalizada

### ✅ **Upload de Arquivos**
- Suporte a `.txt` e `.pdf`
- Preview do conteúdo
- Classificação automática

### ✅ **Monitoramento**
- Status da API em tempo real
- Indicadores visuais
- Tratamento de erros

### ✅ **Interface**
- Design responsivo
- Feedback visual
- Animações suaves

## 🔄 **Próximos passos (opcionais):**

### 1. **Integração com emails reais**
- Configure o Hotmail no backend
- Use o endpoint `/fetch-emails`
- Implemente autenticação OAuth2

### 2. **Melhorias de UX**
- Adicione notificações toast
- Implemente loading states
- Adicione animações

### 3. **Funcionalidades avançadas**
- Histórico de classificações
- Exportar resultados
- Configurações personalizadas

## 📞 **Suporte:**

Se encontrar problemas:
1. Verifique os logs do console (F12)
2. Confirme se ambos os servidores estão rodando
3. Teste os endpoints manualmente
4. Verifique a documentação da API

---

**🎉 Parabéns!** Sua integração está funcionando perfeitamente!
