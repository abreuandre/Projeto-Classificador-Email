# Configurações da Aplicação
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=sua-chave-secreta-aqui

# Configurações do Servidor
PORT=5000
HOST=0.0.0.0

# Configurações de CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Configurações de Upload
MAX_CONTENT_LENGTH=16777216  # 16MB

# Configurações de Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_PERIOD=3600  # 1 hora

# Configurações de Log
LOG_LEVEL=INFO
LOG_FILE=logs/app.log

# Configurações de AI/ML (para futuras integrações)
# OPENAI_API_KEY=sua-chave-openai
# HUGGINGFACE_API_KEY=sua-chave-huggingface

# Configurações de Banco de Dados (para futuras versões)
# DATABASE_URL=sqlite:///emails.db

# Configurações de Cache (para otimização)
# REDIS_URL=redis://localhost:6379

# Configurações de Email (para notificações)
# SMTP_SERVER=smtp.gmail.com
# SMTP_PORT=587
# SMTP_USERNAME=seu-email@gmail.com
# SMTP_PASSWORD=sua-senha-de-app