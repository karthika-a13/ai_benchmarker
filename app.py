# app.py
import streamlit as st
import pandas as pd
from benchmarker import benchmark_max_model

# Page Configuration
st.set_page_config(
    page_title="Oil & Gas AI Benchmark Hub",
    page_icon="⚡",
    layout="wide"
)

# ULTRA MODERN ENTERPRISE DASHBOARD STYLING
st.markdown("""
<style>
    /* Top Banner Styling */
    .banner {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    }
    .banner-title {
        font-size: 1.25rem;
        font-weight: 800;
        color: #38BDF8;
        letter-spacing: -0.3px;
        margin: 0;
    }
    .banner-sub {
        font-size: 0.78rem;
        color: #94A3B8;
        margin-top: 4px;
        margin-bottom: 0;
    }

    /* Custom Metric Cards */
    .card-box {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 12px 16px;
        text-align: center;
    }
    .card-label {
        font-size: 0.7rem;
        color: #94A3B8;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .card-val {
        font-size: 1.05rem;
        font-weight: 700;
        color: #38BDF8;
        margin-top: 4px;
    }
</style>
""", unsafe_allow_html=True)

# Main Banner Header
st.markdown("""
<div class="banner">
    <div class="banner-title">⚡ OIL & GAS EDGE AI BENCHMARKING PLATFORM</div>
    <div class="banner-sub">Real-Time Telemetry Parsing & Performance Evaluation for Off-Grid Rig Infrastructure</div>
</div>
""", unsafe_allow_html=True)

@st.cache_data
def load_and_process_csv():
    df = pd.read_csv("industrial_dataset.csv")
    
    faults = df[df['Target'] == 'Fault'].drop_duplicates(subset=['Error_Message']).head(5)
    normals = df[df['Target'] == 'Normal'].drop_duplicates(subset=['Error_Message']).head(2)
    combined = pd.concat([faults, normals]).reset_index(drop=True)
    
    prompts_list = []
    for idx, row in combined.iterrows():
        prompt_text = (
            f"Industrial Rig Machine #{row['Machine_ID']} logged error '{row['Error_Message']}' "
            f"with Telemetry Data [Temp: {row['Temperature_C']}°C, Pressure: {row['Pressure_bar']} bar, "
            f"Vibration: {row['Vibration_Level']}, Sound: {row['Sound_dB']} dB]. "
            f"Operator notes: '{row['Operator_Notes']}'. Status: {row['Target']}. "
            f"Analyze root cause and provide emergency protocol steps."
        )
        prompts_list.append({
            "incident_id": f"INC-2026-{idx+1:02d}",
            "scenario_name": f"Machine #{row['Machine_ID']} - {row['Error_Message']} ({row['Target']})",
            "prompt_text": prompt_text,
            "category": "Fault Emergency" if row['Target'] == 'Fault' else "Standard Maintenance",
            "severity_level": "Critical" if row['Target'] == 'Fault' else "Medium"
        })
        
    prompts_list.append({
        "incident_id": "INC-2026-99",
        "scenario_name": "Custom / New Fault Entry",
        "prompt_text": "",
        "category": "Manual Entry",
        "severity_level": "Dynamic"
    })
    
    return pd.DataFrame(prompts_list)

df_prompts = load_and_process_csv()

# Sidebar Configuration
with st.sidebar:
    st.markdown("### ⚙️ Benchmark Setup")
    max_tokens = st.slider("Max Token Limit", min_value=32, max_value=512, value=128, step=32)
    base_url = st.text_input("MAX Engine Endpoint", "http://localhost:8000/v1")
    
    st.divider()
    st.markdown("### 🛠️ Architecture Stack")
    st.caption("**Inference Engine:** MAX Engine")
    st.caption("**Kernel Optimization:** Mojo SIMD")
    st.caption("**Dataset Source:** `industrial_dataset.csv`")
    st.caption(f"**Parsed Scenarios:** {len(df_prompts)-1} Records")

