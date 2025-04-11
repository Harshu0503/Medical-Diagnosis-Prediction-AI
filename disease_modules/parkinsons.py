import streamlit as st
import numpy as np

def show_parkinsons_page(model):
    st.title("Parkinson's Disease Prediction")
    
    if model is None:
        st.error("Parkinson's model failed to load")
        return
    
    with st.form("parkinsons_form"):
        st.write("#### Voice Measurement Parameters")
        
        col1, col2 = st.columns(2)
        with col1:
            fo = st.number_input('MDVP:Fo(Hz)', min_value=0.0, max_value=300.0, value=0.0, step=0.1, key="park_fo")
            fhi = st.number_input('MDVP:Fhi(Hz)', min_value=0.0, max_value=300.0, value=0.0, step=0.1, key="park_fhi")
            flo = st.number_input('MDVP:Flo(Hz)', min_value=0.0, max_value=300.0, value=0.0, step=0.1, key="park_flo")
            jitter_percent = st.number_input('MDVP:Jitter(%)', min_value=0.0, max_value=1.0, value=0.0, step=0.0001, key="park_jitter_percent")
            jitter_abs = st.number_input('MDVP:Jitter(Abs)', min_value=0.0, max_value=0.1, value=0.0, step=0.00001, key="park_jitter_abs")
        
        with col2:
            rap = st.number_input('MDVP:RAP', min_value=0.0, max_value=0.1, value=0.0, step=0.0001, key="park_rap")
            ppq = st.number_input('MDVP:PPQ', min_value=0.0, max_value=0.1, value=0.0, step=0.0001, key="park_ppq")
            ddp = st.number_input('Jitter:DDP', min_value=0.0, max_value=0.5, value=0.0, step=0.001, key="park_ddp")
            shimmer = st.number_input('MDVP:Shimmer', min_value=0.0, max_value=1.0, value=0.0, step=0.001, key="park_shimmer")
            shimmer_db = st.number_input('MDVP:Shimmer(dB)', min_value=0.0, max_value=1.0, value=0.0, step=0.01, key="park_shimmer_db")
        
        # Additional parameters
        apq3 = st.number_input('Shimmer:APQ3', min_value=0.0, max_value=1.0, value=0.0, step=0.001, key="park_apq3")
        apq5 = st.number_input('Shimmer:APQ5', min_value=0.0, max_value=1.0, value=0.0, step=0.001, key="park_apq5")
        apq = st.number_input('MDVP:APQ', min_value=0.0, max_value=1.0, value=0.0, step=0.001, key="park_apq")
        dda = st.number_input('Shimmer:DDA', min_value=0.0, max_value=1.0, value=0.0, step=0.001, key="park_dda")
        nhr = st.number_input('NHR', min_value=0.0, max_value=1.0, value=0.0, step=0.0001, key="park_nhr")
        hnr = st.number_input('HNR', min_value=0.0, max_value=40.0, value=0.0, step=0.1, key="park_hnr")
        rpde = st.number_input('RPDE', min_value=0.0, max_value=1.0, value=0.0, step=0.0001, key="park_rpde")
        dfa = st.number_input('DFA', min_value=0.0, max_value=1.0, value=0.0, step=0.0001, key="park_dfa")
        spread1 = st.number_input('Spread1', min_value=-10.0, max_value=0.0, value=0.0, step=0.0001, key="park_spread1")
        spread2 = st.number_input('Spread2', min_value=0.0, max_value=1.0, value=0.0, step=0.0001, key="park_spread2")
        d2 = st.number_input('D2', min_value=0.0, max_value=10.0, value=0.0, step=0.0001, key="park_d2")
        ppe = st.number_input('PPE', min_value=0.0, max_value=1.0, value=0.0, step=0.0001, key="park_ppe")

        if st.form_submit_button("Predict Parkinson's Risk"):
            inputs = {
                'Fo': fo, 'Fhi': fhi, 'Flo': flo,
                'Jitter%': jitter_percent, 'JitterAbs': jitter_abs,
                'RAP': rap, 'PPQ': ppq, 'DDP': ddp,
                'Shimmer': shimmer, 'Shimmer(dB)': shimmer_db,
                'APQ3': apq3, 'APQ5': apq5, 'APQ': apq,
                'DDA': dda, 'NHR': nhr, 'HNR': hnr,
                'RPDE': rpde, 'DFA': dfa, 'Spread1': spread1,
                'Spread2': spread2, 'D2': d2, 'PPE': ppe
            }
            
            invalid_fields = [name for name, value in inputs.items() if value == 0]
            if invalid_fields:
                st.error("All voice measurement fields must be filled")
                for field in invalid_fields:
                    st.markdown(
                        f"""<script>
                        document.querySelector('[aria-label="{field}"]').parentElement.parentElement.classList.add("invalid-field");
                        </script>""",
                        unsafe_allow_html=True
                    )
            else:
                try:
                    # Prepare input array in correct order
                    input_data = np.array([[
                        fo, fhi, flo, jitter_percent, jitter_abs, rap, ppq, ddp,
                        shimmer, shimmer_db, apq3, apq5, apq, dda, nhr, hnr,
                        rpde, dfa, spread1, spread2, d2, ppe
                    ]])
                    
                    prediction = model.predict(input_data)
                    
                    if prediction[0] == 1:
                        st.error("### High probability of Parkinson's disease detected")
                        st.warning("⚠️ Recommendation: Please consult a neurologist for further evaluation")
                    else:
                        st.success("### Low probability of Parkinson's disease")
                    
                    st.info("""
                    **Voice Analysis Insights:**
                    - Normal jitter range: <0.04%
                    - Normal shimmer range: <0.15 dB
                    - HNR below 20 may indicate voice abnormality
                    """)
                    
                except Exception as e:
                    st.error(f"Prediction failed: {str(e)}")