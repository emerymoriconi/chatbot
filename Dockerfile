# Dockerfile

# Stage 1: Build the Python environment
FROM python:3.11-slim as builder

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia apenas o arquivo de requisitos e instala as dependências
# O cache do Docker é usado eficientemente, pois esta etapa só roda se requirements.txt mudar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação
COPY . .

# Comando para rodar a aplicação usando Uvicorn
# O host 0.0.0.0 garante que o container seja acessível externamente
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Exponha a porta que o Uvicorn está escutando
EXPOSE 8000