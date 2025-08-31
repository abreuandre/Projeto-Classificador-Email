"""
Sistema de Classificação de Emails - Backend
Desenvolvido para automatizar a classificação e resposta de emails corporativos
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import RSLPStemmer
import PyPDF2
import io
import os
from datetime import datetime
import logging
import imaplib
import email
from email.header import decode_header
# import emailconfig.env  # Comentado temporariamente para evitar erro de import

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicialização do Flask
app = Flask(__name__)
CORS(app)

# Download dos recursos NLTK necessários (executar automaticamente)
def download_nltk_resources():
    """Download automático dos recursos NLTK necessários"""
    resources = ['punkt', 'stopwords', 'rslp']
    
    for resource in resources:
        try:
            if resource == 'punkt':
                nltk.data.find('tokenizers/punkt')
            elif resource == 'stopwords':
                nltk.data.find('corpora/stopwords')
            elif resource == 'rslp':
                nltk.data.find('stemmers/rslp')
        except LookupError:
            print(f"Baixando recurso NLTK: {resource}")
            nltk.download(resource, quiet=True)

# Download dos recursos
download_nltk_resources()

# Inicialização dos componentes NLP com tratamento de erro
try:
    stemmer = RSLPStemmer()
    print("✅ Stemmer português (RSLP) carregado com sucesso")
except Exception as e:
    print(f"⚠️ Erro ao carregar stemmer português, usando alternativa: {e}")
    # Fallback: usar stemmer básico ou sem stemming
    stemmer = None

try:
    stop_words = set(stopwords.words('portuguese'))
    print("✅ Stop words em português carregadas com sucesso")
except Exception as e:
    print(f"⚠️ Erro ao carregar stop words, usando lista básica: {e}")
    # Lista básica de stop words em português
    stop_words = {
        'a', 'o', 'e', 'é', 'de', 'do', 'da', 'em', 'um', 'uma', 'para', 'com', 'não', 'na', 'no',
        'se', 'que', 'por', 'mais', 'as', 'os', 'como', 'mas', 'foi', 'ao', 'ele', 'das', 'tem',
        'à', 'seu', 'sua', 'ou', 'ser', 'quando', 'muito', 'há', 'nos', 'já', 'está', 'eu', 'também',
        'só', 'pelo', 'pela', 'até', 'isso', 'ela', 'entre', 'era', 'depois', 'sem', 'mesmo', 'aos',
        'ter', 'seus', 'suas', 'numa', 'pelos', 'pelas', 'esse', 'essa', 'num', 'nem', 'suas', 'meu',
        'às', 'minha', 'têm', 'numa', 'pelos', 'pelas', 'foi', 'contra', 'sobre', 'durante', 'antes'
    }

class EmailClassifier:
    def __init__(self):
        # Palavras-chave para classificação produtiva
        self.productive_keywords = [
            'urgente', 'problema', 'erro', 'bug', 'falha', 'suporte', 'ajuda', 
            'dúvida', 'status', 'atualização', 'pendente', 'solicitação', 'requisição',
            'preciso', 'necessário', 'importante', 'prazo', 'deadline', 'crítico',
            'sistema', 'plataforma', 'aplicativo', 'site', 'login', 'senha',
            'pagamento', 'cobrança', 'fatura', 'boleto', 'transferência',
            'documento', 'relatório', 'aprovação', 'autorização', 'permissão',
            'reunião', 'meeting', 'call', 'conferência', 'agendamento',
            'proposta', 'contrato', 'acordo', 'negociação', 'orçamento',
            'cliente', 'fornecedor', 'parceiro', 'projeto', 'entrega'
        ]
        
        # Palavras-chave para classificação improdutiva
        self.unproductive_keywords = [
            'parabéns', 'felicitações', 'feliz', 'natal', 'ano novo', 'aniversário',
            'birthday', 'obrigado', 'obrigada', 'agradecimento', 'thanks',
            'festa', 'evento', 'comemoração', 'celebração', 'happy',
            'bom dia', 'boa tarde', 'boa noite', 'cumprimento', 'saudação',
            'coffee', 'café', 'almoço', 'jantar', 'happy hour', 'confraternização',
            'feriado', 'férias', 'descanso', 'folga', 'licença',
            'weather', 'tempo', 'clima', 'chuva', 'sol', 'frio', 'calor',
            'piada', 'joke', 'humor', 'engraçado', 'funny', 'meme',
            'corrente', 'chain', 'forward', 'repassar', 'viral'
        ]
        
        # Padrões regex para identificar características produtivas
        self.productive_patterns = [
            r'\b(como|when|onde|what|qual|quando|por que|why)\b',  # Perguntas
            r'\b(please|por favor|kindly|gentileza)\b',  # Solicitações educadas
            r'\b(deadline|prazo|until|até|before|antes)\b',  # Prazos
            r'\b(asap|urgente|urgent|imediato|immediate)\b',  # Urgência
            r'\b(anexo|attached|attachment|documento)\b',  # Anexos
            r'\b(erro|error|issue|problema|trouble)\b',  # Problemas
            r'\b(status|update|atualização|progress)\b'  # Status
        ]
    
    def preprocess_text(self, text):
        """Pré-processamento do texto do email com tratamento de erro"""
        if not text:
            return ""
        
        # Converter para minúsculas
        text = text.lower()
        
        # Remover URLs
        text = re.sub(r'http\S+', '', text)
        text = re.sub(r'www\.\S+', '', text)
        
        # Remover emails
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remover números de telefone
        text = re.sub(r'\(?\d{2}\)?\s?\d{4,5}-?\d{4}', '', text)
        
        # Remover pontuação excessiva
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # Remover espaços extras
        text = re.sub(r'\s+', ' ', text)
        
        # Tokenização com tratamento de erro
        try:
            tokens = word_tokenize(text, language='portuguese')
        except Exception:
            # Fallback: split simples se word_tokenize falhar
            tokens = text.split()
        
        # Remover stop words
        filtered_tokens = [word for word in tokens if word not in stop_words and len(word) > 2]
        
        # Aplicar stemming se disponível
        if stemmer is not None:
            try:
                stemmed_tokens = [stemmer.stem(word) for word in filtered_tokens]
                return ' '.join(stemmed_tokens)
            except Exception:
                # Se stemming falhar, retornar tokens filtrados
                return ' '.join(filtered_tokens)
        else:
            return ' '.join(filtered_tokens)
    
    def extract_features(self, text):
        """Extrai características do texto para classificação"""
        features = {}
        
        preprocessed = self.preprocess_text(text)
        
        # Tokenização segura
        try:
            tokens = word_tokenize(preprocessed, language='portuguese')
        except Exception:
            tokens = preprocessed.split()
        
        # Features básicas
        features['word_count'] = len(tokens)
        features['char_count'] = len(text)
        features['sentence_count'] = len(re.split(r'[.!?]+', text))
        features['has_question'] = '?' in text
        features['has_exclamation'] = '!' in text
        
        # Features de urgência
        features['urgency_score'] = sum(1 for word in tokens if word in ['urgente', 'asap', 'imediato', 'crítico'])
        
        # Features de cortesia
        features['politeness_score'] = sum(1 for word in tokens if word in ['por favor', 'please', 'obrigado', 'thanks'])
        
        # Contagem de palavras-chave produtivas
        features['productive_count'] = sum(1 for word in tokens if word in self.productive_keywords)
        
        # Contagem de palavras-chave improdutivas
        features['unproductive_count'] = sum(1 for word in tokens if word in self.unproductive_keywords)
        
        # Padrões regex
        features['pattern_matches'] = sum(1 for pattern in self.productive_patterns if re.search(pattern, text, re.IGNORECASE))
        
        return features
    
    def classify_email(self, text):
        """Classifica o email como Produtivo ou Improdutivo"""
        features = self.extract_features(text)
        
        # Pontuação para classificação
        productive_score = 0
        unproductive_score = 0
        
        # Análise de palavras-chave
        productive_score += features['productive_count'] * 2
        unproductive_score += features['unproductive_count'] * 2
        
        # Análise de padrões
        productive_score += features['pattern_matches'] * 1.5
        
        # Análise de estrutura
        if features['has_question']:
            productive_score += 1
        
        if features['urgency_score'] > 0:
            productive_score += features['urgency_score'] * 2
        
        # Análise de tamanho (emails muito curtos tendem a ser improdutivos)
        if features['word_count'] < 10:
            unproductive_score += 1
        elif features['word_count'] > 30:
            productive_score += 0.5
        
        # Análise de cortesia excessiva (pode indicar email improdutivo)
        if features['politeness_score'] > 2:
            unproductive_score += 0.5
        
        # Decisão final
        total_score = productive_score + unproductive_score
        
        if total_score == 0:
            # Se não há indicadores claros, usar heurísticas adicionais
            if features['word_count'] > 20 and (features['has_question'] or 'solicit' in text.lower()):
                category = 'Produtivo'
                confidence = 0.6
            else:
                category = 'Improdutivo'
                confidence = 0.6
        else:
            confidence = max(productive_score, unproductive_score) / total_score
            category = 'Produtivo' if productive_score > unproductive_score else 'Improdutivo'
        
        # Ajustar confiança baseada na diferença de scores
        if total_score > 0:
            score_diff = abs(productive_score - unproductive_score) / total_score
            confidence = min(0.95, max(0.5, confidence + score_diff * 0.3))
        
        return category, confidence, features
    
    def generate_response(self, category, email_text):
        """Gera resposta automática baseada na categoria"""
        if category == 'Produtivo':
            # Analisar tipo de solicitação para personalizar resposta
            text_lower = email_text.lower()
            
            if any(word in text_lower for word in ['urgente', 'asap', 'crítico', 'imediato']):
                response = """Prezado(a),

