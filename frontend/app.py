import streamlit as st
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import random

st.set_page_config(page_title="PCOS Risk Predictor", layout="wide")

st.markdown(
"""
<h1 style='text-align:center;color:#FF4B4B;'>
AI-Powered PCOS Risk Detection System
</h1>
""",
unsafe_allow_html=True
)

st.write("Enter the patient health parameters below to estimate PCOS risk.")

age = st.number_input("Age")
bmi = st.number_input("BMI")

cycle_input = st.selectbox("Irregular Cycle", ["No", "Yes"])
cycle = 1 if cycle_input == "Yes" else 0

hair_growth_input = st.selectbox("Hair Growth", ["No","Yes"])
hair_growth = 1 if hair_growth_input == "Yes" else 0

skin_darkening_input = st.selectbox("Skin Darkening", ["No","Yes"])
skin_darkening = 1 if skin_darkening_input == "Yes" else 0

weight_gain_input = st.selectbox("Weight Gain", ["No","Yes"])
weight_gain = 1 if weight_gain_input == "Yes" else 0

follicle_left = st.number_input("Follicle Count Left")
follicle_right = st.number_input("Follicle Count Right")
amh = st.number_input("AMH Level")

if st.button("Predict Risk"):

    data = {
        "Age (yrs)": age,
        "BMI": bmi,
        "Cycle(R/I)": cycle,
        "hair growth(Y/N)": hair_growth,
        "Skin darkening (Y/N)": skin_darkening,
        "Weight gain(Y/N)": weight_gain,
        "Follicle No. (L)": follicle_left,
        "Follicle No. (R)": follicle_right,
        "AMH(ng/mL)": amh
    }

    response = requests.post(
        "http://127.0.0.1:8000/predict",
        json=data
    )

    result = response.json()

    prediction_label = "Yes (PCOS Risk)" if result["prediction"] == 1 else "No (Low Risk)"
    probability = result["probability"] * 100

    st.subheader("Prediction Result")
    st.write("PCOS Detected:", prediction_label)
    st.write("Probability:", round(probability,2), "%")

    # Risk level label
    if probability < 30:
        st.success("Risk Level: LOW")
    elif probability < 60:
        st.warning("Risk Level: MODERATE")
    else:
        st.error("Risk Level: HIGH")

    # Gauge meter
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=probability,
        title={'text': "PCOS Risk Level"},
        gauge={
            'axis': {'range': [0,100]},
            'bar': {'color': "red"},
            'steps': [
                {'range':[0,30],'color':'green'},
                {'range':[30,60],'color':'yellow'},
                {'range':[60,100],'color':'red'}
            ]
        }
    ))

    st.plotly_chart(fig, use_container_width=True)

    # Charts side by side
    col1, col2 = st.columns(2)

    with col1:
        labels = ["Low Risk", "PCOS Risk"]
        sizes = [100 - probability, probability]

        fig1, ax1 = plt.subplots(figsize=(3,3))
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax1.set_title("PCOS Risk Distribution")

        st.pyplot(fig1, use_container_width=False)

    with col2:
        features = ["BMI", "AMH", "Follicle Left", "Follicle Right"]
        values = [bmi, amh, follicle_left, follicle_right]

        fig2, ax2 = plt.subplots(figsize=(3.5,2.5))
        sns.barplot(x=features, y=values, ax=ax2)

        ax2.set_title("Health Indicators")

        st.pyplot(fig2, use_container_width=False)

    # Health assessment
    st.subheader("Health Assessment")

    if bmi > 30:
        st.warning("High BMI detected. Lifestyle modification recommended.")

    if amh > 6:
        st.warning("Elevated AMH level detected.")

    if follicle_left > 12 or follicle_right > 12:
        st.warning("High follicle count detected.")

    # Random health tips
    st.subheader("PCOS Health Tips")

    tips = [
        "Exercise regularly to help regulate hormones.",
        "Maintain a balanced diet rich in fiber and protein.",
        "Reduce processed sugars and refined carbs.",
        "Get at least 7–8 hours of quality sleep.",
        "Manage stress through yoga or meditation.",
        "Drink plenty of water daily.",
        "Include omega-3 foods like nuts and seeds.",
        "Track menstrual cycles regularly.",
        "Maintain a healthy body weight.",
        "Eat more vegetables and whole grains.",
        "Avoid sugary drinks and junk food.",
        "Practice mindful eating habits.",
        "Stay physically active daily.",
        "Add anti-inflammatory foods like berries.",
        "Consult a doctor regularly for hormonal checkups."
    ]

    random_tips = random.sample(tips, 5)

    for tip in random_tips:
        st.write("•", tip)