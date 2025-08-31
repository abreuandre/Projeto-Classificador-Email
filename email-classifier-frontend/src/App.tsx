import React, { useState, useRef } from 'react';
import EmailFetcher from './EmailFetcher';

// Componentes de ícones SVG inline
const Upload = ({ className = "h-4 w-4" }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
  </svg>
);

const Mail = ({ className = "h-4 w-4" }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
  </svg>
);

const Brain = ({ className = "h-4 w-4" }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
  </svg>
);

const MessageSquare = ({ className = "h-4 w-4" }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
  </svg>
);

const FileText = ({ className = "h-4 w-4" }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
  </svg>
);

const AlertCircle = ({ className = "h-4 w-4" }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.502 0L4.268 18.5c-.77.833.192 2.5 1.732 2.5z" />
  </svg>
);

const CheckCircle = ({ className = "h-4 w-4" }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
  </svg>
);

const Loader = ({ className = "h-4 w-4" }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 2v6m0 8v6m9-9h-6M3 12h6m12.364-6.364l-4.242 4.242M8.758 15.758l-4.242 4.242m12.364 0l-4.242-4.242M8.758 8.242L4.516 4" />
  </svg>
);

interface ClassificationResult {
  category: 'Produtivo' | 'Improdutivo';
  confidence: number;
  suggestedResponse: string;
  reasoning: string;
}

