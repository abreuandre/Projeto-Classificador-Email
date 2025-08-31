import axios from 'axios';

// Configuração da API
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

// Configuração do axios
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interfaces TypeScript
export interface ClassificationResult {
  category: 'Produtivo' | 'Improdutivo';
  confidence: number;
  suggested_response: string;
  reasoning: string;
  features: {
    word_count: number;
    char_count: number;
    productive_keywords: number;
    unproductive_keywords: number;
    has_question: boolean;
    urgency_indicators: number;
  };
  timestamp: string;
}

export interface EmailData {
  from: string;
  subject: string;
  body: string;
}

export interface ApiError {
  error: string;
  message?: string;
}

// Serviço de classificação
export const classificationService = {
  // Classificar email via texto
  async classifyText(text: string): Promise<ClassificationResult> {
    try {
      const response = await api.post('/classify', { text });
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new Error(error.response?.data?.error || 'Erro na classificação');
      }
      throw new Error('Erro de conexão');
    }
  },

  // Classificar email via arquivo
  async classifyFile(file: File): Promise<ClassificationResult> {
    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await api.post('/classify-file', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new Error(error.response?.data?.error || 'Erro na classificação do arquivo');
      }
      throw new Error('Erro de conexão');
    }
  },

  // Verificar status da API
  async checkHealth(): Promise<{ status: string; timestamp: string; version: string }> {
    try {
      const response = await api.get('/health');
      return response.data;
    } catch (error) {
      throw new Error('API não está disponível');
    }
  },

  // Buscar emails do Hotmail (se configurado)
  async fetchEmails(): Promise<EmailData[]> {
    try {
      const response = await api.get('/fetch-emails');
      return response.data.emails || [];
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new Error(error.response?.data?.error || 'Erro ao buscar emails');
      }
      throw new Error('Erro de conexão');
    }
  },

  // Obter estatísticas da API
  async getStats(): Promise<any> {
    try {
      const response = await api.get('/stats');
      return response.data;
    } catch (error) {
      throw new Error('Erro ao obter estatísticas');
    }
  },
};

import React from 'react';

// Hook personalizado para gerenciar estado da API
export const useApiStatus = () => {
  const [isOnline, setIsOnline] = React.useState<boolean | null>(null);
  const [isChecking, setIsChecking] = React.useState(true);

  const checkStatus = React.useCallback(async () => {
    setIsChecking(true);
    try {
      await classificationService.checkHealth();
      setIsOnline(true);
    } catch (error) {
      setIsOnline(false);
    } finally {
      setIsChecking(false);
    }
  }, []);

  React.useEffect(() => {
    checkStatus();
    
    // Verificar status a cada 30 segundos
    const interval = setInterval(checkStatus, 30000);
    return () => clearInterval(interval);
  }, [checkStatus]);

  return { isOnline, isChecking, checkStatus };
};

export default api;
