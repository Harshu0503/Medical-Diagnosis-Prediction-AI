import streamlit as st
import numpy as np

def validate_inputs(inputs):
    """Validate that no required fields are zero/empty"""
    invalid_fields = [name for name, value in inputs.items() if value == 0]
    if invalid_fields:
        return ("All highlighted fields are required and cannot be zero", invalid_fields)
    return (None, [])

def show_diabetes_page(model):
    st.title("Diabetes Prediction")

    if model is None:
        st.error("Diabetes prediction model failed to load")
        return

    # Gender Selection - Live interaction enabled
    gender = st.selectbox("Gender *", ["Select Gender", "Female", "Male"], index=0, key="diab_gender")

    with st.form("diabetes_form"):
        st.write("#### Patient Health Metrics")

        col1, col2 = st.columns(2)

        with col1:
            # Show Pregnancies only if gender is Female
            if gender == "Female":
                pregnancies = st.number_input("Pregnancies (optional)", min_value=0, max_value=20, value=0,
                                              help="Number of times pregnant", key="diab_preg")
            else:
                pregnancies = 0  # Hidden if not female

            glucose = st.number_input("Glucose (mg/dL) *", min_value=0, max_value=500, value=0,
                                      help="Plasma glucose concentration", key="diab_glucose")
            blood_pressure = st.number_input("Blood Pressure (mmHg) *", min_value=0, max_value=200, value=0,
                                             help="Diastolic blood pressure", key="diab_bp")
            skin_thickness = st.number_input("Skin Thickness (mm) *", min_value=0, max_value=100, value=0,
                                             help="Triceps skin fold thickness", key="diab_skin")

        with col2:
            insulin = st.number_input("Insulin (μU/mL) *", min_value=0, max_value=1000, value=0,
                                      help="2-Hour serum insulin", key="diab_insulin")
            bmi = st.number_input("BMI (kg/m²) *", min_value=0.0, max_value=70.0, value=0.0, step=0.1,
                                  help="Body mass index", key="diab_bmi")
            diabetes_pedigree = st.number_input("Diabetes Pedigree *", min_value=0.0, max_value=3.0, value=0.0, step=0.01,
                                                help="Diabetes family history likelihood", key="diab_pedigree")
            age = st.number_input("Age (years) *", min_value=0, max_value=120, value=0, key="diab_age")

        if st.form_submit_button("Predict Diabetes Risk", type="primary"):
            # Required fields only (exclude pregnancies)
            inputs = {
                "Glucose": glucose,
                "Blood Pressure": blood_pressure,
                "Skin Thickness": skin_thickness,
                "Insulin": insulin,
                "BMI": bmi,
                "Diabetes Pedigree": diabetes_pedigree,
                "Age": age
            }

            error_msg, invalid_fields = validate_inputs(inputs)

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
                    model_input = [[
                        pregnancies, glucose, blood_pressure, skin_thickness,
                        insulin, bmi, diabetes_pedigree, age
                    ]]
                    prediction = model.predict(model_input)

                    st.divider()

                    if prediction[0] == 1:
                        st.error("### High Risk of Diabetes Detected")
                        # Add the alert to consult a doctor
                        st.warning("""
                        ⚠️ **Urgent Medical Attention Required**  
                        Based on your test results, you are at high risk for diabetes.  
                        Please consult a doctor immediately for proper diagnosis and treatment.
                        """)

                        with st.expander("Diagnostic Details", expanded=True):
                            st.write("#### Key Risk Factors")
                            col1, col2 = st.columns(2)

                            with col1:
                                st.metric("Glucose Level", f"{glucose} mg/dL",
                                          delta="High" if glucose > 126 else "Normal",
                                          help="Normal range: 70-99 mg/dL")
                                st.metric("Blood Pressure", f"{blood_pressure} mmHg",
                                          delta="High" if blood_pressure > 120 else "Normal")

                            with col2:
                                st.metric("BMI", f"{bmi:.1f}",
                                          delta="High" if bmi > 25 else "Normal",
                                          help="Normal range: 18.5-24.9")
                                st.metric("Age Risk", f"{age} years",
                                          delta="Higher risk" if age > 45 else "Lower risk")

                            st.warning("""**Immediate Recommendations:**
- Consult an endocrinologist within 1 week
- Get HbA1c test for confirmation
- Begin monitoring fasting glucose daily
""")
                    else:
                        st.success("### Low Risk of Diabetes")

                        with st.expander("Health Summary", expanded=True):
                            st.write("#### Current Health Metrics")
                            col1, col2 = st.columns(2)

                            with col1:
                                st.metric("Glucose Level", f"{glucose} mg/dL", help="Normal range: 70-99 mg/dL")
                                st.metric("Blood Pressure", f"{blood_pressure} mmHg")

                            with col2:
                                st.metric("BMI", f"{bmi:.1f}")
                                st.metric("Age", f"{age} years")

                            st.info("""**Preventive Measures:**
- Annual glucose check if over 40
- Maintain BMI under 25
- 150 mins exercise/week
- Limit processed sugars
""")
                except Exception as e:
                    st.error(f"Prediction error: {str(e)}")