const EmailClassifier: React.FC = () => {
  const [emailContent, setEmailContent] = useState('');
  const [file, setFile] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<ClassificationResult | null>(null);
  const [inputMethod, setInputMethod] = useState<'text' | 'file' | 'fetch'>('text');
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Simulação da API de classificação (substituir pela API real)
  const classifyEmail = async (content: string): Promise<ClassificationResult> => {
    // Simulação de processamento
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // Lógica simples de classificação baseada em palavras-chave
    const productiveKeywords = ['urgente', 'problema', 'erro', 'suporte', 'ajuda', 'dúvida', 'status', 'atualização', 'pendente', 'solicitação'];
    const unproductiveKeywords = ['parabéns', 'feliz', 'natal', 'aniversário', 'obrigado', 'agradecimento', 'festa'];
    
    const contentLower = content.toLowerCase();
    const hasProductiveKeywords = productiveKeywords.some(keyword => contentLower.includes(keyword));
    const hasUnproductiveKeywords = unproductiveKeywords.some(keyword => contentLower.includes(keyword));
    
    let category: 'Produtivo' | 'Improdutivo';
    let confidence: number;
    let suggestedResponse: string;
    let reasoning: string;
    
    if (hasProductiveKeywords && !hasUnproductiveKeywords) {
      category = 'Produtivo';
      confidence = 0.85;
      suggestedResponse = 'Prezado(a), recebemos sua solicitação e nossa equipe está analisando. Retornaremos em até 24 horas úteis com uma atualização. Caso seja urgente, entre em contato pelo telefone (11) 9999-9999.';
      reasoning = 'Email contém termos relacionados a solicitações de suporte ou problemas técnicos.';
    } else if (hasUnproductiveKeywords && !hasProductiveKeywords) {
      category = 'Improdutivo';
      confidence = 0.90;
      suggestedResponse = 'Muito obrigado pela mensagem! Desejamos tudo de bom para você também. Estamos sempre à disposição para qualquer necessidade.';
      reasoning = 'Email contém mensagens de cortesia ou felicitações que não requerem ação específica.';
    } else {
      // Análise mais detalhada baseada no comprimento e estrutura
      const wordCount = content.split(' ').length;
      const hasQuestionMark = content.includes('?');
      const hasRequestWords = /solicito|preciso|gostaria|poderia/.test(contentLower);
      
      if (wordCount > 20 && (hasQuestionMark || hasRequestWords)) {
        category = 'Produtivo';
        confidence = 0.75;
        suggestedResponse = 'Prezado(a), recebemos sua mensagem e nossa equipe está analisando o conteúdo. Em breve retornaremos com as informações solicitadas.';
        reasoning = 'Email apresenta características de solicitação formal baseado na estrutura e conteúdo.';
      } else {
        category = 'Improdutivo';
        confidence = 0.70;
        suggestedResponse = 'Obrigado pelo contato! Caso precise de alguma assistência específica, não hesite em nos informar.';
        reasoning = 'Email não apresenta indicadores claros de necessidade de ação imediata.';
      }
    }
    
    return { category, confidence, suggestedResponse, reasoning };
  };

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0];
    if (selectedFile) {
      setFile(selectedFile);
      
      // Ler conteúdo do arquivo
      const reader = new FileReader();
      reader.onload = (e) => {
        const content = e.target?.result as string;
        setEmailContent(content);
      };
      reader.readAsText(selectedFile);
    }
  };

  const handleSubmit = async () => {
    if (!emailContent.trim()) return;
    
    setIsLoading(true);
    setResult(null);
    
    try {
      const classification = await classifyEmail(emailContent);
      setResult(classification);
    } catch (error) {
      console.error('Erro na classificação:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const resetForm = () => {
    setEmailContent('');
    setFile(null);
    setResult(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleEmailSelect = (email: { body: string }) => {
    setEmailContent(email.body);
    setInputMethod('text');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-gray-100">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-blue-100 rounded-lg">
              <Brain className="h-6 w-6 text-blue-600" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">Sistema de Classificação de Emails</h1>
              <p className="text-sm text-gray-600">IA para automatização de respostas corporativas</p>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-6 py-8">
        <div className="grid lg:grid-cols-2 gap-8">
          {/* Input Section */}
          <div className="space-y-6">
            <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                <Mail className="h-5 w-5 text-blue-600" />
                Entrada de Email
              </h2>
              
              {/* Input Method Selector */}
              <div className="flex gap-2 mb-4 p-1 bg-gray-100 rounded-lg">
                <button
                  onClick={() => setInputMethod('text')}
                  className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-all ${
                    inputMethod === 'text'
                      ? 'bg-white text-blue-600 shadow-sm'
                      : 'text-gray-600 hover:text-gray-900'
                  }`}
                >
                  <FileText className="h-4 w-4 inline mr-2" />
                  Texto Direto
                </button>
                <button
                  onClick={() => setInputMethod('file')}
                  className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-all ${
                    inputMethod === 'file'
                      ? 'bg-white text-blue-600 shadow-sm'
                      : 'text-gray-600 hover:text-gray-900'
                  }`}
                >
                  <Upload className="h-4 w-4 inline mr-2" />
                  Upload Arquivo
                </button>
                <button
                  onClick={() => setInputMethod('fetch')}
                  className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-all ${
                    inputMethod === 'fetch'
                      ? 'bg-white text-blue-600 shadow-sm'
                      : 'text-gray-600 hover:text-gray-900'
                  }`}
                >
                  <Mail className="h-4 w-4 inline mr-2" />
                  Buscar Emails
                </button>
              </div>

              {inputMethod === 'text' ? (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Conteúdo do Email
                  </label>
                  <textarea
                    value={emailContent}
                    onChange={(e) => setEmailContent(e.target.value)}
                    placeholder="Cole aqui o conteúdo do email para classificação..."
                    className="w-full h-40 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                  />
                </div>
              ) : inputMethod === 'file' ? (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Arquivo de Email
                  </label>
                  <div
                    onClick={() => fileInputRef.current?.click()}
                    className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-blue-400 hover:bg-blue-50 transition-colors cursor-pointer"
                  >
                    <Upload className="h-8 w-8 text-gray-400 mx-auto mb-2" />
                    <p className="text-sm text-gray-600">
                      {file ? file.name : 'Clique para selecionar arquivo (.txt ou .pdf)'}
                    </p>
                    <p className="text-xs text-gray-500 mt-1">
                      Formatos suportados: TXT, PDF
                    </p>
                  </div>
                  <input
                    ref={fileInputRef}
                    type="file"
                    accept=".txt,.pdf"
                    onChange={handleFileSelect}
                    className="hidden"
                  />
                </div>
              ) : (
                <EmailFetcher onEmailSelect={handleEmailSelect} />
              )}

              <div className="flex gap-3 mt-6">
                <button
                  onClick={handleSubmit}
                  disabled={!emailContent.trim() || isLoading}
                  className="flex-1 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed text-white font-medium py-3 px-4 rounded-lg transition-colors flex items-center justify-center gap-2"
                >
                  {isLoading ? (
                    <>
                      <Loader className="h-4 w-4 animate-spin" />
                      Classificando...
                    </>
                  ) : (
                    <>
                      <Brain className="h-4 w-4" />
                      Classificar Email
                    </>
                  )}
                </button>
                <button
                  onClick={resetForm}
                  className="px-4 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  Limpar
                </button>
              </div>
            </div>

            {/* Preview Section */}
            {emailContent && (
              <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
                <h3 className="font-semibold text-gray-900 mb-3">Preview do Conteúdo</h3>
                <div className="bg-gray-50 rounded-lg p-4 max-h-32 overflow-y-auto">
                  <p className="text-sm text-gray-700 whitespace-pre-wrap">
                    {emailContent.substring(0, 300)}
                    {emailContent.length > 300 && '...'}
                  </p>
                </div>
                <p className="text-xs text-gray-500 mt-2">
                  {emailContent.length} caracteres • {emailContent.split(' ').length} palavras
                </p>
              </div>
            )}
          </div>

          {/* Results Section */}
          <div className="space-y-6">
            {result && (
              <>
                {/* Classification Result */}
                <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
                  <h3 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
                    <CheckCircle className="h-5 w-5 text-green-600" />
                    Resultado da Classificação
                  </h3>
                  
                  <div className="space-y-4">
                    <div>
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-sm font-medium text-gray-700">Categoria</span>
                        <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                          result.category === 'Produtivo'
                            ? 'bg-orange-100 text-orange-800'
                            : 'bg-green-100 text-green-800'
                        }`}>
                          {result.category}
                        </span>
                      </div>
                    </div>

                    <div>
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-sm font-medium text-gray-700">Confiança</span>
                        <span className="text-sm font-medium text-gray-900">
                          {(result.confidence * 100).toFixed(1)}%
                        </span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-blue-600 h-2 rounded-full transition-all duration-500"
                          style={{ width: `${result.confidence * 100}%` }}
                        ></div>
                      </div>
                    </div>

                    <div className="bg-blue-50 rounded-lg p-4">
                      <div className="flex items-start gap-2">
                        <AlertCircle className="h-4 w-4 text-blue-600 mt-0.5 flex-shrink-0" />
                        <div>
                          <p className="text-sm font-medium text-blue-900">Raciocínio da IA</p>
                          <p className="text-sm text-blue-700 mt-1">{result.reasoning}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Suggested Response */}
                <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
                  <h3 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
                    <MessageSquare className="h-5 w-5 text-blue-600" />
                    Resposta Automática Sugerida
                  </h3>
                  
                  <div className="bg-gray-50 rounded-lg p-4">
                    <p className="text-sm text-gray-700 leading-relaxed">
                      {result.suggestedResponse}
                    </p>
                  </div>
                  
                  <div className="flex gap-2 mt-4">
                    <button
                      onClick={() => navigator.clipboard.writeText(result.suggestedResponse)}
                      className="px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 transition-colors"
                    >
                      Copiar Resposta
                    </button>
                    <button className="px-4 py-2 border border-gray-300 text-gray-700 text-sm font-medium rounded-lg hover:bg-gray-50 transition-colors">
                      Editar
                    </button>
                  </div>
                </div>
              </>
            )}

            {/* Email Examples */}
            <div className="bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl border border-green-100 p-6">
              <h3 className="font-semibold text-gray-900 mb-3">Exemplos para Teste</h3>
              <p className="text-sm text-gray-600 mb-4">Clique em um exemplo para testar a classificação:</p>
              <div className="space-y-2">
                <button
                  onClick={() => setEmailContent(`De: suporte@empresa.com
Para: andre_machado92@hotmail.com
Assunto: Problema com login no sistema

Olá André,

Estou enfrentando um problema para fazer login no sistema da empresa. Quando tento acessar, aparece a mensagem "Usuário ou senha inválidos". Já tentei resetar a senha, mas não consigo resolver.

Você poderia me ajudar com isso? É urgente pois preciso acessar alguns relatórios hoje.

Obrigado,
João Silva`)}
                  className="w-full text-left p-3 bg-white rounded-lg border border-green-200 hover:border-green-300 hover:bg-green-50 transition-colors"
                >
                  <div className="font-medium text-gray-900">Email Produtivo - Problema Técnico</div>
                  <div className="text-xs text-gray-600 mt-1">Solicitação de suporte com urgência</div>
                </button>
                
                <button
                  onClick={() => setEmailContent(`De: maria@empresa.com
Para: andre_machado92@hotmail.com
Assunto: Feliz Aniversário!

Oi André,

Parabéns pelo seu aniversário! 🎉

Desejo que você tenha um dia muito especial, repleto de alegria e realizações. Que este novo ano de vida traga muitas conquistas e momentos felizes.

Um abraço,
Maria`)}
                  className="w-full text-left p-3 bg-white rounded-lg border border-green-200 hover:border-green-300 hover:bg-green-50 transition-colors"
                >
                  <div className="font-medium text-gray-900">Email Improdutivo - Felicitações</div>
                  <div className="text-xs text-gray-600 mt-1">Mensagem de aniversário</div>
                </button>
                
                <button
                  onClick={() => setEmailContent(`De: cliente@empresa.com
Para: andre_machado92@hotmail.com
Assunto: Solicitação de orçamento

Prezado André,

Gostaria de solicitar um orçamento para implementação de um sistema de gestão para nossa empresa. Temos aproximadamente 50 funcionários e precisamos de um sistema que inclua:

- Controle de estoque
- Gestão de vendas
- Relatórios gerenciais
- Integração com sistemas fiscais

Você poderia me enviar uma proposta detalhada com prazos e valores?

Aguardo retorno,
Carlos Santos
Empresa ABC Ltda`)}
                  className="w-full text-left p-3 bg-white rounded-lg border border-green-200 hover:border-green-300 hover:bg-green-50 transition-colors"
                >
                  <div className="font-medium text-gray-900">Email Produtivo - Solicitação Comercial</div>
                  <div className="text-xs text-gray-600 mt-1">Pedido de orçamento detalhado</div>
                </button>
                
                <button
                  onClick={() => setEmailContent(`De: colega@empresa.com
Para: andre_machado92@hotmail.com
Assunto: Obrigado pela ajuda

Oi André,

Só queria agradecer pela ajuda que você me deu ontem com aquele problema no sistema. Você foi muito prestativo e conseguiu resolver tudo rapidamente.

Muito obrigado mesmo!
Ana`)}
                  className="w-full text-left p-3 bg-white rounded-lg border border-green-200 hover:border-green-300 hover:bg-green-50 transition-colors"
                >
                  <div className="font-medium text-gray-900">Email Improdutivo - Agradecimento</div>
                  <div className="text-xs text-gray-600 mt-1">Mensagem de agradecimento</div>
                </button>
              </div>
            </div>

            {/* Instructions */}
            <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl border border-blue-100 p-6">
              <h3 className="font-semibold text-gray-900 mb-3">Como funciona?</h3>
              <div className="space-y-3 text-sm text-gray-700">
                <div className="flex items-start gap-3">
                  <div className="w-6 h-6 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0">
                    <span className="text-xs font-bold text-blue-600">1</span>
                  </div>
                  <p>Cole o texto do email ou faça upload de um arquivo</p>
                </div>
                <div className="flex items-start gap-3">
                  <div className="w-6 h-6 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0">
                    <span className="text-xs font-bold text-blue-600">2</span>
                  </div>
                  <p>Nossa IA analisa o conteúdo usando processamento de linguagem natural</p>
                </div>
                <div className="flex items-start gap-3">
                  <div className="w-6 h-6 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0">
                    <span className="text-xs font-bold text-blue-600">3</span>
                  </div>
                  <p>Receba a classificação e uma resposta automática personalizada</p>
                </div>
              </div>
            </div>

            {/* Categories Info */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
              <h3 className="font-semibold text-gray-900 mb-4">Categorias de Classificação</h3>
              <div className="space-y-3">
                <div className="flex items-start gap-3">
                  <div className="w-3 h-3 bg-orange-500 rounded-full mt-2"></div>
                  <div>
                    <p className="font-medium text-gray-900">Produtivo</p>
                    <p className="text-sm text-gray-600">
                      Emails que requerem ação: suporte técnico, dúvidas sobre sistema, solicitações
                    </p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <div className="w-3 h-3 bg-green-500 rounded-full mt-2"></div>
                  <div>
                    <p className="font-medium text-gray-900">Improdutivo</p>
                    <p className="text-sm text-gray-600">
                      Emails de cortesia: felicitações, agradecimentos, mensagens sociais
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EmailClassifier;