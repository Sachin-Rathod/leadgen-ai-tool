import streamlit as st
import pandas as pd
import time
import altair as alt
from enrich import enrich_domain
from score import score_lead

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Caprae AI Leads",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── GLOBAL CSS & THEME ───────────────────────────────────────────────────────
st.markdown("""
<style>
:root {
    --primary: #1F2C56;
    --secondary: #12A150;
    --accent: #6E48AA;
    --light: #F4F6FA;
    --dark: #0A1026;
    --text: #333333;
    --text-light: #666666;
}

/* Base styling */
body, .stApp, .block-container {
    background-color: var(--light) !important;
    font-family: 'Inter', sans-serif;
    color: var(--text);
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Montserrat', sans-serif;
    color: var(--primary);
    font-weight: 600;
}

/* Main container padding */
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    padding-left: 3rem;
    padding-right: 3rem;
}

/* Fixed card styling with better alignment */
.card {
    background: white;
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 20px;
    box-shadow: 0 4px 24px rgba(31, 44, 86, 0.08);
    transition: transform 0.3s, box-shadow 0.3s;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-height: 280px;
}

.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 32px rgba(31, 44, 86, 0.12);
}

/* Metric card specific styling */
.metric-card {
    background: white;
    border-radius: 12px;
    padding: 24px 16px;
    margin-bottom: 20px;
    box-shadow: 0 4px 24px rgba(31, 44, 86, 0.08);
    transition: transform 0.3s, box-shadow 0.3s;
    height: 140px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
}

.metric-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 32px rgba(31, 44, 86, 0.12);
}

.metric-icon {
    font-size: 2.5rem;
    margin-bottom: 8px;
    line-height: 1;
}

.metric-value {
    font-size: 2rem;
    font-weight: 700;
    margin: 8px 0;
    line-height: 1;
}

.metric-label {
    font-size: 0.9rem;
    margin: 0;
    opacity: 0.7;
    line-height: 1;
}

/* Button styling */
.stButton>button, .stDownloadButton>button {
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 0.75rem 1.5rem !important;
    transition: background-color 0.2s, transform 0.2s !important;
    border: none !important;
    width: 100% !important;
}

.stButton>button {
    background-color: var(--primary) !important;
    color: white !important;
}

.stButton>button:hover {
    background-color: var(--dark) !important;
    transform: translateY(-2px) !important;
}

.stDownloadButton>button {
    background-color: var(--secondary) !important;
    color: white !important;
}

.stDownloadButton>button:hover {
    background-color: #0E8A42 !important;
    transform: translateY(-2px) !important;
}

/* File uploader styling */
.stFileUploader>section {
    border: 2px dashed var(--primary) !important;
    border-radius: 12px !important;
    padding: 32px !important;
    background: rgba(255,255,255,0.8) !important;
    transition: border-color 0.3s, background 0.3s !important;
}

.stFileUploader>section:hover {
    border-color: var(--accent) !important;
    background: rgba(255,255,255,1) !important;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--primary), var(--dark)) !important;
}

[data-testid="stSidebar"] * {
    color: white !important;
}

[data-testid="stSidebar"] .sidebar-content {
    background: transparent !important;
    padding: 16px !important;
}

/* Column alignment fixes */
.stColumn {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

/* Fix for multiselect styling in sidebar */
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="select"] {
    background-color: rgba(255,255,255,0.1) !important;
    border-color: rgba(255,255,255,0.3) !important;
}

/* Fix for slider in sidebar */
[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] {
    background-color: transparent !important;
}

/* Navbar styling */
.navbar-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background-color: transparent;
    border-radius: 6px;
    flex-wrap: wrap;
}

.navbar-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
}

/* Tab styling */
[data-testid="stTabs"] {
    margin-top: 1.5rem;
}

[role="tablist"] button {
    padding: 0.5rem 1rem !important;
}

/* Chart container alignment */
[data-testid="stVerticalBlock"] {
    gap: 1rem;
}

/* Dataframe styling */
[data-testid="stDataFrame"] {
    width: 100% !important;
}

/* Progress bar styling */
[role="progressbar"] {
    background-color: var(--accent) !important;
}

/* Expander styling */
[data-testid="stExpander"] [data-testid="stVerticalBlock"] {
    gap: 0.5rem;
}

/* Footer styling */
.footer {
    text-align: center;
    color: var(--text-light);
    margin-top: 2rem;
    padding-top: 1rem;
    border-top: 1px solid rgba(0,0,0,0.1);
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .main .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }
    
    .navbar-container {
        flex-direction: column;
        gap: 1rem;
    }
}
</style>
""", unsafe_allow_html=True)

