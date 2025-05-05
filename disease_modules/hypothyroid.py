import streamlit as st
import numpy as np

def show_thyroid_page(model):
    st.title("🧠 Hypothyroid Risk Prediction")
    st.write("Provide your health parameters below to assess the risk of hypothyroidism.")

    if model is None:
        st.error("Thyroid model failed to load. Please check the model path or compatibility.")
        return

    with st.form("thyroid_form"):
        col1, col2 = st.columns(2)

        with col1:
            age = st.number_input("Age (years)", min_value=0, max_value=120, value=0)
            sex = st.selectbox("Sex", ["Male", "Female"])
            on_thyroxine = st.selectbox("Are you on Thyroxine medication?", ["Yes", "No"])
            tsh = st.number_input("TSH (mIU/L)", min_value=0.0, max_value=100.0, value=0.0, step=0.1)

        with col2:
            t3_measured = st.selectbox("Was T3 measured?", ["Yes", "No"])
            t3 = st.number_input("T3 (pg/mL)", min_value=0.0, max_value=20.0, value=0.0, step=0.1)
            tt4 = st.number_input("TT4 (ng/dL)", min_value=0.0, max_value=500.0, value=0.0, step=0.1)
            pregnant = st.selectbox("Pregnant (if female)", ["Yes", "No", "N/A"]) if sex == "Female" else "N/A"

        submitted = st.form_submit_button("🔍 Predict Thyroid Risk")

    if submitted:
        invalid_fields = []
        if age == 0:
            invalid_fields.append("Age")
        if tsh == 0:
            invalid_fields.append("TSH")
        if t3_measured == "Yes" and t3 == 0:
            invalid_fields.append("T3")
        if tt4 == 0:
            invalid_fields.append("TT4")

        if invalid_fields:
            st.error("Please fill in the required fields: " + ", ".join(invalid_fields))
            return

        try:
            # Input encoding
            input_data = [[
                age,
                1 if sex == "Male" else 0,
                1 if on_thyroxine == "Yes" else 0,
                tsh,
                1 if t3_measured == "Yes" else 0,
                t3 if t3_measured == "Yes" else 0,
                tt4,
                1 if pregnant == "Yes" else 0
            ]]

            input_data = np.array(input_data).reshape(1, -1)
            prediction = model.predict(input_data)

            st.divider()
            if prediction[0] == 1:
                st.error("### ❗ High Risk of Hypothyroidism Detected")

                st.markdown("""
                <div style="background-color: #fff4f4; border-left: 5px solid #ff6b6b; padding: 1rem;">
                    <strong>⚠️ Immediate endocrinology consultation recommended.</strong><br>
                    Your thyroid levels may indicate hypothyroidism. Please seek medical advice for:
                    <ul>
                        <li>Full thyroid panel (TSH, Free T4, T3, antibodies)</li>
                        <li>Medication evaluation (thyroxine or others)</li>
                        <li>Lifestyle and diet considerations</li>
                    </ul>
                    <strong>Seek urgent care if you feel:</strong>
                    <ul>
                        <li>Severe fatigue</li>
                        <li>Constant cold sensation</li>
                        <li>Sudden weight gain</li>
                        <li>Hair thinning or depression</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

                with st.expander("🔬 Marker Analysis"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("TSH", f"{tsh:.1f} mIU/L", "High" if tsh > 4.0 else "Normal")
                        st.metric("TT4", f"{tt4:.1f} ng/dL", "Low" if tt4 < 5.0 else "Normal")
                    with col2:
                        if t3_measured == "Yes":
                            st.metric("T3", f"{t3:.1f} pg/mL", "Low" if t3 < 2.3 else "Normal")
                        st.metric("Risk Factors", 
                                  "High" if age > 50 or (sex == "Female" and pregnant == "Yes") else "Moderate")

                st.warning("""
                **Suggested Actions:**
                - Book appointment within 2 weeks
                - Request Free T4 and antibody testing
                - Monitor symptoms and avoid self-medication
                - Avoid goitrogens if iodine deficient
                """)

            else:
                st.success("### ✅ Normal Thyroid Function Likely")

                with st.expander("📊 Health Summary"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("TSH", f"{tsh:.1f} mIU/L")
                        st.metric("TT4", f"{tt4:.1f} ng/dL")
                    with col2:
                        if t3_measured == "Yes":
                            st.metric("T3", f"{t3:.1f} pg/mL")
                        st.metric("Risk Factors", "Low" if age < 50 else "Moderate")

                st.info("""
                **Health Tips:**
                - Annual TSH test if over 35 or at risk
                - Maintain iodine-rich diet
                - Manage stress and exercise regularly
                - Stay alert for signs of thyroid dysfunction
                """)

            st.markdown("""
            ---
            #### ℹ️ Understanding Thyroid Markers
            - **TSH**: Stimulates thyroid hormone production. High TSH = likely underactive thyroid.
            - **T3/T4**: Main hormones. Low levels = hypothyroidism.
            - **Antibodies**: Can indicate autoimmune thyroid disease (Hashimoto’s).
            """)

        except Exception as e:
            st.error(f"Prediction failed: {e}")
