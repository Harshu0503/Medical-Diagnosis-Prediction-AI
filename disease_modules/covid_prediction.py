import streamlit as st
import numpy as np

def validate_covid_inputs(inputs):
    """Validate that required fields meet criteria"""
    invalid_fields = []
    if inputs["Fever"] < 95 or inputs["Fever"] > 107:
        invalid_fields.append("Fever")
    if inputs["Age"] <= 0:
        invalid_fields.append("Age")
    for name, value in inputs.items():
        if value == "Select" and name != "Emergency Check":
            invalid_fields.append(name)
    
    if invalid_fields:
        return (f"Invalid values in: {', '.join(invalid_fields)}", invalid_fields)
    return (None, [])

def show_covid_page(model):
    st.title("COVID-19 Risk Prediction")
    
    if model is None:
        st.error("COVID-19 prediction model failed to load")
        return

    # Emergency warning banner
    st.markdown("""
    <style>
    .emergency {
        background-color: #ffcccc;
        border-left: 5px solid #ff0000;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

    with st.form("covid_form"):
        st.write("#### Patient Symptoms")

        col1, col2 = st.columns(2)
        
        with col1:
            fever = st.number_input("Fever (°F) *", min_value=95.0, max_value=110.0, value=98.6, step=0.1, key="covid_fever")
            dry_cough = st.selectbox("Dry Cough *", ["Select", "No", "Yes"], index=0, key="covid_cough")
            sore_throat = st.selectbox("Sore Throat *", ["Select", "No", "Yes"], index=0, key="covid_throat")

        with col2:
            tiredness = st.selectbox("Tiredness *", ["Select", "No", "Yes"], index=0, key="covid_tired")
            breathing = st.selectbox("Difficulty Breathing *", ["Select", "No", "Yes"], index=0, key="covid_breath")
            age = st.number_input("Age (years) *", min_value=0, max_value=120, value=25, key="covid_age")

        if st.form_submit_button("Predict COVID Risk", type="primary"):
            inputs = {
                "Fever": fever,
                "Dry Cough": dry_cough,
                "Sore Throat": sore_throat,
                "Tiredness": tiredness,
                "Difficulty Breathing": breathing,
                "Age": age
            }

            # Emergency check before prediction
            if fever >= 103.0 and breathing == "Yes":
                st.markdown("""
                <div class="emergency">
                    <h3>🚨 EMERGENCY WARNING</h3>
                    <p>High fever with breathing difficulty requires <strong>immediate medical attention</strong>.</p>
                    <ul>
                        <li>Seek emergency care now</li>
                        <li>Monitor oxygen saturation</li>
                        <li>Do not wait for test results</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
                st.stop()

            error_msg, invalid_fields = validate_covid_inputs(inputs)
            
            if error_msg:
                st.error(error_msg)
                for field in invalid_fields:
                    st.markdown(
                        f"""<script>
                        document.querySelector('label:has(+ *[aria-label="{field}"])').style.color = "red";
                        </script>""",
                        unsafe_allow_html=True
                    )
            else:
                try:
                    # Prepare input data
                    input_data = [[
                        fever,
                        1 if dry_cough == "Yes" else 0,
                        1 if sore_throat == "Yes" else 0,
                        1 if tiredness == "Yes" else 0,
                        1 if breathing == "Yes" else 0,
                        age
                    ]]
                    
                    prediction = model.predict(input_data)
                    st.divider()
                    
                    if prediction[0] == 1 or (fever > 100.5 and age > 50 and breathing == "Yes"):
                        st.error("### High Risk of Severe COVID-19")
                        
                        with st.expander("Risk Analysis", expanded=True):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.metric("Fever", f"{fever}°F", 
                                          delta="Dangerous" if fever >= 103 else "High",
                                          help="Normal: 97-99°F")
                                st.metric("Respiratory", breathing, 
                                          delta="Emergency" if breathing == "Yes" else "Stable")
                                
                            with col2:
                                st.metric("Age Risk", f"{age} years",
                                          delta="High" if age > 50 else "Moderate")
                                st.metric("Symptom Burden", 
                                          f"{sum([dry_cough=='Yes', tiredness=='Yes', sore_throat=='Yes'])}/3",
                                          delta="Severe" if breathing == "Yes" else "Moderate")

                        st.warning("""
                        **Immediate Actions:**
                        - Seek testing and medical evaluation within 24 hours
                        - Isolate from others immediately
                        - Monitor oxygen levels if available
                        - Emergency care if breathing worsens
                        """)

                    else:
                        st.success("### Low Risk of COVID-19")
                        
                        with st.expander("Health Summary", expanded=True):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.metric("Fever", f"{fever}°F")
                                st.metric("Key Symptom", 
                                          "Present" if dry_cough == "Yes" else "Absent")
                                
                            with col2:
                                st.metric("Age Factor", f"{age} years")
                                st.metric("Breathing Status", breathing)

                        st.info("""
                        **Preventive Measures:**
                        - Monitor for new symptoms
                        - Isolate if exposed
                        - Consider testing if symptomatic
                        - Follow local health guidelines
                        """)

                except Exception as e:
                    st.error(f"Prediction error: {str(e)}")

if __name__ == "__main__":
    # For testing
    class MockModel:
        def predict(self, X):
            # Simulate model prediction
            fever = X[0][0]
            breathing = X[0][4]
            age = X[0][5]
            return [1 if (fever > 100 and breathing == 1 and age > 45) else 0]
    
    show_covid_page(MockModel())
