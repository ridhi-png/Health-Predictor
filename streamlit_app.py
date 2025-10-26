import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import requests
from io import BytesIO

# Set page configuration
st.set_page_config(
    page_title="Health Predictor",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #4CAF50;
        text-align: center;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2E7D32;
    }
    .card {
        border-radius: 5px;
        background-color: #f9f9f9;
        padding: 20px;
        margin-bottom: 10px;
    }
    .highlight {
        background-color: #e8f5e9;
        padding: 20px;
        border-radius: 5px;
        border-left: 5px solid #4CAF50;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1 class='main-header'>Health Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Your natural health assistant that predicts potential health conditions based on symptoms</p>", unsafe_allow_html=True)

# Sidebar
st.sidebar.image("https://via.placeholder.com/150?text=Health+Predictor", use_column_width=True)
st.sidebar.markdown("## Navigation")
page = st.sidebar.radio("Go to", ["Home", "Symptom Checker", "Dashboard", "About"])

# Generate sample data for demonstration
@st.cache_data
def load_sample_data():
    # Sample symptoms
    symptoms = ["Fever", "Cough", "Fatigue", "Shortness of breath", "Headache", 
                "Sore throat", "Congestion", "Nausea", "Diarrhea", "Body aches"]
    
    # Sample diseases
    diseases = ["Common Cold", "Influenza", "COVID-19", "Allergies", "Bronchitis"]
    
    # Sample remedies
    remedies = {
        "Common Cold": ["Rest", "Hydration", "Vitamin C", "Honey and lemon tea"],
        "Influenza": ["Rest", "Antiviral medication", "Hydration", "Pain relievers"],
        "COVID-19": ["Isolation", "Rest", "Hydration", "Medication as advised"],
        "Allergies": ["Antihistamines", "Avoid allergens", "Nasal spray", "Air purifier"],
        "Bronchitis": ["Rest", "Hydration", "Humidifier", "Honey"]
    }
    
    # Sample patient data
    np.random.seed(42)
    patient_data = pd.DataFrame({
        "Patient ID": range(1, 101),
        "Age": np.random.randint(18, 80, 100),
        "Gender": np.random.choice(["Male", "Female"], 100),
        "Symptoms": [", ".join(np.random.choice(symptoms, np.random.randint(1, 5), replace=False)) for _ in range(100)],
        "Diagnosis": np.random.choice(diseases, 100),
        "Report Date": pd.date_range(start="2023-01-01", periods=100)
    })
    
    # Sample disease counts
    disease_counts = patient_data["Diagnosis"].value_counts().reset_index()
    disease_counts.columns = ["Disease", "Count"]
    
    # Sample symptom counts
    symptom_counts = pd.DataFrame({
        "Symptom": symptoms,
        "Count": np.random.randint(10, 50, len(symptoms))
    }).sort_values("Count", ascending=False)
    
    return patient_data, disease_counts, symptom_counts, remedies

patient_data, disease_counts, symptom_counts, remedies = load_sample_data()

# Home page
if page == "Home":
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("<h2 class='sub-header'>Welcome to Health Predictor</h2>", unsafe_allow_html=True)
        st.markdown("""
        <div class="highlight">
        Health Predictor is an intelligent health assistant that helps you identify potential health conditions based on your symptoms. 
        Our application uses advanced algorithms to analyze your symptoms and provide you with possible health conditions, along with natural remedies and lifestyle recommendations.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Key Features")
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.markdown("""
            - **Symptom Analysis**: Input your symptoms and get potential health condition predictions
            - **Patient Management**: Register and manage patient profiles
            - **Health Reports**: Generate and share detailed health reports
            """)
            
        with col_b:
            st.markdown("""
            - **Dashboard**: Visualize health metrics and trends
            - **Natural Remedies**: Get suggestions for natural remedies
            - **Responsive Design**: Works on all devices
            """)
    
    with col2:
        st.image("https://via.placeholder.com/300x400?text=Health+Predictor+App", use_column_width=True)
        st.markdown("<div class='card'>Try our symptom checker to get started!</div>", unsafe_allow_html=True)
        if st.button("Go to Symptom Checker"):
            st.session_state.page = "Symptom Checker"
            st.experimental_rerun()

# Symptom Checker page
elif page == "Symptom Checker":
    st.markdown("<h2 class='sub-header'>Symptom Checker</h2>", unsafe_allow_html=True)
    st.write("Please select your symptoms and their severity to get a health prediction.")
    
    # Sample symptoms for selection
    available_symptoms = ["Fever", "Cough", "Fatigue", "Shortness of breath", "Headache", 
                         "Sore throat", "Congestion", "Nausea", "Diarrhea", "Body aches"]
    
    # Create columns for symptoms selection
    col1, col2 = st.columns(2)
    
    selected_symptoms = {}
    
    with col1:
        st.subheader("Select Symptoms")
        for symptom in available_symptoms[:5]:
            if st.checkbox(symptom):
                severity = st.slider(f"{symptom} Severity", 1, 10, 5)
                selected_symptoms[symptom] = severity
    
    with col2:
        st.subheader("Select Symptoms (continued)")
        for symptom in available_symptoms[5:]:
            if st.checkbox(symptom):
                severity = st.slider(f"{symptom} Severity", 1, 10, 5)
                selected_symptoms[symptom] = severity
    
    # Patient information
    st.subheader("Patient Information")
    col3, col4 = st.columns(2)
    
    with col3:
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=0, max_value=120, value=30)
    
    with col4:
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        existing_conditions = st.multiselect("Existing Conditions", 
                                            ["None", "Diabetes", "Hypertension", "Asthma", "Heart Disease"])
    
    # Prediction button
    if st.button("Get Health Prediction"):
        if not selected_symptoms:
            st.warning("Please select at least one symptom.")
        else:
            with st.spinner("Analyzing symptoms..."):
                # In a real app, this would call your Django API
                # For demo, we'll just show a random prediction
                import time
                time.sleep(2)
                
                # Mock prediction
                if "Fever" in selected_symptoms and "Cough" in selected_symptoms:
                    prediction = "Influenza"
                elif "Headache" in selected_symptoms and "Fatigue" in selected_symptoms:
                    prediction = "Common Cold"
                elif "Shortness of breath" in selected_symptoms:
                    prediction = "COVID-19"
                elif "Congestion" in selected_symptoms and "Sore throat" in selected_symptoms:
                    prediction = "Allergies"
                else:
                    prediction = "Bronchitis"
                
                # Display prediction
                st.success("Analysis complete!")
                st.markdown(f"<h3>Predicted Condition: {prediction}</h3>", unsafe_allow_html=True)
                
                # Display remedies
                st.subheader("Recommended Natural Remedies")
                for i, remedy in enumerate(remedies[prediction]):
                    st.markdown(f"- {remedy}")
                
                # Display disclaimer
                st.info("Disclaimer: This is not a medical diagnosis. Please consult with a healthcare professional for proper medical advice.")

# Dashboard page
elif page == "Dashboard":
    st.markdown("<h2 class='sub-header'>Health Dashboard</h2>", unsafe_allow_html=True)
    
    # Summary metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Patients", len(patient_data))
    with col2:
        st.metric("Conditions Diagnosed", len(disease_counts))
    with col3:
        st.metric("Symptoms Tracked", len(symptom_counts))
    
    # Charts
    st.subheader("Health Condition Distribution")
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.barplot(x="Disease", y="Count", data=disease_counts, ax=ax1)
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45, ha="right")
    st.pyplot(fig1)
    
    st.subheader("Common Symptoms")
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.barplot(x="Symptom", y="Count", data=symptom_counts.head(10), ax=ax2)
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45, ha="right")
    st.pyplot(fig2)
    
    # Recent patients
    st.subheader("Recent Health Reports")
    st.dataframe(patient_data.sort_values("Report Date", ascending=False).head(10))

# About page
elif page == "About":
    st.markdown("<h2 class='sub-header'>About Health Predictor</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
    <p>Health Predictor is a Django-based health prediction application that helps users identify potential health conditions based on their symptoms and provides natural remedies and lifestyle recommendations.</p>
    
    <p>This Streamlit app serves as a demonstration of the Health Predictor project's capabilities. The full application includes more features such as:</p>
    <ul>
        <li>User authentication and profiles</li>
        <li>Detailed patient records</li>
        <li>Advanced symptom analysis</li>
        <li>Comprehensive health reports</li>
        <li>Natural remedy suggestions</li>
        <li>Admin dashboard for healthcare providers</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("Technologies Used")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Backend:**
        - Django
        - Python
        - SQLite/PostgreSQL
        """)
    
    with col2:
        st.markdown("""
        **Frontend:**
        - HTML/CSS
        - JavaScript
        - Bootstrap
        - Chart.js
        """)
    
    st.subheader("Contact")
    st.markdown("For more information, please visit our [GitHub repository](https://github.com/ridhi-png/health-predictor) or contact us at example@healthpredictor.com")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center;'>© 2025 Health Predictor | Created with ❤️ by Ridhi</p>", unsafe_allow_html=True)
