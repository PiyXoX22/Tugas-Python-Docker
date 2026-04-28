# Gunakan python ringan
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy file
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose port streamlit
EXPOSE 8501

# Run streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]