Recebemos sua solicitação urgente e nossa equipe já foi notificada. 
Estamos priorizando seu atendimento e retornaremos em até 4 horas úteis.

Para casos críticos, entre em contato pelo telefone (11) 9999-9999.

Atenciosamente,
Equipe de Suporte"""
            
            elif any(word in text_lower for word in ['erro', 'problema', 'bug', 'falha']):
                response = """Prezado(a),

Agradecemos o relato do problema. Nossa equipe técnica irá investigar a questão reportada.

Você receberá uma atualização sobre o andamento em até 24 horas úteis.

Caso precise de assistência adicional, estamos à disposição.

Atenciosamente,
Equipe Técnica"""
            
            elif any(word in text_lower for word in ['status', 'andamento', 'atualização']):
                response = """Prezado(a),

Recebemos sua solicitação de atualização. 
Nossa equipe irá verificar o status atual e retornará com as informações em breve.

Tempo previsto para resposta: até 12 horas úteis.

Atenciosamente,
Equipe de Atendimento"""
            
            else:
                response = """Prezado(a),

Recebemos sua mensagem e nossa equipe está analisando sua solicitação.

Retornaremos com uma resposta detalhada em até 24 horas úteis.

Caso seja urgente, entre em contato pelo telefone (11) 9999-9999.

