Building a predictive system for blood pressure is a fantastic way to leverage AI for preventative health. Using Streamlit for the frontend and Groq for the high-speed inference makes for a very snappy user experience.

Since I don't have your specific dataset, I’ve designed this application to use a Llama 3 model via Groq to act as an "Intelligent Analyzer." It will process user vitals and provide a risk assessment based on medical guidelines.

1. Project Index
app.py: The main Streamlit application code.

requirements.txt: List of necessary Python libraries.

.env: (To be created by you) To store your GROQ_API_KEY.

2. Requirements.txt
Create a file named requirements.txt and paste the following:

Plaintext
streamlit
groq
python-dotenv
pandas
3. The Application (app.py)
This script handles the UI, data input, and the connection to Groq's API.

Python
import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq Client
# Ensure you have "GROQ_API_KEY" in your environment variables
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Page Configuration
st.set_page_config(page_title="PulseGuard AI", page_icon="❤️", layout="centered")

def get_ai_prediction(age, weight, sys, dia, heart_rate, smoker):
    prompt = f"""
    Act as a medical assistant AI. Analyze the following patient data:
    - Age: {age}
    - Weight: {weight}kg
    - Blood Pressure: {sys}/{dia} mmHg
    - Heart Rate: {heart_rate} bpm
    - Smoker: {smoker}
    
    Provide a concise risk assessment for hypertension or cardiovascular issues. 
    Classify the BP into: Normal, Elevated, Hypertension Stage 1, or Hypertension Stage 2.
    Give 3 actionable health tips. Keep it professional and brief.
    """
    
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama3-8b-8192",
    )
    return chat_completion.choices[0].message.content

# UI Header
st.title("❤️ PulseGuard AI")
st.subheader("Intelligent Blood Pressure Prediction & Analysis")
st.write("Enter your vitals below for an instant AI-powered health assessment.")

# Input Section
with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input("Age", min_value=1, max_value=120, value=30)
        weight = st.number_input("Weight (kg)", min_value=10, max_value=250, value=70)
        smoker = st.selectbox("Smoking Status", ["Non-Smoker", "Occasional", "Regular Smoker"])

    with col2:
        systolic = st.number_input("Systolic BP (Upper)", min_value=70, max_value=250, value=120)
        diastolic = st.number_input("Diastolic BP (Lower)", min_value=40, max_value=150, value=80)
        heart_rate = st.number_input("Heart Rate (bpm)", min_value=30, max_value=200, value=72)

# Prediction Logic
if st.button("Analyze Vitals"):
    with st.spinner("PulseGuard is analyzing your data..."):
        try:
            result = get_ai_prediction(age, weight, systolic, diastolic, heart_rate, smoker)
            
            st.success("Analysis Complete")
            st.markdown("### 📋 AI Assessment")
            st.write(result)
            
            # Simple Visual Indicator
            if systolic < 120 and diastolic < 80:
                st.info("Status: Your BP is within the healthy range.")
            elif systolic >= 140 or diastolic >= 90:
                st.warning("Status: Your readings suggest Stage 2 Hypertension. Please consult a doctor.")
                
        except Exception as e:
            st.error(f"Error: {e}. Please ensure your Groq API Key is set correctly.")

# Footer
st.markdown("---")
st.caption("Disclaimer: This tool is for informational purposes only and is not a substitute for professional medical advice.")
4. How to Run
Get your API Key: Visit the Groq Cloud Console and generate an API key.

Set up your environment:

Create a .env file in the same folder.

Add: GROQ_API_KEY=your_key_here

Install dependencies:

Bash
pip install -r requirements.txt
Launch the App:

Bash
streamlit run app.py
Key Features Added:
Groq Integration: Uses the llama3-8b-8192 model for lightning-fast analysis.

Responsive UI: Uses Streamlit columns and containers for a clean look.

Dynamic Prompting: Passes your specific vitals into the LLM to get a personalized response rather than a hard-coded one.