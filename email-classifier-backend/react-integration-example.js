// Exemplo de integração com React
// Este arquivo mostra como consumir a API do seu backend Flask em um projeto React

import React, { useState, useEffect } from 'react';
import axios from 'axios';

// Configuração da API
const API_BASE_URL = 'http://localhost:5000';

// Hook personalizado para a API
const useEmailClassifier = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [apiStatus, setApiStatus] = useState('checking');

  // Verificar status da API
  const checkApiStatus = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/health`);
      setApiStatus('online');
      return true;
    } catch (error) {
      setApiStatus('offline');
      return false;
    }
  };

  // Classificar email via texto
  const classifyText = async (text) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await axios.post(`${API_BASE_URL}/classify`, {
        text: text
      });
      
      return response.data;
    } catch (error) {
      setError(error.response?.data?.error || 'Erro na classificação');
      throw error;
    } finally {
      setLoading(false);
    }
  };

  // Classificar email via arquivo
  const classifyFile = async (file) => {
    setLoading(true);
    setError(null);
    
    try {
      const formData = new FormData();
      formData.append('file', file);
      
      const response = await axios.post(`${API_BASE_URL}/classify-file`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      return response.data;
    } catch (error) {
      setError(error.response?.data?.error || 'Erro na classificação do arquivo');
      throw error;
    } finally {
      setLoading(false);
    }
  };

  return {
    loading,
    error,
    apiStatus,
    checkApiStatus,
    classifyText,
    classifyFile
  };
};

// Componente principal
const EmailClassifierApp = () => {
  const [emailText, setEmailText] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);
  const [result, setResult] = useState(null);
  
  const {
    loading,
    error,
    apiStatus,
    checkApiStatus,
    classifyText,
    classifyFile
  } = useEmailClassifier();

  useEffect(() => {
    checkApiStatus();
  }, []);

  const handleClassify = async () => {
    try {
      let classificationResult;
      
      if (selectedFile) {
        classificationResult = await classifyFile(selectedFile);
      } else if (emailText.trim()) {
        classificationResult = await classifyText(emailText);
      } else {
        alert('Por favor, insira um texto ou selecione um arquivo');
        return;
      }
      
      setResult(classificationResult);
    } catch (error) {
      console.error('Erro na classificação:', error);
    }
  };

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    setSelectedFile(file);
    setEmailText(''); // Limpar texto quando arquivo for selecionado
  };

  const clearAll = () => {
    setEmailText('');
    setSelectedFile(null);
    setResult(null);
  };

  return (
    <div className="email-classifier-app">
      <h1>📧 Sistema de Classificação de Emails</h1>
      
      {/* Status da API */}
      <div className={`api-status ${apiStatus}`}>
        {apiStatus === 'checking' && 'Verificando API...'}
        {apiStatus === 'online' && '✅ API Online'}
        {apiStatus === 'offline' && '❌ API Offline'}
      </div>

      {/* Formulário */}
      <div className="form-container">
        <div className="form-group">
          <label>Texto do Email:</label>
          <textarea
            value={emailText}
            onChange={(e) => setEmailText(e.target.value)}
            placeholder="Cole aqui o texto do email..."
            disabled={!!selectedFile}
          />
        </div>

        <div className="form-group">
          <label>Ou faça upload de um arquivo:</label>
          <input
            type="file"
            onChange={handleFileChange}
            accept=".txt,.pdf"
            disabled={!!emailText}
          />
        </div>

        <div className="form-actions">
          <button 
            onClick={handleClassify}
            disabled={loading || (!emailText && !selectedFile)}
          >
            {loading ? '⏳ Processando...' : '🔍 Classificar'}
          </button>
          <button onClick={clearAll}>🗑️ Limpar</button>
        </div>
      </div>

      {/* Erro */}
      {error && (
        <div className="error-message">
          <strong>Erro:</strong> {error}
        </div>
      )}

      {/* Resultado */}
      {result && (
        <div className={`result ${result.category.toLowerCase()}`}>
          <h3>📊 Resultado da Classificação</h3>
          <p><strong>Categoria:</strong> {result.category}</p>
          <p><strong>Confiança:</strong> {Math.round(result.confidence * 100)}%</p>
          
          <div className="reasoning">
            <strong>Análise:</strong> {result.reasoning}
          </div>
          
          <div className="suggested-response">
            <strong>💬 Resposta Sugerida:</strong>
            <pre>{result.suggested_response}</pre>
          </div>
          
          <div className="features">
            <strong>Detalhes técnicos:</strong>
            <ul>
              <li>Palavras: {result.features.word_count}</li>
              <li>Caracteres: {result.features.char_count}</li>
              <li>Palavras-chave produtivas: {result.features.productive_keywords}</li>
              <li>Palavras-chave improdutivas: {result.features.unproductive_keywords}</li>
              <li>Contém pergunta: {result.features.has_question ? 'Sim' : 'Não'}</li>
              <li>Indicadores de urgência: {result.features.urgency_indicators}</li>
            </ul>
          </div>
        </div>
      )}
    </div>
  );
};

// Exemplo de uso com fetch nativo (sem axios)
const useEmailClassifierWithFetch = () => {
  const classifyText = async (text) => {
    const response = await fetch(`${API_BASE_URL}/classify`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text })
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return response.json();
  };

  const classifyFile = async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await fetch(`${API_BASE_URL}/classify-file`, {
      method: 'POST',
      body: formData
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return response.json();
  };

  return { classifyText, classifyFile };
};

export default EmailClassifierApp;
