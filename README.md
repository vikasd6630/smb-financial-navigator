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