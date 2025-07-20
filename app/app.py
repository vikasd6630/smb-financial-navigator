# app.py - Main Application File
import streamlit as st
import google.generativeai as genai
from google.cloud import firestore
import pandas as pd
import vertexai
from vertexai.preview.language_models import TextGenerationModel
from datetime import datetime

# Configuration
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
vertexai.init(project=st.secrets["GCP_PROJECT_ID"], location="us-central1")
db = firestore.Client.from_service_account_json("service-account.json")

# Initialize models
gemini_model = genai.GenerativeModel('gemini-pro')
vertex_model = TextGenerationModel.from_pretrained("text-bison@001")

# Page setup
st.set_page_config(page_title="SMB Financial Navigator", layout="wide")
st.title("📊 SMB Financial Navigator")


# Sample data loading
@st.cache_data
def load_sample_data():
    return pd.read_csv("data/sample_transactions.csv")


# Tabs interface
tab1, tab2, tab3 = st.tabs(["💰 Budget Analysis", "💸 Funding Matcher", "📈 Financial Health"])

# Tab 1: Budget Analysis
with tab1:
    st.subheader("AI-Powered Budget Insights")

    analysis_type = st.radio("Data Source", ["Upload CSV", "Use Sample Data"])

    if analysis_type == "Upload CSV":
        uploaded_file = st.file_uploader("Upload transactions (CSV)")
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
    else:
        df = load_sample_data()

    if 'df' in locals():
        st.write("### Transaction Overview")
        st.dataframe(df.head())

        if st.button("Analyze with Gemini"):
            with st.spinner("Generating insights..."):
                prompt = f"""
                Analyze this business transaction data:
                {df.head(20).to_string()}

                Provide:
                1. Top 3 spending categories
                2. Cash flow warnings
                3. Cost optimization recommendations
                Format as markdown bullets.
                """
                response = gemini_model.generate_content(prompt)
                st.markdown(response.text)

                # Save analysis to Firestore
                analysis_ref = db.collection("budget_analyses").document()
                analysis_ref.set({
                    "timestamp": datetime.now(),
                    "insights": response.text,
                    "source": "Gemini Pro"
                })

# Tab 2: Funding Matcher
with tab2:
    st.subheader("Personalized Funding Recommendations")

    with st.form("funding_profile"):
        col1, col2 = st.columns(2)
        with col1:
            industry = st.selectbox("Industry", ["Retail", "Technology", "Food Service", "Healthcare"])
            revenue = st.number_input("Annual Revenue ($)", min_value=0, value=100000)
        with col2:
            credit_score = st.slider("Credit Score", 300, 850, 700)
            funding_needs = st.multiselect("Funding Needs",
                                           ["Working Capital", "Equipment", "Inventory", "Expansion"])

        submitted = st.form_submit_button("Find Funding Options")

    if submitted:
        with st.spinner("Querying Vertex AI..."):
            prompt = f"""
            Recommend funding options for:
            - Industry: {industry}
            - Annual Revenue: ${revenue:,}
            - Credit Score: {credit_score}
            - Needs: {', '.join(funding_needs)}

            Include:
            1. Loan types (term, line of credit, etc.)
            2. Typical amounts and terms
            3. Eligibility requirements
            4. Potential lenders
            Format as markdown.
            """

            response = vertex_model.predict(
                prompt,
                temperature=0.3,
                max_output_tokens=1024,
                top_k=40,
                top_p=0.8
            )

            st.markdown(response.text)

            # Save to Firestore
            db.collection("funding_queries").add({
                "timestamp": datetime.now(),
                "profile": {
                    "industry": industry,
                    "revenue": revenue,
                    "credit_score": credit_score,
                    "needs": funding_needs
                },
                "recommendations": response.text
            })

# Tab 3: Financial Health
with tab3:
    st.subheader("Comprehensive Financial Assessment")

    with st.expander("Enter Financial Data"):
        col1, col2 = st.columns(2)
        with col1:
            assets = st.number_input("Total Assets ($)", value=250000)
            liabilities = st.number_input("Total Liabilities ($)", value=100000)
        with col2:
            monthly_revenue = st.number_input("Monthly Revenue ($)", value=50000)
            monthly_expenses = st.number_input("Monthly Expenses ($)", value=35000)

    if st.button("Generate Health Report"):
        with st.spinner("Running diagnostics..."):
            # Quantitative analysis
            current_ratio = assets / liabilities if liabilities > 0 else float('inf')
            profit_margin = (monthly_revenue - monthly_expenses) / monthly_revenue if monthly_revenue > 0 else 0

            # Qualitative analysis
            prompt = f"""
            Business Financial Snapshot:
            - Assets: ${assets:,}
            - Liabilities: ${liabilities:,}
            - Monthly Revenue: ${monthly_revenue:,}
            - Monthly Expenses: ${monthly_expenses:,}

            Provide:
            1. Financial health score (1-10)
            2. Key strengths
            3. Major risks
            4. Strategic recommendations
            Format as markdown with headers.
            """

            gemini_response = gemini_model.generate_content(prompt)
            st.markdown(gemini_response.text)

            # Save report
            db.collection("health_reports").add({
                "timestamp": datetime.now(),
                "metrics": {
                    "current_ratio": current_ratio,
                    "profit_margin": profit_margin
                },
                "analysis": gemini_response.text
            })

# Footer
st.sidebar.markdown("""
## Configuration
Set these secrets in `.streamlit/secrets.toml`:
```toml
GEMINI_API_KEY = "GEMINI_API_KEY"
GCP_PROJECT_ID = "GCP_PROJECT_ID"
""")