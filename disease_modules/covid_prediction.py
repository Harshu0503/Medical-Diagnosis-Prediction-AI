# covidprediction.py
import streamlit as st
import numpy as np

def validate_inputs(fever, age, selects):
    errors = []
    if fever < 95.0:
        errors.append("Fever")
    if age <= 0:
        errors.append("Age")
    for key, value in selects.items():
        if value == "Select":
            errors.append(key)
    return errors

def show_covid_page(model):
    st.title("🦠 COVID-19 Risk Prediction")

    if model is None:
        st.error("❌ COVID-19 prediction model failed to load.")
        return

    with st.form("covid_form"):
        st.write("#### Patient Symptoms")

        col1, col2 = st.columns(2)

        with col1:
            fever = st.number_input("Fever (in °F) *", min_value=95.0, max_value=110.0, value=98.6)
            dry_cough = st.selectbox("Dry Cough *", ["Select", "No", "Yes"], index=0)
            sore_throat = st.selectbox("Sore Throat *", ["Select", "No", "Yes"], index=0)

        with col2:
            tiredness = st.selectbox("Tiredness *", ["Select", "No", "Yes"], index=0)
            breathing = st.selectbox("Difficulty Breathing *", ["Select", "No", "Yes"], index=0)
            age = st.number_input("Age (years) *", min_value=0, max_value=120, value=25)

        if st.form_submit_button("🔍 Predict COVID Risk", type="primary"):
            selects = {
                "Dry Cough": dry_cough,
                "Sore Throat": sore_throat,
                "Tiredness": tiredness,
                "Difficulty Breathing": breathing
            }

            invalid_fields = validate_inputs(fever, age, selects)

            if invalid_fields:
                st.error("⚠️ Please fill all required fields correctly.")
                for field in invalid_fields:
                    st.markdown(f"❌ **{field}** is required and needs to be valid.")
            else:
                encoded = lambda x: 1 if x == "Yes" else 0
                input_data = [
                    fever,
                    encoded(dry_cough),
                    encoded(sore_throat),
                    encoded(tiredness),
                    encoded(breathing),
                    age
                ]

                prediction = model.predict([input_data])

                st.divider()

                if prediction[0] == 1:
                    st.error("### High Risk of COVID-19 Detected")
                    st.warning("⚠️ Urgent medical attention is recommended.")
                else:
                    st.success("### Low Risk of COVID-19")
                    st.info("✅ Continue monitoring and follow safety guidelines.")
