import streamlit as st

def validate_lung_inputs(inputs):
    """Validate that age is provided and at least one symptom is present for high risk"""
    invalid_fields = []
    if inputs["Age"] == 0:
        invalid_fields.append("Age")
    
    if invalid_fields:
        return ("Highlighted fields are required", invalid_fields)
    return (None, [])

def show_lung_cancer_page(model):
    st.title("Lung Cancer Risk Prediction")

    if model is None:
        st.error("Lung cancer prediction model failed to load")
        return

    with st.form("lung_cancer_form"):
        st.write("#### Patient Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            gender = st.selectbox("Gender *", ["Select Gender", "Male", "Female"], index=0, key="lung_gender")
            age = st.number_input("Age (years) *", min_value=0, max_value=120, value=0, key="lung_age")
            smoking = st.selectbox("Smoking Status *", ["Select Option", "Yes", "No"], index=0, key="lung_smoking")
            yellow_fingers = st.selectbox("Yellow Fingers/Nails", ["Select Option", "Yes", "No"], index=0, key="lung_yellow")
            anxiety = st.selectbox("Chronic Anxiety", ["Select Option", "Yes", "No"], index=0, key="lung_anxiety")
            peer_pressure = st.selectbox("Peer Pressure to Smoke", ["Select Option", "Yes", "No"], index=0, key="lung_peer")
            chronic_disease = st.selectbox("Chronic Lung Disease *", ["Select Option", "Yes", "No"], index=0, key="lung_chronic")
        
        with col2:
            fatigue = st.selectbox("Persistent Fatigue", ["Select Option", "Yes", "No"], index=0, key="lung_fatigue")
            allergy = st.selectbox("Chronic Allergy", ["Select Option", "Yes", "No"], index=0, key="lung_allergy")
            wheezing = st.selectbox("Wheezing *", ["Select Option", "Yes", "No"], index=0, key="lung_wheezing")
            alcohol = st.selectbox("Regular Alcohol Use", ["Select Option", "Yes", "No"], index=0, key="lung_alcohol")
            coughing = st.selectbox("Persistent Cough *", ["Select Option", "Yes", "No"], index=0, key="lung_cough")
            breath = st.selectbox("Shortness of Breath *", ["Select Option", "Yes", "No"], index=0, key="lung_breath")
            swallowing = st.selectbox("Difficulty Swallowing", ["Select Option", "Yes", "No"], index=0, key="lung_swallow")
            chest_pain = st.selectbox("Chest Pain *", ["Select Option", "Yes", "No"], index=0, key="lung_pain")

        if st.form_submit_button("Predict Lung Cancer Risk", type="primary"):
            # Required fields
            inputs = {
                "Age": age,
                "Gender": gender,
                "Smoking Status": smoking,
                "Chronic Lung Disease": chronic_disease,
                "Wheezing": wheezing,
                "Persistent Cough": coughing,
                "Shortness of Breath": breath,
                "Chest Pain": chest_pain
            }
            
            error_msg, invalid_fields = validate_lung_inputs(inputs)
            
            if error_msg:
                st.error(error_msg)
                for field in invalid_fields:
                    st.markdown(
                        f"""<script>
                        const labels = Array.from(document.querySelectorAll('label'));
                        labels.forEach(label => {{
                            if (label.innerText.includes("{field}")) {{
                                label.style.color = "red";
                                label.parentElement.style.border = "1px solid red";
                            }}
                        }});
                        </script>""",
                        unsafe_allow_html=True
                    )
            else:
                try:
                    # Convert all inputs to binary (1=Yes, 0=No/Select Option)
                    input_data = [[
                        1 if gender == "Male" else 0,
                        age,
                        1 if smoking == "Yes" else 0,
                        1 if yellow_fingers == "Yes" else 0,
                        1 if anxiety == "Yes" else 0,
                        1 if peer_pressure == "Yes" else 0,
                        1 if chronic_disease == "Yes" else 0,
                        1 if fatigue == "Yes" else 0,
                        1 if allergy == "Yes" else 0,
                        1 if wheezing == "Yes" else 0,
                        1 if alcohol == "Yes" else 0,
                        1 if coughing == "Yes" else 0,
                        1 if breath == "Yes" else 0,
                        1 if swallowing == "Yes" else 0,
                        1 if chest_pain == "Yes" else 0,
                    ]]
                    
                    prediction = model.predict(input_data)
                    st.divider()
                    
                    if prediction[0] == 1:
                        st.error("### High Risk of Lung Cancer Detected")
                        st.warning("""
                        ⚠️ **Urgent Medical Attention Recommended**  
                        Based on your risk factors, you may be at high risk for lung cancer.  
                        Please consult a pulmonologist for further evaluation.
                        """)

                        with st.expander("Diagnostic Details", expanded=True):
                            st.write("#### Key Risk Factors")
                            col1, col2 = st.columns(2)

                            with col1:
                                st.metric("Smoking Status", smoking,
                                          delta="High Risk" if smoking == "Yes" else "Low Risk")
                                st.metric("Respiratory Symptoms", 
                                         f"{sum([coughing=='Yes', breath=='Yes', wheezing=='Yes'])}/3 present",
                                         delta="Severe" if sum([coughing=='Yes', breath=='Yes', wheezing=='Yes']) >= 2 else "Moderate")

                            with col2:
                                st.metric("Age Risk", f"{age} years",
                                          delta="High" if age > 55 else "Moderate")
                                st.metric("Chronic Conditions", 
                                         f"{sum([chronic_disease=='Yes', allergy=='Yes'])} present")

                            st.warning("""**Immediate Recommendations:**
- Schedule low-dose CT scan within 2 weeks
- Complete pulmonary function tests
- Smoking cessation program (if applicable)
- Environmental hazard assessment
""")
                    else:
                        st.success("### Low Risk of Lung Cancer")

                        with st.expander("Health Summary", expanded=True):
                            st.write("#### Current Risk Profile")
                            col1, col2 = st.columns(2)

                            with col1:
                                st.metric("Primary Risk", "Smoker" if smoking == "Yes" else "Non-smoker")
                                st.metric("Symptom Burden", 
                                         f"{sum([coughing=='Yes', breath=='Yes', chest_pain=='Yes'])} present")

                            with col2:
                                st.metric("Age Factor", f"{age} years",
                                          delta="Monitor" if age > 50 else "Low")
                                st.metric("Prevention Status", 
                                         "Needs Improvement" if smoking == "Yes" else "Good")

                            st.info("""**Preventive Measures:**
- Annual screening if >50 with smoking history
- Radon testing for home environment
- Regular cardio exercise for lung health
- Antioxidant-rich diet (berries, leafy greens)
- Avoid exposure to air pollutants
""")
                except Exception as e:
                    st.error(f"Prediction error: {str(e)}")
