import streamlit as st

def show_thyroid_page(model):
    st.title("Hypothyroid Risk Prediction")
    
    if model is None:
        st.error("Thyroid model failed to load")
        return
    
    with st.form("thyroid_form"):
        st.write("#### Thyroid Function Parameters")
        
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age (years)", min_value=0, max_value=120, value=0, key="thyroid_age")
            sex = st.selectbox("Sex", ["Male", "Female"], key="thyroid_sex")
            on_thyroxine = st.selectbox("On Thyroxine Medication", ["Yes", "No"], key="thyroid_med")
            tsh = st.number_input("TSH (mIU/L)", min_value=0.0, max_value=100.0, value=0.0, step=0.1, key="thyroid_tsh")
        
        with col2:
            t3_measured = st.selectbox("T3 Measured", ["Yes", "No"], key="thyroid_t3_measured")
            t3 = st.number_input("T3 (pg/mL)", min_value=0.0, max_value=20.0, value=0.0, step=0.1, key="thyroid_t3")
            tt4 = st.number_input("TT4 (ng/dL)", min_value=0.0, max_value=500.0, value=0.0, step=0.1, key="thyroid_tt4")
            pregnant = st.selectbox("Pregnant (if female)", ["Yes", "No", "N/A"], key="thyroid_pregnant") if sex == "Female" else "N/A"

        if st.form_submit_button("Predict Thyroid Risk", type="primary"):
            invalid_fields = []
            if age == 0:
                invalid_fields.append("Age (years)")
            if tsh == 0:
                invalid_fields.append("TSH (mIU/L)")
            if t3_measured == "Yes" and t3 == 0:
                invalid_fields.append("T3 (pg/mL)")
            if tt4 == 0:
                invalid_fields.append("TT4 (ng/dL)")
            
            if invalid_fields:
                st.error("All highlighted fields must be filled")
                for field in invalid_fields:
                    st.markdown(
                        f"""<script>
                        document.querySelector('[aria-label="{field}"]').parentElement.parentElement.classList.add("invalid-field");
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
                        t3 if t3_measured == "Yes" else 0,  # Use 0 if not measured
                        tt4,
                        1 if pregnant == "Yes" else 0 if pregnant == "No" else 0
                    ]]
                    
                    prediction = model.predict(input_data)
                    st.divider()
                    
                    if prediction[0] == 1:
                        st.error("### High Probability of Hypothyroidism Detected")
                        
                        # Doctor consultation alert
                        st.markdown("""
                        <div style="background-color: #fff4f4; border-left: 4px solid #ff5252; padding: 1rem; margin: 1rem 0;">
                            <h4 style="color: #ff5252; margin-top: 0;">⚠️ Endocrinology Consultation Recommended</h4>
                            <p>Your thyroid function results indicate <strong>potential hypothyroidism requiring medical evaluation</strong>.</p>
                            <p>Please schedule an appointment with an endocrinologist for:</p>
                            <ul>
                                <li>Comprehensive thyroid panel (TSH, Free T4, Free T3, antibodies)</li>
                                <li>Evaluation of thyroid medication needs</li>
                                <li>Assessment of potential underlying causes</li>
                            </ul>
                            <p><strong>Urgent Attention Needed If:</strong> Experiencing severe fatigue, unexplained weight gain, depression, or feeling cold constantly.</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        with st.expander("Thyroid Risk Analysis", expanded=True):
                            st.write("#### Critical Thyroid Markers")
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.metric("TSH Level", f"{tsh:.1f} mIU/L",
                                         delta="High" if tsh > 4.0 else "Normal",
                                         help="Normal range: 0.4-4.0 mIU/L")
                                st.metric("T4 Level", f"{tt4:.1f} ng/dL",
                                         delta="Low" if tt4 < 0.8 else "Normal",
                                         help="Normal range: 0.8-1.8 ng/dL")
                            
                            with col2:
                                if t3_measured == "Yes":
                                    st.metric("T3 Level", f"{t3:.1f} pg/mL",
                                             delta="Low" if t3 < 2.3 else "Normal",
                                             help="Normal range: 2.3-4.2 pg/mL")
                                st.metric("Risk Factors", 
                                         "High" if age > 50 or (sex == "Female" and pregnant == "Yes") else "Moderate",
                                         help="Age, gender, pregnancy status")
                            
                            st.warning("""
                            **Immediate Actions:**
                            - Schedule endocrinology appointment within 2 weeks
                            - Request full thyroid antibody testing
                            - Monitor symptoms daily (energy, weight, temperature)
                            - Avoid goitrogenic foods if iodine deficient
                            """)
                    else:
                        st.success("### Normal Thyroid Function Likely")
                        
                        with st.expander("Thyroid Health Summary", expanded=True):
                            st.write("#### Current Thyroid Metrics")
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.metric("TSH Level", f"{tsh:.1f} mIU/L")
                                st.metric("T4 Level", f"{tt4:.1f} ng/dL")
                            
                            with col2:
                                if t3_measured == "Yes":
                                    st.metric("T3 Level", f"{t3:.1f} pg/mL")
                                st.metric("Risk Factors", 
                                         "Low" if age < 50 else "Moderate")
                            
                            st.info("""
                            **Preventive Care Recommendations:**
                            - Annual TSH test if over 35 or with risk factors
                            - Ensure adequate iodine and selenium intake
                            - Manage stress through relaxation techniques
                            - Watch for symptoms of thyroid dysfunction
                            - Regular exercise and balanced diet
                            """)
                    
                    # General thyroid information
                    st.markdown("""
                    <div style="background-color: #f0f7ff; border-left: 4px solid #4dabf7; padding: 1rem; margin: 1rem 0;">
                        <h4 style="color: #1971c2; margin-top: 0;">ℹ️ Understanding Your Thyroid Results</h4>
                        <p><strong>TSH (Thyroid Stimulating Hormone):</strong> Primary screening test. High TSH suggests underactive thyroid.</p>
                        <p><strong>Free T4:</strong> Main thyroid hormone. Low levels confirm hypothyroidism.</p>
                        <p><strong>Free T3:</strong> Active hormone. Important for diagnosis when symptoms persist despite normal TSH/T4.</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                except Exception as e:
                    st.error(f"Prediction error: {str(e)}")
