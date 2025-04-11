import streamlit as st
import numpy as np

def validate_inputs(inputs):
    """Validate that no required fields are zero/empty"""
    invalid_fields = [name for name, value in inputs.items() if value == 0]
    if invalid_fields:
        return ("All highlighted fields are required and cannot be zero", invalid_fields)
    return (None, [])

def show_heart_page(model):
    st.title("Heart Disease Prediction")
    
    if model is None:
        st.error("Heart disease prediction model failed to load")
        return
    
    with st.form("heart_form"):
        st.write("#### Cardiovascular Health Metrics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.number_input("Age (years)", min_value=0, max_value=120, value=0, key="heart_age")
            sex = st.selectbox("Sex", ["Male", "Female"], key="heart_sex")
            cp = st.selectbox("Chest Pain Type", 
                            ["Typical angina", "Atypical angina", "Non-anginal pain", "Asymptomatic"], 
                            key="heart_cp")
            trestbps = st.number_input("Resting BP (mmHg)", min_value=0, max_value=300, value=0, key="heart_bp")
            chol = st.number_input("Cholesterol (mg/dL)", min_value=0, max_value=600, value=0, key="heart_chol")
        
        with col2:
            fbs = st.selectbox("Fasting BS >120 mg/dL", ["Yes", "No"], key="heart_fbs")
            restecg = st.selectbox("Resting ECG", 
                                 ["Normal", "ST-T wave abnormality", "Probable LVH"], 
                                 key="heart_ecg")
            thalach = st.number_input("Max Heart Rate", min_value=0, max_value=250, value=0, key="heart_thalach")
            exang = st.selectbox("Exercise Induced Angina", ["Yes", "No"], key="heart_exang")
            oldpeak = st.number_input("ST Depression", min_value=0.0, max_value=10.0, value=0.0, step=0.1, key="heart_oldpeak")
        
        slope = st.selectbox("Slope of ST Segment", 
                           ["Upsloping", "Flat", "Downsloping"], 
                           key="heart_slope")
        ca = st.selectbox("Major Vessels Colored", options=[0, 1, 2, 3], key="heart_ca")
        thal = st.selectbox("Thalassemia", 
                          ["Normal", "Fixed Defect", "Reversible Defect"], 
                          key="heart_thal")

        if st.form_submit_button("Predict Heart Disease Risk", type="primary"):
            inputs = {
                "Age": age,
                "Resting BP": trestbps,
                "Cholesterol": chol,
                "Max Heart Rate": thalach,
                "ST Depression": oldpeak
            }
            
            error_msg, invalid_fields = validate_inputs(inputs)
            
            if error_msg:
                st.error(error_msg)
                for field in invalid_fields:
                    st.markdown(
                        f"""<script>
                        document.querySelector('[aria-label="{field}"]').parentElement.parentElement.classList.add("invalid-field");
                        </script>""",
                        unsafe_allow_html=True
                    )
            else:
                try:
                    # Convert categorical inputs to numerical values
                    sex_num = 1 if sex == "Male" else 0
                    cp_num = ["Typical angina", "Atypical angina", "Non-anginal pain", "Asymptomatic"].index(cp)
                    fbs_num = 1 if fbs == "Yes" else 0
                    restecg_num = ["Normal", "ST-T wave abnormality", "Probable LVH"].index(restecg)
                    exang_num = 1 if exang == "Yes" else 0
                    slope_num = ["Upsloping", "Flat", "Downsloping"].index(slope)
                    thal_num = ["Normal", "Fixed Defect", "Reversible Defect"].index(thal)
                    
                    prediction = model.predict([[
                        age, sex_num, cp_num, trestbps, chol, fbs_num,
                        restecg_num, thalach, exang_num, oldpeak,
                        slope_num, ca, thal_num
                    ]])
                    
                    st.divider()
                    
                    if prediction[0] == 1:
                        st.error("### High Risk of Heart Disease Detected")
                        
                        with st.expander("Cardiac Risk Analysis", expanded=True):
                            st.write("#### Critical Health Markers")
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.metric("Blood Pressure", f"{trestbps} mmHg",
                                         delta="High" if trestbps >= 140 else "Normal",
                                         help="Normal: <120 mmHg")
                                st.metric("Cholesterol", f"{chol} mg/dL",
                                         delta="High" if chol >= 240 else "Normal",
                                         help="Normal: <200 mg/dL")
                            
                            with col2:
                                st.metric("ST Depression", f"{oldpeak:.1f}",
                                         delta="Abnormal" if oldpeak > 1 else "Normal",
                                         help="Normal: 0-1 mm")
                                st.metric("Max Heart Rate", f"{thalach} bpm",
                                         delta="Low" if thalach < (220 - age) * 0.85 else "Normal")
                            
                            st.warning("""
                            **Urgent Recommendations:**
                            - Consult a cardiologist immediately
                            - Request ECG and stress test
                            - Begin heart-healthy diet immediately
                            - Monitor blood pressure daily
                            """)
                    else:
                        st.success("### Low Risk of Heart Disease")
                        
                        with st.expander("Cardiac Health Summary", expanded=True):
                            st.write("#### Current Cardiovascular Metrics")
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.metric("Blood Pressure", f"{trestbps} mmHg")
                                st.metric("Cholesterol", f"{chol} mg/dL")
                            
                            with col2:
                                st.metric("ST Depression", f"{oldpeak:.1f}")
                                st.metric("Max Heart Rate", f"{thalach} bpm")
                            
                            st.info("""
                            **Preventive Care Tips:**
                            - Annual cardiac checkup if over 40
                            - Mediterranean diet recommended
                            - 150 mins moderate exercise weekly
                            - Manage stress and sleep well
                            """)
                
                except Exception as e:
                    st.error(f"Prediction error: {str(e)}")