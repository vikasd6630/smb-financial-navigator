import streamlit as st
from app.services.firestore import FirestoreClient
from app.services.vertex_ai import VertexAI
from app.utils.config import settings

# Initialize clients
db = FirestoreClient()
ai = VertexAI()

# App layout
st.set_page_config(page_title="SMB Financial Navigator", layout="wide")
st.title(f"SMB Navigator | {settings.ENVIRONMENT.upper()}")

# Funding Matcher Tab
with st.expander("💰 Funding Recommendations"):
    industry = st.selectbox("Industry", ["Retail", "Tech", "Food"])
    revenue = st.number_input("Annual Revenue ($)", min_value=1000)

    if st.button("Get Recommendations"):
        prompt = f"Recommend funding for {industry} business with ${revenue} revenue"
        recommendations = ai.get_funding_recommendations(prompt)
        st.write(recommendations)
        db.save_funding_query({"industry": industry, "revenue": revenue})