Atenciosamente,
Equipe de Atendimento"""
        
        else:  # Improdutivo
            text_lower = email_text.lower()
            
            if any(word in text_lower for word in ['parabéns', 'felicitações', 'feliz']):
                response = """Muito obrigado pelas felicitações!

Ficamos muito felizes com sua mensagem. 
Desejamos tudo de bom para você também!

Estamos sempre à disposição para qualquer necessidade.

Com carinho,
Equipe"""
            
            elif any(word in text_lower for word in ['obrigado', 'obrigada', 'agradecimento', 'thanks']):
                response = """De nada! Foi um prazer ajudar.

Agradecemos pelo feedback positivo.
Caso precise de algo mais, não hesite em nos contatar.

Atenciosamente,
Equipe de Atendimento"""
            
            elif any(word in text_lower for word in ['natal', 'ano novo', 'feriado']):
                response = """Muito obrigado pelas felicitações de fim de ano!

Desejamos a você e sua família um período repleto de alegria e prosperidade.

Continuaremos trabalhando para oferecer o melhor atendimento em 2025.

Feliz Ano Novo!
Equipe"""
            
            else:
                response = """Obrigado pelo contato!

Sua mensagem é muito importante para nós.
Caso precise de alguma assistência específica, não hesite em nos informar.

