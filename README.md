# SMB Financial Navigator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

AI-powered financial management tool for small businesses with:
- **Budget analysis** using Gemini AI
- **Funding recommendations** via Vertex AI
- **Firestore integration** for data persistence
- **Cloud-ready** Docker packaging

![App Screenshot](docs/screenshot.png)

## 🚀 Quick Start

### Prerequisites
- Google Cloud account with billing enabled
- Python 3.9+
- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)

### Local Development
1. **Authenticate with GCP**:
   ```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   gcloud services enable firestore.googleapis.com aiplatform.googleapis.com

2. **Set up environment**:
    ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   pip install -r requirements.txt
3. **Run The App**:
   ```bash
   streamlit run app/main.py

## 🚀 GCP Deployment

### **Prerequisites**
- Google Cloud account with billing enabled
- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) installed
- Python 3.9+

### **1. Infrastructure Setup**
      
   ```bash
   
   UserWarning: Your application has authenticated using end user credentials from Google Cloud SDK without a quota project. You might receive a "quota exceeded" or "API not enabled" error. See the following page for troubleshooting:
   
   FIX :: export GOOGLE_APPLICATION_CREDENTIALS=service-account.json
   
   python -m app.main
   
# Enable required APIs
gcloud services enable \
  firestore.googleapis.com \
  aiplatform.googleapis.com \
  cloudbuild.googleapis.com \
  run.googleapis.com

# Create Firestore database (Native mode)
gcloud app create --region=us-central  # Required for Firestore


### **Deploy to Cloud Run**
# Build and push container
gcloud builds submit --tag gcr.io/$GCP_PROJECT_ID/smb-navigator

# Deploy with secrets
gcloud run deploy smb-navigator \
  --image gcr.io/$GCP_PROJECT_ID/smb-navigator \
  --platform managed \
  --region us-central1 \
  --set-env-vars "GCP_PROJECT_ID=$GCP_PROJECT_ID" \
  --allow-unauthenticated \
  --service-account=smb-navigator@$GCP_PROJECT_ID.iam.gserviceaccount.com

### **Configure Services**

# Grant service account permissions
gcloud projects add-iam-policy-binding $GCP_PROJECT_ID \
  --member="serviceAccount:smb-navigator@$GCP_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/datastore.user"

gcloud projects add-iam-policy-binding $GCP_PROJECT_ID \
  --member="serviceAccount:smb-navigator@$GCP_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"

### **Project Structure**

/smb-financial-navigator
├── .cloudbuild/               # CI/CD configurations
│   └── cloudbuild.yaml
├── app/
│   ├── __init__.py            # Package initialization
│   ├── main.py                # Streamlit entrypoint
│   ├── services/              # Cloud integrations
│   │   ├── firestore.py       # Firestore client
│   │   └── vertex_ai.py       # Gemini/VertexAI service
│   └── utils/
│       ├── config.py          # Environment management
│       └── logger.py          # Cloud Logging setup
├── tests/                     # Unit tests
├── .env                       # Local environment variables
├── .gcloudignore              # Files excluded from GCP builds
├── Dockerfile                 # Container definition
├── requirements.txt           # Python dependencies
└── README.md                  # This file


## 🔐 IAM Requirements

Service	Role	Purpose
Cloud Run	roles/run.admin	Deploy services
Firestore	roles/datastore.user	Database access
Vertex AI	roles/aiplatform.user	Model predictions
Secret Manager	roles/secretmanager.secretAccessor	API key access
