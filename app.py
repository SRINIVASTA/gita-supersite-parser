import streamlit as st
import json
import re

# Crucial: Import your standalone data engine from pipeline.py
from pipeline import IndicDataPipeline

# --- Streamlit Configuration Settings ---
st.set_page_config(page_title="IITK Indic Data Pipeline", layout="wide", page_icon="🕉️")

# --- Custom CSS Styling Layer ---
st.markdown("""
    <style>
    /* Main App Background Normalization */
    .stApp {
        background-color: #f8fafc;
    }
    /* Header and Title Typography */
    h1, h2, h3 {
        color: #0f172a !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 700;
    }
    /* Structural Card Containers for Options, Metrics, and Alerts */
    div[data-testid="stColumn"], div[data-testid="element-container"] > div.stAlert, .upload-container {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    /* Metric Card Enhancements */
    div[data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: #4f46e5 !important;
    }
    div[data-testid="stMetricLabel"] {
        font-weight: 600 !important;
        color: #475569 !important;
    }
    /* Action Button Adjustments */
    .stButton>button {
        width: 100%;
        border-radius: 8px !important;
        font-weight: 600 !important;
        background-color: #4f46e5 !important;
        color: white !important;
        border: none !important;
        padding: 12px 0px !important;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #4338ca !important;
        box-shadow: 0 10px 15px -3px rgba(79, 70, 229, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

# --- Streamlit Presentation Layer ---
st.title("🕉️ IIT Kanpur Git Supersite Data Pipeline")
st.markdown("Transform unstructured raw file layouts into clean, schema-validated multilingual JSON objects instantaneously.")
st.markdown("---")

# Single Container Layout for Local File Upload
raw_text_data = None

st.markdown("### 📁 Local File Drag & Drop")
uploaded_file = st.file_uploader(
    "Choose your unstructured text file (.txt):", 
    type=['txt'],
    help="Upload files directly from your workspace directory disk storage."
)

if uploaded_file is not None:
    raw_text_data = uploaded_file.getvalue().decode("utf-8")
    st.success("✅ Local file verified and uploaded successfully!")

# --- Processing Runtime Layer ---
if raw_text_data:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀 Execute Engine Pipeline", type="primary"):
        with st.spinner("Executing regex parser matrix components..."):
            # Fire parsing engine tasks
            pipeline = IndicDataPipeline(raw_text_data)
            clean_json_output = pipeline.run_parser_pipeline()
            
            # Save raw components to session state
            st.session_state['parsed_output'] = clean_json_output
            st.session_state['raw_text'] = raw_text_data
            # Set action flag to prevent state destruction on sidebar toggles
            st.session_state['pipeline_executed'] = True

# --- Persistent View Rendering Layer ---
if st.session_state.get('pipeline_executed', False):
    clean_json_output = st.session_state['parsed_output']
    raw_text_data = st.session_state['raw_text']
    verses = clean_json_output.get("verses", [])
    total_verses = len(verses)
    
    # Calculate Real-Time Metrics
    available_chapters = sorted(list(set(v["chapter"] for v in verses)))
    total_chapters = len(available_chapters)
    total_words = sum(v["analytics"]["word_count"] for v in verses)
    avg_word_count = round(total_words / total_verses, 1) if total_verses > 0 else 0.0
    
    # Track Validation Failures
    corrupted_verses = [v for v in verses if not v["validation"]["is_valid"]]
    
    # --- Real-Time Analytics UI Section ---
    st.markdown("### 📊 Live Pipeline Metrics")
    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        st.metric(label="Total Verses Parsed", value=total_verses)
    with m_col2:
        st.metric(label="Unique Chapters Found", value=total_chapters)
    with m_col3:
        st.metric(label="Avg Sanskrit Word Count", value=avg_word_count)
    
    # --- Integrity Validation Flag Center ---
    if corrupted_verses:
        st.markdown("<br>", unsafe_allow_html=True)
        st.error(f"⚠️ Validation Warning: Found {len(corrupted_verses)} structural data anomalies during parse run.")
        with st.expander("🔍 Click to Inspect Flagged Integrity Anomalies"):
            for bad_v in corrupted_verses:
                st.warning(f"**ID: {bad_v['verse_id']}** (Chapter {bad_v['chapter']}, Verse {bad_v['verse_number']})")
                for issue in bad_v["validation"]["flagged_issues"]:
                    st.write(f"• {issue}")
    else:
        st.markdown("<br>", unsafe_allow_html=True)
        st.success("💯 Integrity Check Passed: Zero data dropouts or blank translation slots discovered.")

    # --- Interactive Filtering Sidebar Component ---
    st.sidebar.markdown("### 🔍 Chapter Lookup Engine")
    filter_choice = st.sidebar.selectbox(
        "Filter Preview Database By Chapter:",
        options=["Show All Chapters"] + [f"Chapter {ch}" for ch in available_chapters]
    )
    
    # Safe lookup logic
    if filter_choice != "Show All Chapters":
        chapter_digits = re.findall(r'\d+', filter_choice)
        if chapter_digits:
            target_ch = int(chapter_digits[0])
            filtered_verses = [v for v in verses if v["chapter"] == target_ch]
            filtered_output = {
                "metadata": clean_json_output["metadata"],
                "verses": filtered_verses
            }
        else:
            filtered_output = clean_json_output
    else:
        filtered_output = clean_json_output

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Stringify payload without corrupting Unicode character maps
    json_str = json.dumps(filtered_output, indent=4, ensure_ascii=False)
    
    # UI Organization Elements
    tab1, tab2 = st.tabs(["📊 Interactive JSON Output", "📝 Checked Source Log"])
    
    with tab1:
        st.markdown(f"### Schema-Validated Dataset Result ({filter_choice})")
        st.json(filtered_output)
        
        st.markdown("---")
        st.download_button(
            label=f"💾 Download {filter_choice} JSON File",
            data=json_str,
            file_name="iitk_indic_parsed_output.json",
            mime="application/json"
        )
        
    with tab2:
        st.markdown("### System Log: Raw Plaintext String Preview")
        st.code(raw_text_data, language="text")
else:
    st.info("ℹ️ Pipeline Idle: Please upload a raw text file (.txt) up above to trigger processing.")
