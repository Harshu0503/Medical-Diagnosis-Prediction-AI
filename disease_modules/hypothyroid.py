import streamlit as st
import numpy as np

def validate_thyroid_inputs(inputs):
    """Validate that required fields are filled"""
    invalid_fields = [name for name, value in inputs.items() if value == 0]
    if invalid_fields:
        return ("All highlighted fields are required and cannot be zero", invalid_fields)
    return (None, [])

def show_thyroid_page(model):
    st.title("Hypothyroid Risk Prediction")
    
    if model is None:
        st.error("Thyroid prediction model failed to load")
        return

    with st.form("thyroid_form"):
        st.write("#### Patient Health Metrics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.number_input("Age (years) *", min_value=0, max_value=120, value=0, key="thyroid_age")
            sex = st.selectbox("Sex *", ["Select Sex", "Male", "Female"], index=0, key="thyroid_sex")
            on_thyroxine = st.selectbox("On Thyroxine *", ["Select Option", "Yes", "No"], index=0, key="thyroid_thyroxine")
            tsh = st.number_input("TSH (mIU/L) *", min_value=0.0, max_value=100.0, value=0.0, step=0.1, key="thyroid_tsh")
        
        with col2:
            t3_measured = st.selectbox("T3 Measured *", ["Select Option", "Yes", "No"], index=0, key="thyroid_t3_measured")
            t3 = st.number_input("T3 (pg/mL)", min_value=0.0, max_value=20.0, value=0.0, step=0.1, 
                                disabled=(st.session_state.get("thyroid_t3_measured", "Select Option") != "Yes"),
                                key="thyroid_t3")
            tt4 = st.number_input("TT4 (ng/dL) *", min_value=0.0, max_value=500.0, value=0.0, step=0.1, key="thyroid_tt4")

        if st.form_submit_button("Predict Thyroid Risk", type="primary"):
            # Required fields
            inputs = {
                "Age": age,
                "Sex": sex,
                "On Thyroxine": on_thyroxine,
                "TSH": tsh,
                "T3 Measured": t3_measured,
                "TT4": tt4
            }
            
            # Additional validation for T3 if measured
            if t3_measured == "Yes" and t3 == 0:
                inputs["T3"] = 0  # Mark as invalid
            elif t3_measured == "Yes":
                inputs["T3"] = t3  # Valid if provided
                
            error_msg, invalid_fields = validate_thyroid_inputs(inputs)
            
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
                    # Prepare input data
                    input_data = [[
                        age,
                        1 if sex == "Male" else 0,
                        1 if on_thyroxine == "Yes" else 0,
                        tsh,
                        1 if t3_measured == "Yes" else 0,
                        t3 if t3_measured == "Yes" else 0,
                        tt4
                    ]]
                    
                    prediction = model.predict(input_data)
                    st.divider()
                    
                    if prediction[0] == 1:
                        st.error("### High Risk of Hypothyroidism Detected")
                        st.warning("""
                        ⚠️ **Medical Consultation Recommended**  
                        Your thyroid markers indicate potential hypothyroidism.  
                        Please consult an endocrinologist for proper evaluation.
                        """)

                        with st.expander("Diagnostic Details", expanded=True):
                            st.write("#### Thyroid Markers Analysis")
                            col1, col2 = st.columns(2)

                            with col1:
                                st.metric("TSH Level", f"{tsh:.1f} mIU/L",
                                          delta="High" if tsh > 4.0 else "Normal",
                                          help="Normal range: 0.4-4.0 mIU/L")
                                st.metric("TT4 Level", f"{tt4:.1f} ng/dL",
                                          delta="Low" if tt4 < 5.0 else "Normal",
                                          help="Normal range: 5.0-12.0 ng/dL")

                            with col2:
                                if t3_measured == "Yes":
                                    st.metric("T3 Level", f"{t3:.1f} pg/mL",
                                              delta="Low" if t3 < 2.3 else "Normal",
                                              help="Normal range: 2.3-4.2 pg/mL")
                                st.metric("Age Risk", f"{age} years",
                                          delta="Higher risk" if age > 50 else "Lower risk")

                            st.warning("""**Immediate Recommendations:**
- Schedule endocrinology appointment within 2 weeks
- Request full thyroid panel (TSH, Free T4, antibodies)
- Monitor symptoms (fatigue, weight changes, cold sensitivity)
- Avoid sudden dietary changes before testing
""")
                    else:
                        st.success("### Normal Thyroid Function Likely")

                        with st.expander("Health Summary", expanded=True):
                            st.write("#### Current Thyroid Status")
                            col1, col2 = st.columns(2)

                            with col1:
                                st.metric("TSH Level", f"{tsh:.1f} mIU/L", help="Normal range: 0.4-4.0 mIU/L")
                                st.metric("TT4 Level", f"{tt4:.1f} ng/dL", help="Normal range: 5.0-12.0 ng/dL")

                            with col2:
                                if t3_measured == "Yes":
                                    st.metric("T3 Level", f"{t3:.1f} pg/mL", help="Normal range: 2.3-4.2 pg/mL")
                                st.metric("Prevention Status", "Good", 
                                          delta="Monitor if >40" if age > 40 else None)

                            st.info("""**Preventive Measures:**
- Annual TSH test if over 35 or with family history
- Maintain adequate iodine intake
- Be aware of hypothyroidism symptoms
- Regular exercise and stress management
""")
                except Exception as e:
                    st.error(f"Prediction error: {str(e)}")
