FROM python:3.9-slim

WORKDIR /app

# Copy requirements first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Set environment variables
ENV PORT 8080  # Cloud Run default port
EXPOSE $PORT

# Use shell form to expand PORT variable
CMD streamlit run app/app.py --server.port=$PORT --server.address=0.0.0.0