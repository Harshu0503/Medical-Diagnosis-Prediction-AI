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
                'Spread2': spread2, 'PPE': ppe
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
                    st.divider()
                    
                    if prediction[0] == 1:
                        st.error("### High Probability of Parkinson's Disease Detected")
                        
                        # Neurologist consultation alert
                        st.markdown("""
                        <div style="background-color: #fff4f4; border-left: 4px solid #ff5252; padding: 1rem; margin: 1rem 0;">
                            <h4 style="color: #ff5252; margin-top: 0;">⚠️ Neurology Specialist Consultation Recommended</h4>
                            <p>Your voice analysis results indicate <strong>potential Parkinson's disease markers requiring expert evaluation</strong>.</p>
                            <p>Please schedule an appointment with a movement disorder specialist for:</p>
                            <ul>
                                <li>Comprehensive neurological examination</li>
                                <li>UPDRS (Unified Parkinson's Disease Rating Scale) assessment</li>
                                <li>Possible DATscan or other diagnostic imaging</li>
                            </ul>
                            <p><strong>Early Intervention Benefits:</strong> Early diagnosis allows for more effective symptom management and treatment planning.</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        with st.expander("Detailed Voice Analysis", expanded=True):
                            st.write("#### Key Abnormal Voice Parameters")
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.metric("Jitter (%)", f"{jitter_percent*100:.4f}%",
                                         delta="Abnormal" if jitter_percent > 0.0006 else "Normal",
                                         help="Normal <0.04%")
                                st.metric("Shimmer (dB)", f"{shimmer_db:.2f} dB",
                                         delta="Abnormal" if shimmer_db > 0.15 else "Normal",
                                         help="Normal <0.15 dB")
                                st.metric("Fundamental Frequency Variation", 
                                         f"{(fhi-flo)/fo*100:.1f}%",
                                         delta="High" if (fhi-flo)/fo > 0.2 else "Normal")
                            
                            with col2:
                                st.metric("Harmonics-to-Noise Ratio", f"{hnr:.1f}",
                                         delta="Low" if hnr < 20 else "Normal",
                                         help="Normal >20")
                                st.metric("Noise-to-Harmonics Ratio", f"{nhr:.4f}",
                                         delta="High" if nhr > 0.1 else "Normal",
                                         help="Normal <0.1")
                                st.metric("Pitch Period Entropy", f"{ppe:.4f}",
                                         delta="High" if ppe > 0.15 else "Normal")
                            
                            st.warning("""
                            **Next Steps:**
                            - Schedule movement disorder specialist appointment within 4 weeks
                            - Document symptom progression (tremor, stiffness, balance)
                            - Begin voice therapy exercises
                            - Consider physical therapy evaluation
                            """)
                    else:
                        st.success("### Low Probability of Parkinson's Disease")
                        
                        with st.expander("Voice Health Summary", expanded=True):
                            st.write("#### Current Voice Parameters")
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.metric("Jitter", f"{jitter_percent*100:.4f}%")
                                st.metric("Shimmer", f"{shimmer_db:.2f} dB")
                                st.metric("Fundamental Frequency", f"{fo:.1f} Hz")
                            
                            with col2:
                                st.metric("HNR", f"{hnr:.1f}")
                                st.metric("NHR", f"{nhr:.4f}")
                                st.metric("Pitch Stability", 
                                         "Good" if ppe < 0.1 else "Moderate")
                            
                            st.info("""
                            **Preventive Recommendations:**
                            - Annual voice screening if over 60 or with risk factors
                            - Vocal exercises to maintain speech clarity
                            - Regular physical activity to support motor function
                            - Monitor for early symptoms (micrographia, reduced arm swing)
                            - Antioxidant-rich diet (berries, nuts, leafy greens)
                            """)
                    
                    # Educational content
                    st.markdown("""
                    <div style="background-color: #f0f7ff; border-left: 4px solid #4dabf7; padding: 1rem; margin: 1rem 0;">
                        <h4 style="color: #1971c2; margin-top: 0;">ℹ️ Understanding Parkinson's Voice Changes</h4>
                        <p><strong>Hypokinetic Dysarthria:</strong> Characteristic speech pattern in Parkinson's including reduced loudness, monotone pitch, and imprecise articulation.</p>
                        <p><strong>Early Warning Signs:</strong> Soft speech (hypophonia), rapid speech (tachyphemia), vocal tremor, and reduced stress patterns.</p>
                        <p><strong>Voice Therapy:</strong> Lee Silverman Voice Treatment (LSVT LOUD) is the most effective evidence-based therapy.</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                except Exception as e:
                    st.error(f"Prediction error: {str(e)}")
