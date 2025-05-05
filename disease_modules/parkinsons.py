import streamlit as st
import numpy as np

def show_parkinsons_page(model):
    st.title("Parkinson's Disease Prediction")
    
    if model is None:
        st.error("Parkinson's model failed to load")
        return
    
    with st.form("parkinsons_form"):
        st.write("#### Voice and Speech Measurement Parameters")
        
        col1, col2 = st.columns(2)
        with col1:
            fo = st.number_input('Average Vocal Fundamental Frequency (Hz)', min_value=0.0, max_value=300.0, value=0.0, step=0.1, key="park_fo",
                               help="Normal range: 85-180Hz for men, 165-255Hz for women")
            fhi = st.number_input('Maximum Vocal Fundamental Frequency (Hz)', min_value=0.0, max_value=300.0, value=0.0, step=0.1, key="park_fhi")
            flo = st.number_input('Minimum Vocal Fundamental Frequency (Hz)', min_value=0.0, max_value=300.0, value=0.0, step=0.1, key="park_flo")
            jitter_percent = st.number_input('Jitter (%)', min_value=0.0, max_value=1.0, value=0.0, step=0.0001, key="park_jitter_percent",
                                           help="Normal <0.04%, Parkinson's typically >0.06%")
            jitter_abs = st.number_input('Jitter Absolute (ms)', min_value=0.0, max_value=0.1, value=0.0, step=0.00001, key="park_jitter_abs")
        
        with col2:
            rap = st.number_input('Relative Amplitude Perturbation', min_value=0.0, max_value=0.1, value=0.0, step=0.0001, key="park_rap")
            ppq = st.number_input('5-point Period Perturbation Quotient', min_value=0.0, max_value=0.1, value=0.0, step=0.0001, key="park_ppq")
            ddp = st.number_input('Jitter DDP (3*RAP)', min_value=0.0, max_value=0.5, value=0.0, step=0.001, key="park_ddp")
            shimmer = st.number_input('Shimmer (amplitude variation)', min_value=0.0, max_value=1.0, value=0.0, step=0.001, key="park_shimmer")
            shimmer_db = st.number_input('Shimmer in dB', min_value=0.0, max_value=1.0, value=0.0, step=0.01, key="park_shimmer_db",
                                       help="Normal <0.15dB, Parkinson's typically >0.2dB")
        
        # Additional parameters
        st.write("#### Advanced Voice Parameters")
        col3, col4 = st.columns(2)
        with col3:
            apq3 = st.number_input('Shimmer APQ3', min_value=0.0, max_value=1.0, value=0.0, step=0.001, key="park_apq3")
            apq5 = st.number_input('Shimmer APQ5', min_value=0.0, max_value=1.0, value=0.0, step=0.001, key="park_apq5")
            apq = st.number_input('Amplitude Perturbation Quotient', min_value=0.0, max_value=1.0, value=0.0, step=0.001, key="park_apq")
            dda = st.number_input('Shimmer DDA (3*APQ3)', min_value=0.0, max_value=1.0, value=0.0, step=0.001, key="park_dda")
            nhr = st.number_input('Noise-to-Harmonics Ratio', min_value=0.0, max_value=1.0, value=0.0, step=0.0001, key="park_nhr",
                                help="Higher values indicate more voice disorder")
        
        with col4:
            hnr = st.number_input('Harmonics-to-Noise Ratio', min_value=0.0, max_value=40.0, value=0.0, step=0.1, key="park_hnr",
                                 help="Normal >20, Parkinson's typically <15")
            rpde = st.number_input('Recurrence Period Density Entropy', min_value=0.0, max_value=1.0, value=0.0, step=0.0001, key="park_rpde")
            dfa = st.number_input('Detrended Fluctuation Analysis', min_value=0.0, max_value=1.0, value=0.0, step=0.0001, key="park_dfa")
            spread1 = st.number_input('Spread1 (nonlinear measure)', min_value=-10.0, max_value=0.0, value=0.0, step=0.0001, key="park_spread1")
            spread2 = st.number_input('Spread2 (nonlinear measure)', min_value=0.0, max_value=1.0, value=0.0, step=0.0001, key="park_spread2")
        
        # 🔹 Add D2 input here
        d2 = st.number_input('D2 (nonlinear dynamic measure)', min_value=0.0, max_value=5.0, value=0.0, step=0.001, key="park_d2")
        
        ppe = st.number_input('Pitch Period Entropy', min_value=0.0, max_value=1.0, value=0.0, step=0.0001, key="park_ppe")

        if st.form_submit_button("Predict Parkinson's Risk", type="primary"):
            inputs = {
                'Average Vocal Frequency': fo, 'Max Frequency': fhi, 'Min Frequency': flo,
                'Jitter%': jitter_percent, 'Jitter Absolute': jitter_abs,
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
            else:
                try:
                    input_data = np.array([[
                        fo, fhi, flo, jitter_percent, jitter_abs, rap, ppq, ddp,
                        shimmer, shimmer_db, apq3, apq5, apq, dda, nhr, hnr,
                        rpde, dfa, spread1, spread2, d2, ppe
                    ]])
                    
                    prediction = model.predict(input_data)
                    st.divider()
                    
                    if prediction[0] == 1:
                        st.error("### High Probability of Parkinson's Disease Detected")
                    else:
                        st.success("### Low Probability of Parkinson's Disease")
                
                except Exception as e:
                    st.error(f"Prediction error: {str(e)}")
