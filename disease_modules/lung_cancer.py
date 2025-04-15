import streamlit as st

def show_lung_cancer_page(model):
    st.title("Lung Cancer Risk Prediction")
    
    if model is None:
        st.error("Lung cancer model failed to load")
        return
    
    with st.form("lung_cancer_form"):
        st.write("#### Patient Information")
        
        col1, col2 = st.columns(2)
        with col1:
            gender = st.selectbox("Gender", ["Male", "Female"], key="lung_gender")
            age = st.number_input("Age (years)", min_value=0, max_value=120, value=0, key="lung_age")
            smoking = st.selectbox("Smoking Status", ["Yes", "No"], key="lung_smoking")
            smoking_pack_years = st.number_input("Pack Years (if smoker)", min_value=0, max_value=200, value=0, key="lung_pack_years") if smoking == "Yes" else 0
            yellow_fingers = st.selectbox("Yellow Fingers/Nails", ["Yes", "No"], key="lung_yellow")
            anxiety = st.selectbox("Chronic Anxiety", ["Yes", "No"], key="lung_anxiety")
        
        with col2:
            peer_pressure = st.selectbox("History of Peer Pressure to Smoke", ["Yes", "No"], key="lung_peer")
            chronic_disease = st.selectbox("Chronic Lung Disease", ["Yes", "No"], key="lung_chronic")
            fatigue = st.selectbox("Persistent Fatigue", ["Yes", "No"], key="lung_fatigue")
            allergy = st.selectbox("Chronic Allergy", ["Yes", "No"], key="lung_allergy")
            wheezing = st.selectbox("Wheezing", ["Yes", "No"], key="lung_wheezing")
        
        alcohol = st.selectbox("Regular Alcohol Consumption", ["Yes", "No"], key="lung_alcohol")
        coughing = st.selectbox("Persistent Cough (3+ weeks)", ["Yes", "No"], key="lung_cough")
        breath = st.selectbox("Shortness of Breath", ["Yes", "No"], key="lung_breath")
        swallowing = st.selectbox("Difficulty Swallowing", ["Yes", "No"], key="lung_swallow")
        chest_pain = st.selectbox("Chest Pain", ["Yes", "No"], key="lung_pain")
        family_history = st.selectbox("Family History of Lung Cancer", ["Yes", "No"], key="lung_family")

        if st.form_submit_button("Predict Lung Cancer Risk", type="primary"):
            if age == 0:
                st.error("Age is required")
                st.markdown(
                    """<script>
                    document.querySelector('[aria-label="Age (years)"]').parentElement.parentElement.classList.add("invalid-field");
                    </script>""",
                    unsafe_allow_html=True
                )
            else:
                try:
                    # Prepare input data
                    input_data = [[
                        1 if gender == "Male" else 0,
                        age,
                        1 if smoking == "Yes" else 0,
                        smoking_pack_years if smoking == "Yes" else 0,
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
                        1 if family_history == "Yes" else 0
                    ]]
                    
                    prediction = model.predict(input_data)
                    st.divider()
                    
                    if prediction[0] == 1:
                        st.error("### High Risk of Lung Cancer Detected")
                        
                        # Urgent consultation alert
                        st.markdown("""
                        <div style="background-color: #fff4f4; border-left: 4px solid #ff5252; padding: 1rem; margin: 1rem 0;">
                            <h4 style="color: #ff5252; margin-top: 0;">⚠️ Immediate Pulmonologist Consultation Recommended</h4>
                            <p>Your risk factors indicate <strong>potential lung cancer risk requiring urgent evaluation</strong>.</p>
                            <p>Please schedule an appointment with a pulmonologist for:</p>
                            <ul>
                                <li>Low-dose CT scan (for high-risk individuals)</li>
                                <li>Bronchoscopy if indicated</li>
                                <li>Complete pulmonary function tests</li>
                            </ul>
                            <p><strong>Emergency Symptoms:</strong> Coughing blood, severe chest pain, or sudden breathing difficulty require immediate ER visit.</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        with st.expander("Detailed Risk Analysis", expanded=True):
                            st.write("#### Key Risk Factors Identified")
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                if smoking == "Yes":
                                    st.metric("Smoking Status", "Current Smoker", 
                                             delta=f"{smoking_pack_years} pack-years" if smoking_pack_years > 0 else "Unknown pack-years",
                                             help="1 pack-year = 1 pack/day for 1 year")
                                st.metric("Chronic Symptoms", 
                                         f"{sum([coughing=='Yes', breath=='Yes', chest_pain=='Yes'])}/3 present",
                                         delta="High" if sum([coughing=='Yes', breath=='Yes', chest_pain=='Yes']) >= 2 else "Moderate")
                            
                            with col2:
                                st.metric("Age Risk", f"{age} years",
                                         delta="High" if age > 55 else "Moderate",
                                         help="Risk increases significantly after 55")
                                st.metric("Family History", 
                                         "Present" if family_history == "Yes" else "None",
                                         delta="High" if family_history == "Yes" else "Low")
                            
                            st.warning("""
                            **Critical Next Steps:**
                            - Schedule pulmonologist appointment within 2 weeks
                            - Request low-dose CT scan referral
                            - Immediate smoking cessation program if applicable
                            - Document symptom progression (frequency, severity)
                            """)
                    else:
                        st.success("### Low Risk of Lung Cancer")
                        
                        with st.expander("Preventive Health Summary", expanded=True):
                            st.write("#### Current Risk Profile")
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.metric("Primary Risk Factors", 
                                         f"{sum([smoking=='Yes', chronic_disease=='Yes', family_history=='Yes'])} present")
                                st.metric("Respiratory Symptoms", 
                                         f"{sum([coughing=='Yes', breath=='Yes', wheezing=='Yes'])} present")
                            
                            with col2:
                                st.metric("Prevention Status", 
                                         "Needs Improvement" if smoking == "Yes" else "Good",
                                         delta="Quit Smoking" if smoking == "Yes" else None)
                                st.metric("Screening Recommended", 
                                         "Annual CT after 55" if age >= 55 and (smoking == "Yes" or family_history == "Yes") 
                                         else "Not currently")
                            
                            st.info("""
                            **Prevention Recommendations:**
                            - Annual screening if >55 with 30+ pack-year history
                            - Radon testing for home (2nd leading cause)
                            - Use N95 masks in polluted environments
                            - Regular cardio exercise for lung health
                            - Antioxidant-rich diet (berries, leafy greens)
                            """)
                    
                    # General lung health information
                    st.markdown("""
                    <div style="background-color: #f0f7ff; border-left: 4px solid #4dabf7; padding: 1rem; margin: 1rem 0;">
                        <h4 style="color: #1971c2; margin-top: 0;">ℹ️ Lung Cancer Early Detection</h4>
                        <p><strong>Screening Eligibility:</strong> Adults 50-80 with 20+ pack-year history who currently smoke or quit within past 15 years.</p>
                        <p><strong>Warning Signs:</strong> Persistent cough, chest pain, hoarseness, unexplained weight loss, coughing blood.</p>
                        <p><strong>Risk Reduction:</strong> Smoking cessation reduces risk by 50% after 10 years of quitting.</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                except Exception as e:
                    st.error(f"Prediction error: {str(e)}")
