import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# Set page config
st.set_page_config(
    page_title="Physical & Analytical Chemistry Virtual Lab",
    page_icon=":test_tube:",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        max-width: 1200px;
    }
    .experiment-section {
        padding: 20px;
        background-color: #f8f9fa;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .sidebar .sidebar-content {
        background-color: #f0f2f6;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
    }
    .stDownloadButton>button {
        background-color: #2196F3;
        color: white;
    }
    h2 {
        color: #2c3e50;
        border-bottom: 2px solid #2c3e50;
        padding-bottom: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("Navigation")
experiment = st.sidebar.radio(
    "Select Experiment",
    ("Home", "Phenol-Water System", "Conductometric Titration")
)

# Home page
if experiment == "Home":
    st.title("Physical & Analytical Chemistry Virtual Lab")
    st.image("https://images.unsplash.com/photo-1532187863486-abf9dbad1b69", width=700)
    
    st.markdown("""
    ## Welcome to the Virtual Lab!
    
    This interactive platform allows you to perform virtual experiments from your Physical and Analytical Chemistry lab manual.
    
    ### Available Experiments:
    1. **Determination of Critical Solution Temperature for Phenol-Water System**
    2. **Conductometric Titration of Acid Mixture**
    
    ### How to use:
    - Select an experiment from the sidebar
    - Follow the instructions for each experiment
    - Enter your observations or upload data
    - View and analyze results
    - Download your lab report
    
    ### Learning Objectives:
    - Understand the principles behind each experiment
    - Analyze experimental data
    - Interpret results and draw conclusions
    """)

# Phenol-Water System Experiment
elif experiment == "Phenol-Water System":
    st.title("Determination of Critical Solution Temperature for Phenol-Water System")
    
    with st.expander("Experiment Theory"):
        st.markdown("""
        ### Principle
        Phenol and water are partially miscible at ordinary temperatures. On shaking these two liquids, two saturated solutions of different compositions are obtained - one of phenol in water and another of water in phenol. 
        
        The mutual solubility increases with temperature until at a certain temperature (critical solution temperature), the two conjugate solutions become one homogeneous solution.
        
        ### Key Concepts
        - Partially miscible liquids
        - Critical solution temperature (CST)
        - Conjugate solutions
        - Lever rule for phase diagrams
        """)
    
    with st.expander("Procedure"):
        st.markdown("""
        1. Take a clean dry boiling tube and fit it with a thermometer and stirrer
        2. Add 5 ml of phenol using a burette
        3. Add 3.0 ml of distilled water and mix well
        4. Heat the mixture in a water bath with constant stirring
        5. Note the temperature when turbidity disappears (clear solution)
        6. Cool the mixture and note the temperature when turbidity reappears
        7. Repeat with additional water increments (2 ml each) up to 36 ml total
        8. Calculate volume percentages and plot temperature vs composition
        """)
    
    # Data input section
    st.header("Data Entry")
    st.markdown("Enter your experimental observations below:")
    
    num_observations = st.slider("Number of observations", 5, 16, 10)
    
    # Initialize dataframe
    if 'phenol_data' not in st.session_state:
        st.session_state.phenol_data = pd.DataFrame(columns=[
            "Volume of phenol (ml)", "Volume of water (ml)", 
            "Temp of disappearance (°C)", "Temp of appearance (°C)"
        ])
    
    # Data entry form
    with st.form("phenol_data_form"):
        cols = st.columns(4)
        headers = ["Volume of phenol (ml)", "Volume of water (ml)", 
                  "Temp of disappearance (°C)", "Temp of appearance (°C)"]
        
        for i in range(num_observations):
            st.subheader(f"Observation {i+1}")
            row = {}
            for j, col in enumerate(cols):
                if j == 0:  # Volume of phenol
                    row[headers[j]] = col.number_input(
                        f"{headers[j]} - Obs {i+1}", 
                        value=5.0, key=f"phenol_{i}_{j}"
                    )
                elif j == 1:  # Volume of water
                    row[headers[j]] = col.number_input(
                        f"{headers[j]} - Obs {i+1}", 
                        value=3.0 + 2*i, key=f"water_{i}_{j}"
                    )
                else:  # Temperatures
                    row[headers[j]] = col.number_input(
                        f"{headers[j]} - Obs {i+1}", 
                        value=60.0 + i*2, key=f"temp_{i}_{j}"
                    )
            
            # Add to dataframe
            st.session_state.phenol_data = pd.concat([
                st.session_state.phenol_data, 
                pd.DataFrame([row])
            ], ignore_index=True)
        
        submitted = st.form_submit_button("Save Data")
        if submitted:
            st.success("Data saved successfully!")
    
    # Data display and calculations
    if not st.session_state.phenol_data.empty:
        st.subheader("Recorded Data")
        df = st.session_state.phenol_data.copy()
        
        # Calculate additional columns
        df["Volume % of phenol"] = (df["Volume of phenol (ml)"] / 
                                   (df["Volume of phenol (ml)"] + df["Volume of water (ml)"]) * 100)
        df["Mean Temp (°C)"] = (df["Temp of disappearance (°C)"] + 
                               df["Temp of appearance (°C)"]) / 2
        
        st.dataframe(df.style.format("{:.2f}"))
        
        # Plotting
        st.subheader("Phase Diagram")
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(df["Volume % of phenol"], df["Mean Temp (°C)"], 'bo-')
        ax.set_xlabel("Volume % of phenol")
        ax.set_ylabel("Temperature (°C)")
        ax.set_title("Critical Solution Temperature for Phenol-Water System")
        ax.grid(True)
        
        # Find and mark CST (highest point)
        max_idx = df["Mean Temp (°C)"].idxmax()
        cst_temp = df.loc[max_idx, "Mean Temp (°C)"]
        cst_conc = df.loc[max_idx, "Volume % of phenol"]
        
        ax.plot(cst_conc, cst_temp, 'ro', markersize=10, 
                label=f'CST: {cst_temp:.1f}°C at {cst_conc:.1f}% phenol')
        ax.legend()
        
        st.pyplot(fig)
        
        # Results
        st.subheader("Results")
        st.markdown(f"""
        - **Critical Solution Temperature (CST):** {cst_temp:.1f} °C
        - **Critical Solution Composition:** {cst_conc:.1f} % phenol by volume
        """)
        
        # Download data
        st.download_button(
            label="Download Data as CSV",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name='phenol_water_data.csv',
            mime='text/csv'
        )
        
        # Download plot
        buf = BytesIO()
        fig.savefig(buf, format="png")
        st.download_button(
            label="Download Plot as PNG",
            data=buf,
            file_name="phenol_water_phase_diagram.png",
            mime="image/png"
        )

# Conductometric Titration Experiment
elif experiment == "Conductometric Titration":
    st.title("Conductometric Titration of Acid Mixture")
    
    with st.expander("Experiment Theory"):
        st.markdown("""
        ### Principle
        Conductometric titration measures the conductance of a solution during titration. 
        
        When a strong acid (HCl) is titrated with strong base (NaOH):
        - Fast-moving H⁺ ions are replaced by slower Na⁺ ions → conductance decreases
        - After equivalence point, excess OH⁻ ions increase conductance
        
        For weak acid (CH₃COOH) with strong base:
        - Few H⁺ ions are replaced by Na⁺
        - CH₃COO⁻ ions increase conductance
        - After equivalence point, excess OH⁻ sharply increases conductance
        
        ### Key Concepts
        - Equivalent conductance
        - Conductivity changes during titration
        - Strong vs weak acid titration curves
        - Endpoint determination
        """)
    
    with st.expander("Procedure"):
        st.markdown("""
        1. Prepare standard oxalic acid solution (0.1N)
        2. Standardize NaOH solution using oxalic acid
        3. Dilute the acid mixture sample to 100 ml
        4. Take 10 ml sample in beaker, add 10 ml water
        5. Measure initial conductance
        6. Add 0.2 ml NaOH, stir, measure conductance
        7. Repeat until 8 ml NaOH added
        8. Plot conductance vs volume NaOH
        9. Determine endpoints for HCl and CH₃COOH
        """)
    
    # Data input section
    st.header("Data Entry")
    
    # Standardization of NaOH
    st.subheader("Standardization of NaOH")
    oxalic_acid_vol = st.number_input("Volume of oxalic acid used (ml)", 25.0)
    naoh_vol = st.number_input("Volume of NaOH consumed (ml)", 18.5)
    oxalic_normality = st.number_input("Normality of oxalic acid", 0.1)
    
    # Calculate NaOH normality
    naoh_normality = (oxalic_acid_vol * oxalic_normality) / naoh_vol if naoh_vol else 0
    
    st.markdown(f"**Calculated NaOH Normality:** {naoh_normality:.4f} N")
    
    # Titration data
    st.subheader("Titration Data")
    
    if 'cond_data' not in st.session_state:
        st.session_state.cond_data = pd.DataFrame(columns=[
            "Volume of NaOH (ml)", "Conductance (mS)"
        ])
    
    # Data entry form
    with st.form("cond_data_form"):
        num_points = st.slider("Number of data points", 10, 40, 20)
        
        cols = st.columns(2)
        for i in range(num_points):
            vol = cols[0].number_input(
                f"Volume NaOH (ml) - Point {i+1}", 
                value=0.2*i, key=f"vol_{i}"
            )
            cond = cols[1].number_input(
                f"Conductance (mS) - Point {i+1}", 
                value=0.8 - 0.02*i if i < 10 else 0.6 + 0.03*(i-10), 
                key=f"cond_{i}"
            )
            
            # Add to dataframe
            st.session_state.cond_data = pd.concat([
                st.session_state.cond_data, 
                pd.DataFrame([[vol, cond]], columns=["Volume of NaOH (ml)", "Conductance (mS)"])
            ], ignore_index=True)
        
        submitted = st.form_submit_button("Save Data")
        if submitted:
            st.success("Data saved successfully!")
    
    # Data analysis
    if not st.session_state.cond_data.empty:
        st.subheader("Recorded Data")
        df = st.session_state.cond_data.sort_values("Volume of NaOH (ml)")
        st.dataframe(df.style.format("{:.2f}"))
        
        # Plotting
        st.subheader("Conductometric Titration Curve")
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(df["Volume of NaOH (ml)"], df["Conductance (mS)"], 'bo-')
        ax.set_xlabel("Volume of NaOH (ml)")
        ax.set_ylabel("Conductance (mS)")
        ax.set_title("Conductometric Titration of Acid Mixture")
        ax.grid(True)
        
        # Find endpoints (simplified approach)
        # First derivative to find inflection points
        df['diff'] = df["Conductance (mS)"].diff() / df["Volume of NaOH (ml)"].diff()
        
        # First endpoint (HCl)
        try:
            hcl_end = df.iloc[df['diff'].idxmin()]["Volume of NaOH (ml)"]
            ax.axvline(hcl_end, color='r', linestyle='--', 
                      label=f'HCl endpoint: {hcl_end:.2f} ml')
        except:
            hcl_end = 0
        
        # Second endpoint (CH₃COOH)
        try:
            ch3cooh_end = df.iloc[df['diff'].idxmax()]["Volume of NaOH (ml)"]
            ax.axvline(ch3cooh_end, color='g', linestyle='--', 
                      label=f'CH₃COOH endpoint: {ch3cooh_end:.2f} ml')
        except:
            ch3cooh_end = 0
        
        ax.legend()
        st.pyplot(fig)
        
        # Calculations
        st.subheader("Calculations")
        
        sample_vol = st.number_input("Volume of sample used (ml)", 10.0)
        
        if hcl_end > 0 and ch3cooh_end > 0:
            hcl_normality = (hcl_end * naoh_normality) / sample_vol
            ch3cooh_vol = ch3cooh_end - hcl_end
            ch3cooh_normality = (ch3cooh_vol * naoh_normality) / sample_vol
            
            hcl_amount = hcl_normality * 36.5 * 100 / 1000  # g in 100 ml
            ch3cooh_amount = ch3cooh_normality * 60 * 100 / 1000  # g in 100 ml
            
            st.markdown(f"""
            ### Results:
            - **Volume of NaOH for HCl:** {hcl_end:.2f} ml
            - **Volume of NaOH for CH₃COOH:** {ch3cooh_vol:.2f} ml
            - **Normality of HCl:** {hcl_normality:.4f} N
            - **Normality of CH₃COOH:** {ch3cooh_normality:.4f} N
            - **Amount of HCl in mixture:** {hcl_amount:.4f} g
            - **Amount of CH₃COOH in mixture:** {ch3cooh_amount:.4f} g
            """)
        
        # Download options
        st.download_button(
            label="Download Data as CSV",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name='conductometric_data.csv',
            mime='text/csv'
        )
        
        buf = BytesIO()
        fig.savefig(buf, format="png")
        st.download_button(
            label="Download Plot as PNG",
            data=buf,
            file_name="conductometric_titration_curve.png",
            mime="image/png"
        )

# Footer
st.markdown("---")
st.markdown("""
**Physical & Analytical Chemistry Virtual Lab**  
Department of Chemical Engineering  
SRM Institute of Science and Technology  
© 2023 All Rights Reserved
""")
