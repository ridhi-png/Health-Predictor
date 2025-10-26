import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import random
import uuid
from PIL import Image
import io

# Set page configuration
st.set_page_config(
    page_title="Health Predictor",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables if they don't exist
if 'patients' not in st.session_state:
    st.session_state.patients = []
if 'symptoms' not in st.session_state:
    st.session_state.symptoms = [
        {"id": 1, "name": "Fever", "description": "Elevated body temperature", "severity_level": 3, "body_part": "Whole body"},
        {"id": 2, "name": "Cough", "description": "Forceful expulsion of air from the lungs", "severity_level": 2, "body_part": "Respiratory"},
        {"id": 3, "name": "Headache", "description": "Pain in the head or upper neck", "severity_level": 2, "body_part": "Head"},
        {"id": 4, "name": "Fatigue", "description": "Extreme tiredness resulting from mental or physical exertion", "severity_level": 2, "body_part": "Whole body"},
        {"id": 5, "name": "Sore Throat", "description": "Pain or irritation in the throat", "severity_level": 2, "body_part": "Throat"},
        {"id": 6, "name": "Shortness of Breath", "description": "Difficulty breathing or catching your breath", "severity_level": 4, "body_part": "Respiratory"},
        {"id": 7, "name": "Nausea", "description": "Feeling of sickness with an inclination to vomit", "severity_level": 3, "body_part": "Stomach"},
        {"id": 8, "name": "Diarrhea", "description": "Loose, watery stools", "severity_level": 3, "body_part": "Digestive"},
        {"id": 9, "name": "Body Aches", "description": "Generalized pain throughout the body", "severity_level": 2, "body_part": "Whole body"},
        {"id": 10, "name": "Loss of Taste or Smell", "description": "Inability to taste or smell", "severity_level": 2, "body_part": "Sensory"}
    ]
if 'diseases' not in st.session_state:
    st.session_state.diseases = [
        {"id": 1, "name": "Common Cold", "description": "A viral infectious disease of the upper respiratory tract", "severity_level": 2, "common_age_group": "All ages", "symptoms": [2, 5, 9]},
        {"id": 2, "name": "Influenza", "description": "A viral infection that attacks your respiratory system", "severity_level": 4, "common_age_group": "All ages", "symptoms": [1, 2, 3, 4, 9]},
        {"id": 3, "name": "COVID-19", "description": "An infectious disease caused by the SARS-CoV-2 virus", "severity_level": 5, "common_age_group": "All ages", "symptoms": [1, 2, 4, 6, 10]},
        {"id": 4, "name": "Gastroenteritis", "description": "Inflammation of the stomach and intestines", "severity_level": 3, "common_age_group": "All ages", "symptoms": [1, 7, 8]},
        {"id": 5, "name": "Migraine", "description": "A headache of varying intensity, often accompanied by nausea and sensitivity to light and sound", "severity_level": 3, "common_age_group": "Adults", "symptoms": [3, 7]}
    ]
if 'remedies' not in st.session_state:
    st.session_state.remedies = [
        {"id": 1, "name": "Rest and Hydration", "remedy_type": "LIFESTYLE", "description": "Getting adequate rest and staying hydrated", "instructions": "Rest as much as possible and drink plenty of fluids", "diseases": [1, 2, 3], "symptoms": [1, 4], "effectiveness_rating": 4},
        {"id": 2, "name": "Ginger Tea", "remedy_type": "NATURAL", "description": "Tea made from ginger root", "instructions": "Steep fresh ginger in hot water for 10 minutes and drink", "diseases": [4], "symptoms": [7], "effectiveness_rating": 3},
        {"id": 3, "name": "Honey and Lemon", "remedy_type": "NATURAL", "description": "Mixture of honey and lemon juice", "instructions": "Mix 1 tablespoon of honey with juice from half a lemon in warm water", "diseases": [1], "symptoms": [2, 5], "effectiveness_rating": 3},
        {"id": 4, "name": "Yoga Breathing", "remedy_type": "YOGA", "description": "Deep breathing exercises", "instructions": "Practice deep breathing for 10 minutes, 3 times a day", "diseases": [3], "symptoms": [6], "effectiveness_rating": 2},
        {"id": 5, "name": "BRAT Diet", "remedy_type": "DIET", "description": "Bananas, Rice, Applesauce, Toast diet", "instructions": "Eat only bananas, rice, applesauce, and toast until symptoms improve", "diseases": [4], "symptoms": [8], "effectiveness_rating": 4}
    ]
if 'reports' not in st.session_state:
    st.session_state.reports = []
if 'selected_symptoms' not in st.session_state:
    st.session_state.selected_symptoms = []
if 'symptom_data' not in st.session_state:
    st.session_state.symptom_data = {}
if 'current_patient' not in st.session_state:
    st.session_state.current_patient = None

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #4A90E2;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #5C5C5C;
        margin-bottom: 1rem;
    }
    .card {
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        background-color: white;
    }
    .info-box {
        background-color: #E8F4FD;
        border-left: 5px solid #4A90E2;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .warning-box {
        background-color: #FFF3CD;
        border-left: 5px solid #FFC107;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .success-box {
        background-color: #D4EDDA;
        border-left: 5px solid #28A745;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .metric-card {
        text-align: center;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        background-color: white;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #4A90E2;
    }
    .metric-label {
        font-size: 1rem;
        color: #5C5C5C;
    }
