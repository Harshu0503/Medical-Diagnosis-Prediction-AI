import streamlit as st

def validate_inputs(inputs):
    """Validate that no required fields are zero/empty."""
    invalid_fields = [name for name, value in inputs.items() if value == 0 or value == 0.0]
    if invalid_fields:
        return ("All highlighted fields are required and cannot be zero", invalid_fields)
    return (None, [])

def show_heart_page(model):
    st.title("Heart Disease Prediction")

    # Display a temporary warning message
    st.warning("⚠️ There is a temporary technical issue with heart disease prediction. The service will be working soon. Please try again later.")

    if model is None:
        st.error("Heart disease prediction model failed to load.")
        return

    with st.form("heart_form"):
        st.write("#### Patient Health Metrics")

        col1, col2 = st.columns(2)

        with col1:
            age = st.number_input("Age (years) *", min_value=0, max_value=120, value=0, key="heart_age")
            sex = st.selectbox("Sex *", ["Select Sex", "Male", "Female"], index=0, key="heart_sex")
            cp = st.selectbox("Chest Pain Type *", 
                            ["Select Type", "Typical angina", "Atypical angina", "Non-anginal pain", "Asymptomatic"], 
                            index=0, key="heart_cp")
            trestbps = st.number_input("Resting BP (mmHg) *", min_value=0, max_value=300, value=0, key="heart_bp")
            chol = st.number_input("Cholesterol (mg/dL) *", min_value=0, max_value=600, value=0, key="heart_chol")

        with col2:
            fbs = st.selectbox("Fasting BS >120 mg/dL *", ["Select Option", "Yes", "No"], index=0, key="heart_fbs")
            restecg = st.selectbox("Resting ECG *", 
                                   ["Select Result", "Normal", "ST-T wave abnormality", "Probable LVH"], 
                                   index=0, key="heart_ecg")
            thalach = st.number_input("Max Heart Rate *", min_value=0, max_value=250, value=0, key="heart_thalach")
            exang = st.selectbox("Exercise Induced Angina *", ["Select Option", "Yes", "No"], index=0, key="heart_exang")
            oldpeak = st.number_input("ST Depression *", min_value=0.0, max_value=10.0, value=0.0, step=0.1, key="heart_oldpeak")

        slope = st.selectbox("Slope of ST Segment *", 
                             ["Select Slope", "Upsloping", "Flat", "Downsloping"], 
                             index=0, key="heart_slope")
        ca = st.selectbox("Major Vessels Colored *", options=["Select Number", 0, 1, 2, 3], index=0, key="heart_ca")
        thal = st.selectbox("Thalassemia *", 
                            ["Select Type", "Normal", "Fixed Defect", "Reversible Defect"], 
                            index=0, key="heart_thal")

        if st.form_submit_button("Predict Heart Disease Risk", type="primary"):
            invalid_fields = []

            inputs = {
                "Age": age,
                "Resting BP": trestbps,
                "Cholesterol": chol,
                "Max Heart Rate": thalach,
                "ST Depression": oldpeak
            }

            # Manual selectbox validation
            if sex == "Select Sex":
                invalid_fields.append("Sex")
            if cp == "Select Type":
                invalid_fields.append("Chest Pain Type")
            if fbs == "Select Option":
                invalid_fields.append("Fasting BS >120 mg/dL")
            if restecg == "Select Result":
                invalid_fields.append("Resting ECG")
            if exang == "Select Option":
                invalid_fields.append("Exercise Induced Angina")
            if slope == "Select Slope":
                invalid_fields.append("Slope of ST Segment")
            if ca == "Select Number":
                invalid_fields.append("Major Vessels Colored")
            if thal == "Select Type":
                invalid_fields.append("Thalassemia")

            error_msg, number_invalid_fields = validate_inputs(inputs)
            invalid_fields.extend(number_invalid_fields)

            if error_msg or invalid_fields:
                st.error("All fields marked with * are required")
            else:
                try:
                    # Map categorical inputs to numbers
                    sex_num = 1 if sex == "Male" else 0
                    cp_num = ["Typical angina", "Atypical angina", "Non-anginal pain", "Asymptomatic"].index(cp) + 1
                    fbs_num = 1 if fbs == "Yes" else 0
                    restecg_num = ["Normal", "ST-T wave abnormality", "Probable LVH"].index(restecg)
                    exang_num = 1 if exang == "Yes" else 0
                    slope_num = ["Upsloping", "Flat", "Downsloping"].index(slope)
                    thal_num = ["Normal", "Fixed Defect", "Reversible Defect"].index(thal) + 3
                    ca_num = int(ca)

                    prediction = model.predict([[ 
                        age, sex_num, cp_num, trestbps, chol, fbs_num, 
                        restecg_num, thalach, exang_num, oldpeak, 
                        slope_num, ca_num, thal_num
                    ]])

                    st.divider()

                    if prediction[0] == 1:
                        st.error("### High Risk of Heart Disease Detected")
                        st.warning("""\n⚠️ **Urgent Medical Attention Required**  \nYou are at **high risk** for heart disease.  \nPlease consult a cardiologist immediately!
""")
                        with st.expander("Diagnostic Details", expanded=True):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.metric("Blood Pressure", f"{trestbps} mmHg", delta="High" if trestbps >= 140 else "Normal")
                                st.metric("Cholesterol", f"{chol} mg/dL", delta="High" if chol >= 240 else "Normal")
                            with col2:
                                st.metric("ST Depression", f"{oldpeak:.1f}", delta="Abnormal" if oldpeak > 1 else "Normal")
                                st.metric("Max Heart Rate", f"{thalach} bpm", delta="Low" if thalach < (220 - age) * 0.85 else "Normal")
                            st.warning("""
**Immediate Recommendations:**
- See a cardiologist within 1 week
- Perform ECG & Stress Test
- Follow a strict cardiac diet
- Monitor blood pressure daily
""")
                    else:
                        st.success("### Low Risk of Heart Disease")
                        with st.expander("Health Summary", expanded=True):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.metric("Blood Pressure", f"{trestbps} mmHg")
                                st.metric("Cholesterol", f"{chol} mg/dL")
                            with col2:
                                st.metric("ST Depression", f"{oldpeak:.1f}")
                                st.metric("Max Heart Rate", f"{thalach} bpm")
                            st.info("""
**Preventive Tips:**
- Annual cardiac checkups
- Exercise 150 mins/week
- Eat a heart-healthy diet
- Manage stress and sleep
""")
                except Exception as e:
                    st.error(f"Prediction error: {str(e)}")