Estamos sempre à disposição.

Atenciosamente,
Equipe de Atendimento"""
        
        return response

# Inicializar o classificador
classifier = EmailClassifier()

def fetch_hotmail_emails(limit=5):
    """Busca últimos emails do Hotmail via IMAP"""
    try:
        imap_server = "outlook.office365.com"
        email_user = "andre_machado92@hotmail.com"
        email_pass = os.environ.get("HOTMAIL_PASSWORD")  # use variável de ambiente

        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(email_user, email_pass)
        mail.select("inbox")

        # Buscar os últimos emails
        status, messages = mail.search(None, "ALL")
        email_ids = messages[0].split()
        latest_ids = email_ids[-limit:]

        email_list = []
        for num in reversed(latest_ids):
            status, data = mail.fetch(num, "(RFC822)")
            msg = email.message_from_bytes(data[0][1])

            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8")

            from_ = msg.get("From")

            # Pegar corpo
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        try:
                            body = part.get_payload(decode=True).decode()
                            break
                        except:
                            continue
            else:
                try:
                    body = msg.get_payload(decode=True).decode()
                except:
                    body = msg.get_payload()

            email_list.append({
                "from": from_,
                "subject": subject,
                "body": body
            })

        mail.logout()
        return email_list

    except Exception as e:
        logger.error(f"Erro ao buscar emails: {e}")
        return []


def extract_text_from_pdf(pdf_file):
    """Extrai texto de arquivo PDF"""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        logger.error(f"Erro ao extrair texto do PDF: {str(e)}")
        return None

@app.route('/fetch-emails', methods=['GET'])
def fetch_emails():
    """Endpoint para buscar emails reais do Hotmail"""
    emails = fetch_hotmail_emails(limit=5)
    if not emails:
        return jsonify({"error": "Não foi possível buscar emails"}), 500
    return jsonify({"emails": emails})

@app.route('/')
def index():
    """Página inicial com documentação da API"""
    return """
    <h1>Sistema de Classificação de Emails - API</h1>
    <h2>Endpoints Disponíveis:</h2>
    <ul>
        <li><strong>POST /classify</strong> - Classifica email via texto direto</li>
        <li><strong>POST /classify-file</strong> - Classifica email via upload de arquivo</li>
        <li><strong>GET /health</strong> - Verifica status da API</li>
        <li><strong>GET /stats</strong> - Estatísticas de uso</li>
    </ul>
    
    <h2>Exemplo de uso:</h2>
    <pre>
    curl -X POST http://localhost:5000/classify \\
         -H "Content-Type: application/json" \\
         -d '{"text": "Preciso de ajuda com o sistema"}'
    </pre>
    """

@app.route('/health')
def health_check():
    """Endpoint de verificação de saúde da API"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/classify', methods=['POST'])