</style>
""", unsafe_allow_html=True)

# Helper functions
def get_symptom_by_id(symptom_id):
    for symptom in st.session_state.symptoms:
        if symptom["id"] == symptom_id:
            return symptom
    return None

def get_disease_by_id(disease_id):
    for disease in st.session_state.diseases:
        if disease["id"] == disease_id:
            return disease
    return None

def get_remedy_by_id(remedy_id):
    for remedy in st.session_state.remedies:
        if remedy["id"] == remedy_id:
            return remedy
    return None

def get_patient_by_id(patient_id):
    for patient in st.session_state.patients:
        if patient["id"] == patient_id:
            return patient
    return None

def get_report_by_id(report_id):
    for report in st.session_state.reports:
        if report["id"] == report_id:
            return report
    return None

def predict_diseases(symptom_ids):
    """Predict diseases based on symptoms"""
    if not symptom_ids:
        return []
    
    disease_scores = []
    for disease in st.session_state.diseases:
        common_symptoms = set(disease["symptoms"]).intersection(set(symptom_ids))
        if common_symptoms:
            score = len(common_symptoms) / len(disease["symptoms"]) * 100
            disease_scores.append((disease, score))
    
    # Sort by score (descending)
    disease_scores.sort(key=lambda x: x[1], reverse=True)
    return disease_scores[:5]  # Return top 5 diseases

def recommend_remedies(disease_ids, symptom_ids):
    """Recommend remedies based on diseases and symptoms"""
    if not disease_ids and not symptom_ids:
        return []
    
    recommended_remedies = []
    for remedy in st.session_state.remedies:
        # Check if remedy is for any of the diseases or symptoms
        if (set(remedy["diseases"]).intersection(set(disease_ids)) or 
            set(remedy["symptoms"]).intersection(set(symptom_ids))):
            recommended_remedies.append(remedy)
    
    # Sort by effectiveness rating (descending)
    recommended_remedies.sort(key=lambda x: x["effectiveness_rating"], reverse=True)
    return recommended_remedies

def generate_chart_data():
    """Generate random data for charts"""
    dates = [(datetime.datetime.now() - datetime.timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)]
    symptom_counts = [random.randint(5, 20) for _ in range(7)]
    disease_counts = [random.randint(3, 15) for _ in range(7)]
    
    return dates, symptom_counts, disease_counts

def create_chart():
    """Create a chart for the dashboard"""
    dates, symptom_counts, disease_counts = generate_chart_data()
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(dates, symptom_counts, marker='o', linewidth=2, label='Symptoms')
    ax.plot(dates, disease_counts, marker='s', linewidth=2, label='Conditions')
    
    ax.set_xlabel('Date')
    ax.set_ylabel('Count')
    ax.set_title('Health Trends - Last 7 Days')
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend()
    
    # Rotate date labels for better readability
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    return fig

# Navigation
def navigation():
    st.sidebar.title("Health Predictor")
    
    menu = st.sidebar.radio(
        "Navigation",
        ["Home", "Symptom Checker", "Dashboard", "Patients", "About"]
    )
    
    if menu == "Home":
        home_page()
    elif menu == "Symptom Checker":
        symptom_checker_page()
    elif menu == "Dashboard":
        dashboard_page()
    elif menu == "Patients":
        patients_page()
    elif menu == "About":
        about_page()

# Pages
def home_page():
    st.markdown('<h1 class="main-header">Welcome to Health Predictor</h1>', unsafe_allow_html=True)
    
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown("""
    Health Predictor is an AI-powered health assessment tool that helps you identify potential health conditions 
    based on your symptoms and provides natural remedy recommendations.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 🔍 Symptom Checker")
        st.markdown("Identify potential health conditions based on your symptoms.")
        st.button("Check Symptoms", key="home_check_symptoms", on_click=lambda: st.session_state.update({"_current_page": "Symptom Checker"}))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 📊 Health Dashboard")
        st.markdown("View health metrics and trends.")
        st.button("View Dashboard", key="home_view_dashboard", on_click=lambda: st.session_state.update({"_current_page": "Dashboard"}))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 👥 Patient Management")
        st.markdown("Manage patient records and health reports.")
        st.button("Manage Patients", key="home_manage_patients", on_click=lambda: st.session_state.update({"_current_page": "Patients"}))
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("## How It Works")
    st.markdown("""
    1. **Enter your symptoms** - Select from our comprehensive list of symptoms
    2. **Rate severity and duration** - Provide details about your symptoms
    3. **Get predictions** - Our AI analyzes your symptoms to identify potential conditions
    4. **View recommendations** - Receive personalized natural remedy suggestions
    """)
    
    st.markdown("## Disclaimer")
    st.markdown('<div class="warning-box">', unsafe_allow_html=True)
    st.markdown("""
    This application is for informational purposes only and is not a substitute for professional medical advice, 
    diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any 
    questions you may have regarding a medical condition.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

def symptom_checker_page():
    st.markdown('<h1 class="main-header">Symptom Checker</h1>', unsafe_allow_html=True)
    
    # Step 1: Select Patient (optional)
    st.markdown('<h2 class="sub-header">Step 1: Select Patient (Optional)</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.session_state.patients:
            patient_options = ["None"] + [f"{p['name']} ({p['age']})" for p in st.session_state.patients]
            selected_patient_index = st.selectbox("Select Patient", options=range(len(patient_options)), format_func=lambda x: patient_options[x])
            
            if selected_patient_index > 0:
                st.session_state.current_patient = st.session_state.patients[selected_patient_index - 1]
            else:
                st.session_state.current_patient = None
        else:
            st.info("No patients available. You can add a patient or continue without selecting one.")
            st.session_state.current_patient = None
    
    with col2:
        if st.button("Add New Patient"):
            st.session_state.update({"_current_page": "Patients", "_add_new": True})
    
    # Display current patient info if selected
    if st.session_state.current_patient:
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown(f"**Selected Patient:** {st.session_state.current_patient['name']}, {st.session_state.current_patient['age']} years, {st.session_state.current_patient['gender']}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Step 2: Select Symptoms
    st.markdown('<h2 class="sub-header">Step 2: Select Symptoms</h2>', unsafe_allow_html=True)
    
    # Search for symptoms
    search_query = st.text_input("Search for symptoms", "")
    
    # Filter symptoms based on search query
    filtered_symptoms = st.session_state.symptoms
    if search_query:
        filtered_symptoms = [s for s in st.session_state.symptoms if search_query.lower() in s["name"].lower()]
    
    # Display symptoms as checkboxes
    selected_symptom_ids = []
    
    # Create columns for symptoms
    cols = st.columns(3)
    for i, symptom in enumerate(filtered_symptoms):
        col_index = i % 3
        with cols[col_index]:
            if st.checkbox(f"{symptom['name']} ({symptom['body_part']})", key=f"symptom_{symptom['id']}"):
                selected_symptom_ids.append(symptom["id"])
    
    st.session_state.selected_symptoms = selected_symptom_ids
    
    # Step 3: Symptom Details
    if selected_symptom_ids:
        st.markdown('<h2 class="sub-header">Step 3: Symptom Details</h2>', unsafe_allow_html=True)
        
        for symptom_id in selected_symptom_ids:
            symptom = get_symptom_by_id(symptom_id)
            st.markdown(f"### {symptom['name']}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                severity = st.slider(f"Severity of {symptom['name']}", 1, 10, 5, key=f"severity_{symptom_id}")
            
            with col2:
                duration_options = ["Less than a day", "1-3 days", "4-7 days", "1-2 weeks", "More than 2 weeks"]
                duration = st.selectbox(f"Duration of {symptom['name']}", duration_options, key=f"duration_{symptom_id}")
            
            # Store symptom data
            if symptom_id not in st.session_state.symptom_data:
                st.session_state.symptom_data[symptom_id] = {}
            
            st.session_state.symptom_data[symptom_id]["severity"] = severity
            st.session_state.symptom_data[symptom_id]["duration"] = duration
        
        # Step 4: Get Prediction
        st.markdown('<h2 class="sub-header">Step 4: Get Prediction</h2>', unsafe_allow_html=True)
        
        if st.button("Analyze Symptoms"):
            if not selected_symptom_ids:
                st.error("Please select at least one symptom.")
            else:
                # Redirect to prediction results
                st.session_state.update({"_show_prediction": True})
                st.experimental_rerun()
    
    # Show prediction results
    if "_show_prediction" in st.session_state and st.session_state._show_prediction:
        show_prediction_results()
        # Reset the flag after showing results
        st.session_state._show_prediction = False

def show_prediction_results():
    st.markdown('<h1 class="main-header">Health Prediction Results</h1>', unsafe_allow_html=True)
    
    # Display disclaimer
    st.markdown('<div class="warning-box">', unsafe_allow_html=True)
    st.markdown("""
    **Disclaimer:** These results are based on the symptoms you provided and are not a substitute for professional 
    medical advice. Please consult with a healthcare provider for proper diagnosis and treatment.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display selected patient if any
    if st.session_state.current_patient:
        st.markdown(f"### Results for {st.session_state.current_patient['name']}")
    
    # Display symptoms recap
    st.markdown("### Your Symptoms")
    
    symptom_data = []
    for symptom_id in st.session_state.selected_symptoms:
        symptom = get_symptom_by_id(symptom_id)
        severity = st.session_state.symptom_data[symptom_id]["severity"]
        duration = st.session_state.symptom_data[symptom_id]["duration"]
        symptom_data.append({
            "Symptom": symptom["name"],
            "Body Part": symptom["body_part"],
            "Severity": f"{severity}/10",
            "Duration": duration
        })
    
    if symptom_data:
        st.table(pd.DataFrame(symptom_data))
    
    # Predict diseases
    disease_predictions = predict_diseases(st.session_state.selected_symptoms)
    
    # Display predicted diseases
    st.markdown("### Potential Health Conditions")
    
    if disease_predictions:
        disease_ids = [disease[0]["id"] for disease in disease_predictions]
        
        for disease, score in disease_predictions:
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**{disease['name']}** (Match: {score:.1f}%)")
                st.markdown(disease["description"])
            
            with col2:
                # Display severity level with color
                severity = disease["severity_level"]
                color = "green"
                if severity > 3:
                    color = "orange"
                if severity > 7:
                    color = "red"
                
                st.markdown(f"**Severity:** <span style='color:{color};'>{severity}/10</span>", unsafe_allow_html=True)
                st.markdown(f"**Age Group:** {disease['common_age_group']}")
            
            st.markdown("---")
        
        # Recommend remedies
        recommended_remedies = recommend_remedies(disease_ids, st.session_state.selected_symptoms)
        
        st.markdown("### Recommended Remedies")
        
        if recommended_remedies:
            for remedy in recommended_remedies:
                st.markdown(f"#### {remedy['name']} ({remedy['remedy_type'].capitalize()})")
                st.markdown(remedy["description"])
                st.markdown(f"**Instructions:** {remedy['instructions']}")
                st.markdown(f"**Effectiveness Rating:** {'⭐' * remedy['effectiveness_rating']}")
                st.markdown("---")
        else:
            st.info("No specific remedies found for your symptoms.")
        
        # Create report if patient is selected
        if st.session_state.current_patient:
            if st.button("Save Report"):
                # Create a new report
                new_report = {
                    "id": str(uuid.uuid4()),
                    "patient_id": st.session_state.current_patient["id"],
                    "title": f"Health Report - {datetime.datetime.now().strftime('%Y-%m-%d')}",
                    "symptoms": st.session_state.selected_symptoms,
                    "symptom_data": st.session_state.symptom_data,
                    "predicted_diseases": [d[0]["id"] for d in disease_predictions],
                    "recommended_remedies": [r["id"] for r in recommended_remedies],
                    "created_at": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "status": "COMPLETED"
                }
                
                st.session_state.reports.append(new_report)
                st.success("Report saved successfully!")
    else:
        st.info("No health conditions could be predicted based on the provided symptoms.")
    
    # Reset button
    if st.button("Start New Assessment"):
        st.session_state.selected_symptoms = []
        st.session_state.symptom_data = {}
        st.session_state.current_patient = None
        st.experimental_rerun()

def dashboard_page():
    st.markdown('<h1 class="main-header">Health Dashboard</h1>', unsafe_allow_html=True)
    
    # Health metrics
    st.markdown('<h2 class="sub-header">Health Metrics</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{len(st.session_state.patients)}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Total Patients</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{len(st.session_state.reports)}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Health Reports</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{len(st.session_state.symptoms)}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Tracked Symptoms</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Health trends chart
    st.markdown('<h2 class="sub-header">Health Trends</h2>', unsafe_allow_html=True)
    
    chart = create_chart()
    st.pyplot(chart)
    
    # Recent reports and common conditions
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<h2 class="sub-header">Recent Reports</h2>', unsafe_allow_html=True)
        
        recent_reports = sorted(st.session_state.reports, key=lambda x: x["created_at"], reverse=True)[:5]
        
        if recent_reports:
            for report in recent_reports:
                patient = get_patient_by_id(report["patient_id"])
                if patient:
                    st.markdown(f"**{report['title']}** - {patient['name']}")
                    st.markdown(f"Created: {report['created_at']} | Status: {report['status']}")
                    st.markdown("---")
        else:
            st.info("No reports available.")
    
    with col2:
        st.markdown('<h2 class="sub-header">Common Conditions</h2>', unsafe_allow_html=True)
        
        # Count diseases in reports
        disease_counts = {}
        for report in st.session_state.reports:
            for disease_id in report["predicted_diseases"]:
                if disease_id in disease_counts:
                    disease_counts[disease_id] += 1
                else:
                    disease_counts[disease_id] = 1
        
        # Sort by count
        sorted_diseases = sorted(disease_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        if sorted_diseases:
            for disease_id, count in sorted_diseases:
                disease = get_disease_by_id(disease_id)
                if disease:
                    st.markdown(f"**{disease['name']}** - {count} cases")
                    st.markdown(f"Severity: {disease['severity_level']}/10")
                    st.markdown("---")
        else:
            st.info("No common conditions to display.")

def patients_page():
    st.markdown('<h1 class="main-header">Patient Management</h1>', unsafe_allow_html=True)
    
    # Check if we should show the add patient form
    show_add_form = False
    if "_add_new" in st.session_state and st.session_state._add_new:
        show_add_form = True
        st.session_state._add_new = False
    
    tab1, tab2 = st.tabs(["Patient List", "Add Patient"])
    
    # If redirected to add patient, switch to that tab
    if show_add_form:
        tab2.markdown('<h2 class="sub-header">Add New Patient</h2>', unsafe_allow_html=True)
        add_patient_form(tab2)
    
    # Patient List Tab
    with tab1:
        st.markdown('<h2 class="sub-header">Patient List</h2>', unsafe_allow_html=True)
        
        if st.session_state.patients:
            # Search functionality
            search_query = st.text_input("Search patients by name", key="patient_search")
            
            filtered_patients = st.session_state.patients
            if search_query:
                filtered_patients = [p for p in st.session_state.patients if search_query.lower() in p["name"].lower()]
            
            # Display patients
            for patient in filtered_patients:
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.markdown(f"**{patient['name']}** ({patient['age']} years, {patient['gender']})")
                    if patient.get("email"):
                        st.markdown(f"Email: {patient['email']} | Phone: {patient.get('phone', 'N/A')}")
                
                with col2:
                    # Count reports for this patient
                    patient_reports = [r for r in st.session_state.reports if r["patient_id"] == patient["id"]]
                    st.markdown(f"Reports: {len(patient_reports)}")
                
                with col3:
                    if st.button("View Details", key=f"view_{patient['id']}"):
                        st.session_state.update({"_view_patient": patient["id"]})
                        st.experimental_rerun()
                
                st.markdown("---")
        else:
            st.info("No patients available. Add a patient to get started.")
    
    # Add Patient Tab
    with tab2:
        if not show_add_form:
            st.markdown('<h2 class="sub-header">Add New Patient</h2>', unsafe_allow_html=True)
            add_patient_form(tab2)
    
    # View patient details if selected
    if "_view_patient" in st.session_state:
        patient_id = st.session_state._view_patient
        patient = get_patient_by_id(patient_id)
        
        if patient:
            st.markdown('<h2 class="sub-header">Patient Details</h2>', unsafe_allow_html=True)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"### {patient['name']}")
                st.markdown(f"**Age:** {patient['age']} years")
                st.markdown(f"**Gender:** {patient['gender']}")
                st.markdown(f"**Email:** {patient.get('email', 'N/A')}")
                st.markdown(f"**Phone:** {patient.get('phone', 'N/A')}")
                
                if patient.get("address"):
                    st.markdown(f"**Address:** {patient['address']}")
                
                if patient.get("medical_history"):
                    st.markdown(f"**Medical History:** {patient['medical_history']}")
            
            with col2:
                if st.button("Start Symptom Check"):
                    st.session_state.current_patient = patient
                    st.session_state.update({"_current_page": "Symptom Checker"})
                    st.session_state.pop("_view_patient", None)
                    st.experimental_rerun()
                
                if st.button("Edit Patient"):
                    st.session_state.update({"_edit_patient": patient["id"]})
                    st.experimental_rerun()
            
            # Display patient reports
            st.markdown("### Patient Reports")
            
            patient_reports = [r for r in st.session_state.reports if r["patient_id"] == patient["id"]]
            
            if patient_reports:
                for report in sorted(patient_reports, key=lambda x: x["created_at"], reverse=True):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"**{report['title']}**")
                        st.markdown(f"Created: {report['created_at']} | Status: {report['status']}")
                    
                    with col2:
                        if st.button("View Report", key=f"view_report_{report['id']}"):
                            st.session_state.update({"_view_report": report["id"]})
                            st.experimental_rerun()
                    
                    st.markdown("---")
            else:
                st.info("No reports available for this patient.")
            
            # Back button
            if st.button("Back to Patient List"):
                st.session_state.pop("_view_patient", None)
                st.experimental_rerun()
        
        # Clear the view patient flag
        st.session_state.pop("_view_patient", None)
    
    # View report if selected
    if "_view_report" in st.session_state:
        report_id = st.session_state._view_report
        report = get_report_by_id(report_id)
        
        if report:
            st.markdown('<h2 class="sub-header">Report Details</h2>', unsafe_allow_html=True)
            
            patient = get_patient_by_id(report["patient_id"])
            
            st.markdown(f"### {report['title']}")
            st.markdown(f"**Patient:** {patient['name'] if patient else 'Unknown'}")
            st.markdown(f"**Created:** {report['created_at']}")
            st.markdown(f"**Status:** {report['status']}")
            
            # Display symptoms
            st.markdown("### Symptoms")
            
            symptom_data = []
            for symptom_id in report["symptoms"]:
                symptom = get_symptom_by_id(symptom_id)
                if symptom and symptom_id in report["symptom_data"]:
                    severity = report["symptom_data"][symptom_id]["severity"]
                    duration = report["symptom_data"][symptom_id]["duration"]
                    symptom_data.append({
                        "Symptom": symptom["name"],
                        "Body Part": symptom["body_part"],
                        "Severity": f"{severity}/10",
                        "Duration": duration
                    })
            
            if symptom_data:
                st.table(pd.DataFrame(symptom_data))
            
            # Display predicted diseases
            st.markdown("### Predicted Conditions")
            
            for disease_id in report["predicted_diseases"]:
                disease = get_disease_by_id(disease_id)
                if disease:
                    st.markdown(f"**{disease['name']}**")
                    st.markdown(disease["description"])
                    st.markdown(f"Severity: {disease['severity_level']}/10")
                    st.markdown("---")
            
            # Display recommended remedies
            st.markdown("### Recommended Remedies")
            
            for remedy_id in report["recommended_remedies"]:
                remedy = get_remedy_by_id(remedy_id)
                if remedy:
                    st.markdown(f"**{remedy['name']}** ({remedy['remedy_type'].capitalize()})")
                    st.markdown(remedy["description"])
                    st.markdown(f"Instructions: {remedy['instructions']}")
                    st.markdown(f"Effectiveness Rating: {'⭐' * remedy['effectiveness_rating']}")
                    st.markdown("---")
            
            # Back button
            if st.button("Back to Patient Details"):
                st.session_state.update({"_view_patient": report["patient_id"]})
                st.session_state.pop("_view_report", None)
                st.experimental_rerun()
        
        # Clear the view report flag
        st.session_state.pop("_view_report", None)

def add_patient_form(container):
    with container:
        with st.form("add_patient_form"):
            name = st.text_input("Name*")
            
            col1, col2 = st.columns(2)
            
            with col1:
                age = st.number_input("Age*", min_value=0, max_value=120, value=30)
            
            with col2:
                gender = st.selectbox("Gender*", ["Male", "Female", "Other"])
            
            email = st.text_input("Email")
            phone = st.text_input("Phone")
            address = st.text_area("Address")
            medical_history = st.text_area("Medical History")
            
            submitted = st.form_submit_button("Add Patient")
            
            if submitted:
                if not name:
                    st.error("Name is required.")
                else:
                    # Create new patient
                    new_patient = {
                        "id": str(uuid.uuid4()),
                        "name": name,
                        "age": age,
                        "gender": gender,
                        "email": email,
                        "phone": phone,
                        "address": address,
                        "medical_history": medical_history,
                        "created_at": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
                    st.session_state.patients.append(new_patient)
                    st.success(f"Patient {name} added successfully!")
                    
                    # Clear form by triggering a rerun
                    st.experimental_rerun()

def about_page():
    st.markdown('<h1 class="main-header">About Health Predictor</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    Health Predictor is an AI-powered health assessment tool designed to help users identify potential health conditions 
    based on their symptoms and provide natural remedy recommendations.
    
    ### Features
    
    - **Symptom Analysis**: Select from a comprehensive list of symptoms and provide details about severity and duration.
    - **Health Prediction**: AI-powered analysis to identify potential health conditions based on symptoms.
    - **Natural Remedies**: Recommendations for natural remedies, yoga practices, and lifestyle changes.
    - **Patient Management**: Store and manage patient information and health reports.
    - **Health Dashboard**: View health metrics and trends.
    
    ### How It Works
    
    1. **Enter your symptoms** - Select from our comprehensive list of symptoms
    2. **Rate severity and duration** - Provide details about your symptoms
    3. **Get predictions** - Our AI analyzes your symptoms to identify potential conditions
    4. **View recommendations** - Receive personalized natural remedy suggestions
    
    ### Disclaimer
    
    This application is for informational purposes only and is not a substitute for professional medical advice, 
    diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any 
    questions you may have regarding a medical condition.
    """)
    
    st.markdown("### Contact")
    st.markdown("For questions or support, please contact us at support@healthpredictor.com")
    
    st.markdown("### Version")
    st.markdown("Health Predictor v1.0.0")

# Main app
def main():
    navigation()

if __name__ == "__main__":
    main()
