# Integração com APIs de Email

## 🚨 **Situação Atual**
A aplicação atual usa **emails simulados** para demonstração. Para conectar com seu email real `andre_machado92@hotmail.com`, você precisa de uma das opções abaixo:

## 🔧 **Opções de Integração**

### **Opção 1: Microsoft Graph API (Recomendado para Hotmail/Outlook)**

1. **Registrar aplicação no Azure Portal:**
   - Acesse: https://portal.azure.com
   - Crie um novo registro de aplicativo
   - Configure permissões para Microsoft Graph API

2. **Instalar dependências:**
```bash
npm install @azure/msal-browser @microsoft/microsoft-graph-client
```

3. **Configurar autenticação:**
```typescript
// src/services/emailService.ts
import { Client } from '@microsoft/microsoft-graph-client';
import { PublicClientApplication } from '@azure/msal-browser';

const msalConfig = {
  auth: {
    clientId: 'SEU_CLIENT_ID_AQUI',
    authority: 'https://login.microsoftonline.com/consumers'
  }
};

export const emailService = {
  async getEmails() {
    // Implementar busca de emails via Microsoft Graph API
  }
};
```

### **Opção 2: IMAP (Alternativa)**

1. **Instalar dependência:**
```bash
npm install node-imap
```

2. **Configurar servidor IMAP do Hotmail:**
```typescript
// src/services/imapService.ts
import Imap from 'node-imap';

const imapConfig = {
  user: 'andre_machado92@hotmail.com',
  password: 'SUA_SENHA_AQUI',
  host: 'outlook.office365.com',
  port: 993,
  tls: true,
  tlsOptions: { rejectUnauthorized: false }
};
```

### **Opção 3: Webhook com Microsoft Power Automate**

1. **Criar fluxo no Power Automate:**
   - Conectar com Outlook/Hotmail
   - Configurar trigger para novos emails
   - Enviar dados para sua aplicação via webhook

2. **Receber webhooks na aplicação:**
```typescript
// src/api/webhook.ts
app.post('/webhook/email', (req, res) => {
  const emailData = req.body;
  // Processar email recebido
});
```

## 🛡️ **Considerações de Segurança**

⚠️ **IMPORTANTE:** Nunca exponha credenciais de email no código frontend!

- Use variáveis de ambiente (.env)
- Implemente autenticação OAuth2
- Considere usar um backend para intermediar as chamadas
- Use HTTPS em produção

## 🚀 **Implementação Rápida (Backend)**

Para uma solução completa, recomendo criar um backend:

```typescript
// Backend (Node.js/Express)
app.get('/api/emails', async (req, res) => {
  // Buscar emails via Microsoft Graph API
  // Retornar lista de emails
});

app.post('/api/classify', async (req, res) => {
  // Classificar email recebido
  // Retornar resultado
});
```

## 📋 **Próximos Passos**

1. **Escolha uma das opções acima**
2. **Configure as credenciais necessárias**
3. **Substitua a simulação no `EmailFetcher.tsx`**
4. **Teste com emails reais**

## 🔗 **Links Úteis**

- [Microsoft Graph API Documentation](https://docs.microsoft.com/en-us/graph/)
- [Outlook REST API](https://docs.microsoft.com/en-us/outlook/rest/)
- [Azure App Registration](https://portal.azure.com/#blade/Microsoft_AAD_RegisteredApps/ApplicationsListBlade)

---

**Nota:** A implementação atual com emails simulados permite testar a funcionalidade de classificação enquanto você configura a integração real.