def classify_text():
    """Endpoint para classificação via texto direto"""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'error': 'Campo "text" é obrigatório'
            }), 400
        
        email_text = data['text'].strip()
        
        if not email_text:
            return jsonify({
                'error': 'Texto do email não pode estar vazio'
            }), 400
        
        # Classificar email
        category, confidence, features = classifier.classify_email(email_text)
        
        # Gerar resposta automática
        suggested_response = classifier.generate_response(category, email_text)
        
        # Gerar explicação do raciocínio
        reasoning = generate_reasoning(category, features, email_text)
        
        result = {
            'category': category,
            'confidence': round(confidence, 3),
            'suggested_response': suggested_response,
            'reasoning': reasoning,
            'features': {
                'word_count': features['word_count'],
                'char_count': features['char_count'],
                'productive_keywords': features['productive_count'],
                'unproductive_keywords': features['unproductive_count'],
                'has_question': features['has_question'],
                'urgency_indicators': features['urgency_score']
            },
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info(f"Email classificado como: {category} (confiança: {confidence:.3f})")
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Erro na classificação: {str(e)}")
        return jsonify({
            'error': 'Erro interno do servidor'
        }), 500

@app.route('/classify-file', methods=['POST'])
def classify_file():
    """Endpoint para classificação via upload de arquivo"""
    try:
        if 'file' not in request.files:
            return jsonify({
                'error': 'Arquivo não fornecido'
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'error': 'Nenhum arquivo selecionado'
            }), 400
        
        # Verificar extensão do arquivo
        allowed_extensions = {'.txt', '.pdf'}
        file_extension = os.path.splitext(file.filename)[1].lower()
        
        if file_extension not in allowed_extensions:
            return jsonify({
                'error': f'Tipo de arquivo não suportado. Use: {", ".join(allowed_extensions)}'
            }), 400
        
        # Extrair texto do arquivo
        if file_extension == '.txt':
            email_text = file.read().decode('utf-8')
        elif file_extension == '.pdf':
            email_text = extract_text_from_pdf(io.BytesIO(file.read()))
            if email_text is None:
                return jsonify({
                    'error': 'Erro ao extrair texto do PDF'
                }), 400
        
        if not email_text.strip():
            return jsonify({
                'error': 'Arquivo está vazio ou não contém texto legível'
            }), 400
        
        # Classificar email (reutilizando a lógica do endpoint de texto)
        category, confidence, features = classifier.classify_email(email_text)
        suggested_response = classifier.generate_response(category, email_text)
        reasoning = generate_reasoning(category, features, email_text)
        
        result = {
            'category': category,
            'confidence': round(confidence, 3),
            'suggested_response': suggested_response,
            'reasoning': reasoning,
            'file_info': {
                'filename': file.filename,
                'type': file_extension,
                'size': len(email_text)
            },
            'features': {
                'word_count': features['word_count'],
                'char_count': features['char_count'],
                'productive_keywords': features['productive_count'],
                'unproductive_keywords': features['unproductive_count'],
                'has_question': features['has_question'],
                'urgency_indicators': features['urgency_score']
            },
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info(f"Arquivo {file.filename} classificado como: {category}")
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Erro na classificação de arquivo: {str(e)}")
        return jsonify({
            'error': 'Erro interno do servidor'
        }), 500

def generate_reasoning(category, features, email_text):
    """Gera explicação do raciocínio da classificação"""
    reasons = []
    
    if features['productive_count'] > 0:
        reasons.append(f"Contém {features['productive_count']} palavra(s)-chave relacionada(s) a solicitações produtivas")
    
    if features['unproductive_count'] > 0:
        reasons.append(f"Contém {features['unproductive_count']} palavra(s)-chave relacionada(s) a mensagens de cortesia")
    
    if features['has_question']:
        reasons.append("Contém pergunta(s), indicando necessidade de resposta")
    
    if features['urgency_score'] > 0:
        reasons.append("Apresenta indicadores de urgência")
    
    if features['pattern_matches'] > 0:
        reasons.append("Corresponde a padrões típicos de emails produtivos")
    
    if features['word_count'] < 10:
        reasons.append("Email muito curto, típico de mensagens casuais")
    elif features['word_count'] > 30:
        reasons.append("Email detalhado, indicando solicitação formal")
    
    # Análise contextual específica
    text_lower = email_text.lower()
    if any(word in text_lower for word in ['obrigado', 'obrigada', 'thanks']):
        reasons.append("Contém agradecimentos")
    
    if any(word in text_lower for word in ['parabéns', 'felicitações']):
        reasons.append("Contém felicitações")
    
    if not reasons:
        reasons.append("Classificação baseada na análise geral do conteúdo e estrutura")
    
    return "; ".join(reasons) + "."

@app.route('/stats')
def get_stats():
    """Endpoint para estatísticas da API"""
    return jsonify({
        'api_version': '1.0.0',
        'supported_formats': ['.txt', '.pdf'],
        'classification_categories': ['Produtivo', 'Improdutivo'],
        'features': {
            'nlp_processing': True,
            'keyword_analysis': True,
            'pattern_matching': True,
            'automatic_responses': True
        },
        'uptime': datetime.now().isoformat()
    })


if __name__ == '__main__':
    # Configuração para desenvolvimento
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info("Iniciando Sistema de Classificação de Emails...")
    logger.info(f"Servidor rodando na porta {port}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)

    