FROM python:3.9-slim

WORKDIR /app

# Install gcloud CLI for ADC
RUN apt-get update && \
    apt-get install -y curl && \
    curl -sSL https://sdk.cloud.google.com | bash && \
    echo "source /root/google-cloud-sdk/path.bash.inc" >> /root/.bashrc

# Copy app
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Initialize gcloud (for service accounts in production)
CMD ["/bin/bash", "-c", "source /root/google-cloud-sdk/path.bash.inc && \
     gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS} && \
     streamlit run app/main.py --server.port=8080"]