# ─── NAVBAR ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="navbar-container">
    <div style="display: flex; align-items: center;">
        <h2 style="margin: 0; font-size: 1.75rem; color: var(--primary);">Caprae AI Leads</h2>
    </div>
    <div style="display: flex; gap: 2rem;">
        <div class="navbar-item">
            <div style="font-size: 1.4rem;">👤</div>
            <div style="font-size: 0.8rem;">Sales Team</div>
        </div>
        <div class="navbar-item">
            <div style="font-size: 1.4rem;">📅</div>
            <div style="font-size: 0.8rem;">{}</div>
        </div>
        <div class="navbar-item">
            <div style="font-size: 1.4rem;">⚙️</div>
            <div style="font-size: 0.8rem;">Settings</div>
        </div>
    </div>
</div>
""".format(pd.Timestamp.now().strftime("%b %d")), unsafe_allow_html=True)

st.markdown("---")

# ─── HERO SECTION ─────────────────────────────────────────────────────────────
def hero_section():
    c1, c2 = st.columns([3, 3], gap="medium")
    with c1:
        st.markdown("""
        <div class='card' style='min-height: 280px;'>
            <div>
                <h2 style='color: var(--accent); margin-top: 0;'>🚀 AI‑Powered Lead Intelligence</h2>
                <p style='color: var(--text-light);'>
                Transform domains into high‑quality sales leads with our enrichment engine.
                </p>
            </div>
            <div style='display:flex; gap:8px; flex-wrap: wrap; justify-content: center; margin-top: auto;'>
                <span style='background: rgba(110,72,170,0.1); color: var(--accent); padding:4px 8px; border-radius:16px; font-size: 0.8rem;'>+50 Data Points</span>
                <span style='background: rgba(18,161,80,0.1); color: var(--secondary); padding:4px 8px; border-radius:16px; font-size: 0.8rem;'>AI Scoring</span>
                <span style='background: rgba(31,44,86,0.1); color: var(--primary); padding:4px 8px; border-radius:16px; font-size: 0.8rem;'>CRM Ready</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class='card' style='background: linear-gradient(135deg,var(--primary),var(--dark)); color:white; min-height: 280px;'>
            <div>
                <h3 style='color: white; margin-top: 0;'>How it works</h3>
                <ol style='padding-left:1.2rem; color:rgba(255,255,255,0.9); text-align: left; margin-bottom: 1.5rem;'>
                    <li>Upload CSV with domains</li>
                    <li>We enrich with 50+ data points</li>
                    <li>AI scores each lead (1⁠–⁠100)</li>
                    <li>Download ready‑to‑use leads</li>
                </ol>
            </div>
            <div style='margin-top: auto;'></div> <!-- Empty spacer for alignment -->
        </div>
        """, unsafe_allow_html=True)

hero_section()

# ─── SIDEBAR FILTERS ───────────────────────────────────────────────────────────
def sidebar_filters():
    st.sidebar.markdown("<h3 style='color:white; margin-top: 0;'>🔍 Filters</h3>", unsafe_allow_html=True)
    min_score, max_score = st.sidebar.slider("Lead Score Range", 0, 100, (50, 100))
    industries = st.sidebar.multiselect(
        "Industries", ["Fintech","Ecommerce","Healthcare","SaaS"], default=["Fintech","SaaS"]
    )
    
    tech_opts = []
    if 'df_out' in st.session_state and not st.session_state.df_out.empty:
        try:
            # Flatten all tech stacks and get unique values
            tech_opts = sorted(set(tech for sublist in st.session_state.df_out['tech_stack'].dropna() for tech in sublist))
        except:
            tech_opts = []
    
    selected_tech = st.sidebar.multiselect("Tech Stack", tech_opts)
    st.sidebar.markdown("---")
    st.sidebar.markdown("Need help? 📞 support@caprae.com")
    return min_score, max_score, industries, selected_tech

min_score, max_score, industries, selected_tech = sidebar_filters()

# ─── METRIC CARDS ──────────────────────────────────────────────────────────────
def show_metrics(df=None, elapsed=None):
    cols = st.columns(4, gap="medium")
    metrics = [
        ("📊", "Total Leads", df.shape[0] if df is not None and not df.empty else "—", "var(--primary)"),
        ("🎯", "Avg. Score", f"{df.lead_score.mean():.1f}" if df is not None and not df.empty else "—", "var(--accent)"),
        ("🏆", "High ≥80", f"{(df.lead_score>=80).sum()}" if df is not None and not df.empty else "—", "var(--secondary)"),
        ("⏱️", "Time (s)", f"{elapsed:.1f}" if elapsed else "—", "var(--text-light)")
    ]
    
    for col, (icon, title, val, color) in zip(cols, metrics):
        col.markdown(
            f"""
            <div class='metric-card'>
                <div class='metric-icon' style='color:{color};'>{icon}</div>
                <div class='metric-value' style='color:{color};'>{val}</div>
                <div class='metric-label' style='color:var(--text-light);'>{title}</div>
            </div>
            """, unsafe_allow_html=True
        )

# ─── PROCESS SECTION ──────────────────────────────────────────────────────────
def process_section():
    left, right = st.columns([1, 2], gap="large")
    
    with left:
        st.markdown("### Upload Data")
        uploaded = st.file_uploader("CSV with `domain` column", type="csv", help="Upload a CSV file containing a 'domain' column")
        
        if uploaded:
            if uploaded.size == 0:
                st.error("Empty file—please upload a valid CSV.")
                return
            try:
                sample = pd.read_csv(uploaded, nrows=5)
                if 'domain' not in sample.columns:
                    st.error("Missing `domain` column.")
                    return
                with st.expander("Preview", expanded=True):
                    st.dataframe(sample, use_container_width=True)
            except Exception as e:
                st.error(f"Can't read CSV: {e}")
                return
        
        run = st.button("🚀 Enrich & Score Leads", disabled=not uploaded, use_container_width=True)
        
        if run:
            uploaded.seek(0)
            try:
                df_in = pd.read_csv(uploaded)
            except Exception as e:
                st.error(f"Failed to parse CSV: {e}")
                return
            
            if 'domain' not in df_in.columns or df_in.empty:
                st.error("CSV must have ≥1 row and a `domain` column.")
                return
            
            start = time.time()
            recs, bar, msg = [], st.progress(0), st.empty()
            
            for i, d in enumerate(df_in['domain']):
                try:
                    rec = enrich_domain(d)
                    rec['lead_score'] = score_lead(rec)
                    # Ensure tech_stack is always a list (even if empty)
                    rec['tech_stack'] = rec.get('tech_stack', [])
                    if not isinstance(rec['tech_stack'], list):
                        rec['tech_stack'] = [rec['tech_stack']] if pd.notna(rec['tech_stack']) else []
                    recs.append(rec)
                except Exception as e:
                    st.warning(f"Error processing {d}: {str(e)}")
                    continue
                pct = (i+1)/len(df_in)
                bar.progress(pct)
                msg.text(f"Processing {i+1}/{len(df_in)}")
            
            df_out = pd.DataFrame(recs)
            elapsed = time.time() - start
            st.session_state.df_out = df_out
            st.session_state.elapsed = elapsed
            st.success(f"Processed {len(df_out)} leads in {elapsed:.1f}s")
            st.balloons()
    
    with right:
        if 'df_out' in st.session_state:
            dfv = st.session_state.df_out.copy()
            
            # Apply filters
            dfv = dfv[
                (dfv.lead_score >= min_score) & 
                (dfv.lead_score <= max_score)
            ]
            
            if industries:
                dfv = dfv[dfv.industry.isin(industries)]
            
            if selected_tech:
                # Filter for leads that have ANY of the selected technologies
                dfv = dfv[dfv['tech_stack'].apply(
                    lambda tech_list: any(tech in selected_tech for tech in tech_list) if isinstance(tech_list, list) else False
                )]
            
            show_metrics(dfv, st.session_state.elapsed)
            
            tab1, tab2, tab3 = st.tabs(["📊 Overview", "🔍 Details", "💾 Export"])
            
            with tab1:
                st.markdown("#### Lead Score Distribution")
                hist = alt.Chart(dfv).mark_bar(color='#6E48AA').encode(
                    alt.X("lead_score:Q", bin=True, title="Lead Score"),
                    alt.Y("count()", title="Count of Records")
                ).properties(height=300)
                st.altair_chart(hist, use_container_width=True)
                
                st.markdown("#### Industry Breakdown")
                pie = alt.Chart(dfv).mark_arc(innerRadius=50).encode(
                    theta='count():Q', 
                    color=alt.Color('industry:N', legend=alt.Legend(orient="bottom"))
                ).properties(height=300)
                st.altair_chart(pie, use_container_width=True)
            
            with tab2:
                st.markdown("#### Enriched Leads Table")
                # Display tech stack as comma-separated string for better readability
                display_df = dfv.copy()
                display_df['tech_stack'] = display_df['tech_stack'].apply(
                    lambda x: ', '.join(x) if isinstance(x, list) and len(x) > 0 else 'None'
                )
                styled = display_df.reset_index(drop=True).style.background_gradient(
                    "Blues", subset=["lead_score"])
                st.dataframe(styled, use_container_width=True, height=600)
            
            with tab3:
                st.markdown("#### Export Your Data")
                fmt = st.radio("Format", ["CSV", "Excel", "JSON"], horizontal=True)
                
                if fmt == "CSV":
                    data = dfv.to_csv(index=False)
                    mime = "text/csv"
                    fn = "leads.csv"
                elif fmt == "Excel":
                    data = dfv.to_excel(index=False)
                    mime = "application/vnd.ms-excel"
                    fn = "leads.xlsx"
                else:
                    data = dfv.to_json(orient="records")
                    mime = "application/json"
                    fn = "leads.json"
                
                st.download_button("💾 Download", data=data, file_name=fn, mime=mime)
        else:
            st.info("Upload & click **Enrich & Score Leads** to begin.")

process_section()

# ─── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  © 2025 Caprae Capital • <a href='#' style='color:var(--text-light);'>Privacy</a> • <a href='#' style='color:var(--text-light);'>Terms</a>
</div>
""", unsafe_allow_html=True)