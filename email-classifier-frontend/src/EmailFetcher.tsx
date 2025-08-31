import React, { useState } from 'react';

interface Email {
  id: string;
  from: string;
  subject: string;
  body: string;
  date: string;
}

interface EmailFetcherProps {
  onEmailSelect: (email: Email) => void;
}

const EmailFetcher: React.FC<EmailFetcherProps> = ({ onEmailSelect }) => {
  const [emailAddress, setEmailAddress] = useState('andre_machado92@hotmail.com');
  const [isLoading, setIsLoading] = useState(false);
  const [emails, setEmails] = useState<Email[]>([]);
  const [error, setError] = useState<string | null>(null);

  // Simulação de busca de emails (substituir por API real)
  const fetchEmails = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      // Simulação de delay de API
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // Emails simulados para teste
      const mockEmails: Email[] = [
        {
          id: '1',
          from: 'suporte@empresa.com',
          subject: 'Problema com login no sistema',
          body: `Olá André,

Estou enfrentando um problema para fazer login no sistema da empresa. Quando tento acessar, aparece a mensagem "Usuário ou senha inválidos". Já tentei resetar a senha, mas não consigo resolver.

Você poderia me ajudar com isso? É urgente pois preciso acessar alguns relatórios hoje.

Obrigado,
João Silva`,
          date: '2024-01-15T10:30:00Z'
        },
        {
          id: '2',
          from: 'maria@empresa.com',
          subject: 'Feliz Aniversário!',
          body: `Oi André,

Parabéns pelo seu aniversário! 🎉

Desejo que você tenha um dia muito especial, repleto de alegria e realizações. Que este novo ano de vida traga muitas conquistas e momentos felizes.

Um abraço,
Maria`,
          date: '2024-01-15T09:15:00Z'
        },
        {
          id: '3',
          from: 'cliente@empresa.com',
          subject: 'Solicitação de orçamento',
          body: `Prezado André,

Gostaria de solicitar um orçamento para implementação de um sistema de gestão para nossa empresa. Temos aproximadamente 50 funcionários e precisamos de um sistema que inclua:

- Controle de estoque
- Gestão de vendas
- Relatórios gerenciais
- Integração com sistemas fiscais

Você poderia me enviar uma proposta detalhada com prazos e valores?

Aguardo retorno,
Carlos Santos
Empresa ABC Ltda`,
          date: '2024-01-15T08:45:00Z'
        }
      ];
      
      setEmails(mockEmails);
    } catch (err) {
      setError('Erro ao buscar emails. Tente novamente.');
    } finally {
      setIsLoading(false);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString('pt-BR');
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
      <h3 className="font-semibold text-gray-900 mb-4">Buscar Emails</h3>
      
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Endereço de Email
          </label>
          <input
            type="email"
            value={emailAddress}
            onChange={(e) => setEmailAddress(e.target.value)}
            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Digite o endereço de email"
          />
        </div>
        
        <button
          onClick={fetchEmails}
          disabled={isLoading}
          className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed text-white font-medium py-3 px-4 rounded-lg transition-colors"
        >
          {isLoading ? 'Buscando emails...' : 'Buscar Emails Recentes'}
        </button>
        
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-3">
            <p className="text-sm text-red-700">{error}</p>
          </div>
        )}
        
        {emails.length > 0 && (
          <div className="space-y-2">
            <h4 className="font-medium text-gray-900">Emails Encontrados:</h4>
            {emails.map((email) => (
              <div
                key={email.id}
                onClick={() => onEmailSelect(email)}
                className="p-3 border border-gray-200 rounded-lg hover:border-blue-300 hover:bg-blue-50 cursor-pointer transition-colors"
              >
                <div className="flex justify-between items-start mb-2">
                  <span className="font-medium text-gray-900">{email.from}</span>
                  <span className="text-xs text-gray-500">{formatDate(email.date)}</span>
                </div>
                <div className="text-sm font-medium text-gray-700 mb-1">{email.subject}</div>
                <div className="text-sm text-gray-600 line-clamp-2">
                  {email.body.substring(0, 100)}...
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default EmailFetcher;