# Split Screen Interactive Layout
col_left, col_right = st.columns([1, 1], gap="medium")

with col_left:
    st.markdown("##### 1. Incident Ingestion")
    scenarios = df_prompts["scenario_name"].tolist()
    selected_scenario = st.selectbox("Select Incident Log:", scenarios)

    selected_row = df_prompts[df_prompts["scenario_name"] == selected_scenario].iloc[0]

    if selected_scenario == "Custom / New Fault Entry":
        prompt = st.text_area("Custom Log Prompt:", placeholder="Paste raw logs here...", height=120)
    else:
        m1, m2, m3 = st.columns(3)
        m1.markdown(f'<div class="card-box"><div class="card-label">Incident ID</div><div class="card-val">{selected_row["incident_id"]}</div></div>', unsafe_allow_html=True)
        m2.markdown(f'<div class="card-box"><div class="card-label">Category</div><div class="card-val">{selected_row["category"]}</div></div>', unsafe_allow_html=True)
        m3.markdown(f'<div class="card-box"><div class="card-label">Severity</div><div class="card-val">{selected_row["severity_level"]}</div></div>', unsafe_allow_html=True)
        
        st.write("")
        prompt = st.text_area("Dynamically Extracted Prompt:", value=selected_row["prompt_text"], height=95)

with col_right:
    st.markdown("##### 2. Benchmark Execution")
    models_to_test = st.multiselect(
        "Target Edge Models:",
        ["meta-llama/Llama-3.1-8B-Instruct", "Qwen/Qwen2.5-7B-Instruct", "Mistral-7B-Instruct-v0.3"],
        default=["meta-llama/Llama-3.1-8B-Instruct", "Qwen/Qwen2.5-7B-Instruct", "Mistral-7B-Instruct-v0.3"]
    )
    
    st.write("")
    st.write("")
    run_btn = st.button("🚀 Run Multi-Model Inference Benchmark", type="primary", use_container_width=True)

if run_btn:
    if not prompt.strip():
        st.error("Please enter or select a valid fault prompt before benchmarking.")
    elif not models_to_test:
        st.warning("Please select at least one model.")
    else:
        results = []
        with st.spinner("Benchmarking Inference Performance via MAX Engine & Mojo SIMD Metrics..."):
            for model in models_to_test:
                res = benchmark_max_model(model, prompt, max_tokens, base_url)
                results.append(res)
                
        df_res = pd.DataFrame(results)
        
        st.divider()
        st.markdown("##### 📊 Real-Time Benchmark Analytics")
        
        # Highlight Metric Cards
        fastest_model = df_res.loc[df_res['Throughput (Tokens/sec)'].idxmax()]['Model'].split('/')[-1]
        lowest_latency = df_res.loc[df_res['Latency (sec)'].idxmin()]['Model'].split('/')[-1]
        
        h1, h2, h3 = st.columns(3)
        h1.markdown(f'<div class="card-box"><div class="card-label">⚡ Highest Speed</div><div class="card-val">{fastest_model}</div></div>', unsafe_allow_html=True)
        h2.markdown(f'<div class="card-box"><div class="card-label">⏱️ Lowest Latency</div><div class="card-val">{lowest_latency}</div></div>', unsafe_allow_html=True)
        h3.markdown(f'<div class="card-box"><div class="card-label">📐 Workload Limit</div><div class="card-val">{max_tokens} Tokens</div></div>', unsafe_allow_html=True)
        
        st.write("")
        st.dataframe(df_res, use_container_width=True)
        
        t1, t2 = st.tabs(["⚡ Throughput (Tokens/sec)", "⏱️ Latency (Seconds)"])
        with t1:
            st.bar_chart(df_res.set_index("Model")["Throughput (Tokens/sec)"], color="#38BDF8")
        with t2:
            st.bar_chart(df_res.set_index("Model")["Latency (sec)"], color="#EF4444")