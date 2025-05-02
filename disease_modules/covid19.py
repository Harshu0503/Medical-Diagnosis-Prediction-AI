import streamlit as st
import numpy as np

def validate_inputs(inputs):
    invalid_fields = [name for name, value in inputs.items() if value == 0]
    if invalid_fields:
        return ("All highlighted fields are required and cannot be zero", invalid_fields)
    return (None, [])

def show_covid_page(model):
    st.title("COVID-19 Risk Prediction")

    if model is None:
        st.error("COVID-19 prediction model failed to load")
        return

    with st.form("covid_form"):
        st.write("#### Patient Symptoms")

        col1, col2 = st.columns(2)

        with col1:
            fever = st.number_input("Fever (in °F) *", min_value=95.0, max_value=110.0, value=0.0)
            dry_cough = st.selectbox("Dry Cough *", ["Select", "No", "Yes"], index=0)
            sore_throat = st.selectbox("Sore Throat *", ["Select", "No", "Yes"], index=0)

        with col2:
            tiredness = st.selectbox("Tiredness *", ["Select", "No", "Yes"], index=0)
            breathing = st.selectbox("Difficulty Breathing *", ["Select", "No", "Yes"], index=0)
            age = st.number_input("Age (years) *", min_value=0, max_value=120, value=0)

        if st.form_submit_button("Predict COVID Risk", type="primary"):
            symptom_inputs = {
                "Fever": fever,
                "Dry Cough": 0 if dry_cough == "Select" else (1 if dry_cough == "Yes" else 0),
                "Sore Throat": 0 if sore_throat == "Select" else (1 if sore_throat == "Yes" else 0),
                "Tiredness": 0 if tiredness == "Select" else (1 if tiredness == "Yes" else 0),
                "Difficulty Breathing": 0 if breathing == "Select" else (1 if breathing == "Yes" else 0),
                "Age": age
            }

            error_msg, invalid_fields = validate_inputs(symptom_inputs)

            if error_msg:
                st.error(error_msg)
                for field in invalid_fields:
                    st.markdown(
                        f"""<script>
                        Array.from(document.querySelectorAll('label')).forEach(label => {{
                          if (label.innerText.includes("{field}")) {{
                             label.style.color = "red";
                             label.parentElement.style.border = "1px solid red";
                          }}
                        }});
                        </script>""",
                        unsafe_allow_html=True
                    )
            else:
                symptom_values = list(symptom_inputs.values())
                prediction = model.predict([symptom_values])

                st.divider()

                if prediction[0] == 1:
                    st.error("### High Risk of COVID-19 Detected")
                    st.warning("""
                    ⚠️ **Urgent Medical Attention Required**  
                    Based on your symptoms, you might be at high risk.  
                    Please seek medical advice immediately.
                    """)
                else:
                    st.success("### Low Risk of COVID-19")
                    st.info("""
                    **Stay Safe!**  
                    Continue following safety protocols and monitor for any worsening symptoms.
                    """)
