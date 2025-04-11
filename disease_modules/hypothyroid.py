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
        
        with col2:
            tsh = st.number_input("TSH (mIU/L)", min_value=0.0, max_value=100.0, value=0.0, step=0.1, key="thyroid_tsh")
            t3_measured = st.selectbox("T3 Measured", ["Yes", "No"], key="thyroid_t3_measured")
            t3 = st.number_input("T3 (pg/mL)", min_value=0.0, max_value=20.0, value=0.0, step=0.1, key="thyroid_t3")
        
        tt4 = st.number_input("TT4 (ng/dL)", min_value=0.0, max_value=500.0, value=0.0, step=0.1, key="thyroid_tt4")

        if st.form_submit_button("Predict Thyroid Risk"):
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
                st.error("All thyroid function fields must be filled")
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
                        tt4
                    ]]
                    
                    prediction = model.predict(input_data)
                    
                    if prediction[0] == 1:
                        st.error("### High probability of hypothyroidism")
                        st.warning("""
                        ⚠️ **Recommendations:**
                        - Consult an endocrinologist immediately
                        - TSH > 4.0 mIU/L indicates hypothyroidism
                        - May require thyroid hormone replacement
                        """)
                    else:
                        st.success("### Normal thyroid function likely")
                    
                    st.info("""
                    **Thyroid Health Ranges:**
                    - Normal TSH: 0.4-4.0 mIU/L
                    - Normal Free T4: 0.8-1.8 ng/dL
                    - Normal Free T3: 2.3-4.2 pg/mL
                    
                    **Wellness Tips:**
                    - Ensure adequate iodine intake
                    - Manage stress levels
                    - Regular thyroid function tests
                    """)
                    
                except Exception as e:
                    st.error(f"Prediction failed: {str(e)}")