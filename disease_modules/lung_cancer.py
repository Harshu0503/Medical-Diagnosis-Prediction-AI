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
            smoking = st.selectbox("Smoking", ["Yes", "No"], key="lung_smoking")
            yellow_fingers = st.selectbox("Yellow Fingers", ["Yes", "No"], key="lung_yellow")
            anxiety = st.selectbox("Anxiety", ["Yes", "No"], key="lung_anxiety")
        
        with col2:
            peer_pressure = st.selectbox("Peer Pressure", ["Yes", "No"], key="lung_peer")
            chronic_disease = st.selectbox("Chronic Disease", ["Yes", "No"], key="lung_chronic")
            fatigue = st.selectbox("Fatigue", ["Yes", "No"], key="lung_fatigue")
            allergy = st.selectbox("Allergy", ["Yes", "No"], key="lung_allergy")
            wheezing = st.selectbox("Wheezing", ["Yes", "No"], key="lung_wheezing")
        
        alcohol = st.selectbox("Alcohol Consumption", ["Yes", "No"], key="lung_alcohol")
        coughing = st.selectbox("Coughing", ["Yes", "No"], key="lung_cough")
        breath = st.selectbox("Shortness of Breath", ["Yes", "No"], key="lung_breath")
        swallowing = st.selectbox("Swallowing Difficulty", ["Yes", "No"], key="lung_swallow")
        chest_pain = st.selectbox("Chest Pain", ["Yes", "No"], key="lung_pain")

        if st.form_submit_button("Predict Lung Cancer Risk"):
            if age == 0:
                st.error("Age cannot be zero")
                st.markdown(
                    """<script>
                    document.querySelector('[aria-label="Age (years)"]').parentElement.parentElement.classList.add("invalid-field");
                    </script>""",
                    unsafe_allow_html=True
                )
            else:
                try:
                    # Convert all inputs to binary (1=Yes, 0=No)
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
                        1 if chest_pain == "Yes" else 0
                    ]]
                    
                    prediction = model.predict(input_data)
                    
                    if prediction[0] == 1:
                        st.error("### High risk of lung cancer detected")
                        st.warning("""
                        ⚠️ **Critical Recommendations:**
                        - Immediate smoking cessation if applicable
                        - Consult a pulmonologist for CT scan
                        - Monitor for persistent symptoms
                        """)
                    else:
                        st.success("### Low risk of lung cancer")
                    
                    st.info("""
                    **Risk Reduction Tips:**
                    - Avoid tobacco and secondhand smoke
                    - Test your home for radon
                    - Use protective gear if exposed to carcinogens
                    - Regular exercise improves lung function
                    """)
                    
                except Exception as e:
                    st.error(f"Prediction failed: {str(e)}")