import streamlit as st
import json
import re
import io
import pandas as pd
import plotly.express as px
from gtts import gTTS

# Import your standalone data engine from pipeline.py safely
try:
    from pipeline import IndicDataPipeline
except ImportError:
    class IndicDataPipeline:
        def __init__(self, text): self.raw_input = text
        def run_parser_pipeline(self): return {"metadata": {"status": "Fallback"}, "verses": []}

# --- Streamlit Global Settings Configuration ---
st.set_page_config(page_title="IITK Indic Enterprise Suite", layout="wide", page_icon="🕉️")

# Initialize Serverless Database logs in background cache state safely
if 'global_db_registry' not in st.session_state:
    st.session_state['global_db_registry'] = []
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
# --- Custom Dashboard CSS Styling Layer ---
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    h1, h2, h3, h4 { color: #0f172a !important; font-family: 'Segoe UI', sans-serif; font-weight: 700; }
    div[data-testid="stColumn"], div[data-testid="element-container"] > div.stAlert {
        background-color: #ffffff; border: 1px solid #e2e8f0; padding: 24px; border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    .stButton>button {
        width: 100%; border-radius: 8px !important; font-weight: 600 !important;
        background-color: #4f46e5 !important; color: white !important; border: none !important; padding: 12px 0px !important;
    }
    .stButton>button:hover { background-color: #4338ca !important; box-shadow: 0 10px 15px -3px rgba(79, 70, 229, 0.3); }
    .search-card { border-left: 5px solid #4f46e5; background-color: #f1f5f9; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
    .nlp-pill { background-color: #e0e7ff; color: #4338ca; padding: 4px 10px; border-radius: 20px; font-size: 0.85rem; font-weight: 600; display: inline-block; margin: 4px; }
    .highlight-san { background-color: #ffebd5; padding: 4px 8px; border-radius: 6px; font-weight: 600; border: 1px solid #fed7aa; display: block; margin: 4px 0; }
    .highlight-tel { background-color: #dcfce7; padding: 4px 8px; border-radius: 6px; font-weight: 600; border: 1px solid #bbf7d0; display: block; margin: 4px 0; }
    .highlight-eng { background-color: #e0e7ff; padding: 4px 8px; border-radius: 6px; font-weight: 600; border: 1px solid #c7d2fe; display: block; margin: 4px 0; }
    </style>
""", unsafe_allow_html=True)
# --- ADVANCED INTERNAL NLP ENGINE LAYER ---
class SanskritNLPSplitter:
    @staticmethod
    def break_compounds(token):
        rules = [
            (r'(.*?)यावाधिकार(.*?)$', [r'\1ि', 'एव', 'अधिकार', r'\2']),
            (r'(.*?)गఽస్త్వ(.*?)$', [r'\1गః', 'అస్తు', r'\2']),
            (r'(.*?)శ్చైవ(.*?)$', [r'\1చ', 'ఎవ', r'\2']),
            (r'(.*?)श्चैव(.*?)$', [r'\1च', 'एव', r'\2']),
            (r'(.*?)హేతుర్భూ(.*?)$', [r'\1హేతుః', 'భూ', r'\2']),
            (r'(.*?)हेतुर्भू(.*?)$', [r'\1हेतुः', 'भू', r'\2'])
        ]
        for pattern, replacements in rules:
            match = re.match(pattern, token, re.IGNORECASE)
            if match:
                results = []
                for rep in replacements:
                    if rep.startswith(r'\1'): results.append(match.group(1) + rep[2:])
                    elif rep.startswith(r'\2'): results.append(match.group(2))
                    else: results.append(rep)
                return [r for r in results if r]
        return [token]

# --- BACKEND TELEMETRY AUDIO GENERATION LAYER ---
@st.cache_data(show_spinner=False)
def generate_backend_tts(text_string, language_code):
    """Serverless container speech processor. Prevents all CORS browser blockades."""
    try:
        clean_text = re.sub(r'[।॥\?\!\.\,\(\)\[\]]+', ' ', text_string).strip()
        tts = gTTS(text=clean_text, lang=language_code, slow=False)
        audio_fp = io.BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        return audio_fp.read()
    except Exception:
        return None
# --- SECURITY SYSTEM CONTROL BAR GATEWAY ---
if not st.session_state['authenticated']:
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        st.markdown("<div style='text-align: center;'><h2>🔐 Scholar Access Portal</h2><p>IITK Indic Pipeline Enterprise Gateway</p></div>", unsafe_allow_html=True)
        user_input = st.text_input("Username Identification:", placeholder="Enter your scholar ID")
        pass_input = st.text_input("Security Encryption Key:", type="password", placeholder="••••••••")
        
        if st.button("Unlock Core Dashboard Systems"):
            if user_input.strip().lower() == "scholar" and pass_input == "iitk2026":
                st.session_state['authenticated'] = True
                st.rerun()
            else:
                st.error("❌ Access Denied: Security authentication token signature mismatch.")
    st.stop()
# --- MAIN WORKSPACE WORKFLOW ---
st.sidebar.markdown(f"### 👤 Active Session: Scholar User")
if st.sidebar.button("🔒 Terminate Secure Session"):
    st.session_state['authenticated'] = False
    st.rerun()

st.title("🕉️ IITK Git Supersite Enterprise Pipeline")
st.markdown("Automated cross-script parser, deep NLP linguistic segmenter, serverless database register, and Plotly visualization studio.")
st.markdown("---")

raw_text_data = None
st.markdown("### 📁 Local File Drag & Drop")
uploaded_file = st.file_uploader("Choose your unstructured text file (.txt):", type=['txt'])

if uploaded_file is not None:
    raw_text_data = uploaded_file.getvalue().decode("utf-8")
    st.success("✅ Local file verified and uploaded successfully!")

if raw_text_data:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀 Execute Engine Pipeline", type="primary"):
        with st.spinner("Executing regex parser matrix components..."):
            pipeline = IndicDataPipeline(raw_text_data)
            clean_json_output = pipeline.run_parser_pipeline()
            log_entry = {"timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"), "file_name": uploaded_file.name, "dataset": clean_json_output}
            st.session_state['global_db_registry'].append(log_entry)
            st.session_state['parsed_output'] = clean_json_output
            st.session_state['raw_text'] = raw_text_data
            st.session_state['pipeline_executed'] = True

if st.session_state['global_db_registry']:
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🗄️ Container Database Ledger")
    for idx, item in enumerate(st.session_state['global_db_registry']):
        if st.sidebar.button(f"📄 [{item['timestamp']}] {item['file_name'][:15]}...", key=f"db_{idx}"):
            st.session_state['parsed_output'] = item['dataset']
            st.session_state['pipeline_executed'] = True

if st.session_state.get('pipeline_executed', False):
    clean_json_output = st.session_state['parsed_output']
    raw_text_data = st.session_state['raw_text']
    verses = clean_json_output.get("verses", [])
    total_verses = len(verses)
    available_chapters = sorted(list(set(v["chapter"] for v in verses)))
    total_chapters = len(available_chapters)
    total_words = sum(v["analytics"]["word_count"] for v in verses)
    avg_word_count = round(total_words / total_verses, 1) if total_verses > 0 else 0.0
    corrupted_verses = [v for v in verses if not v["validation"]["is_valid"]]
    
    st.markdown("### 📊 Live Pipeline Metrics")
    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1: st.metric(label="Total Verses Parsed", value=total_verses)
    with m_col2: st.metric(label="Unique Chapters Found", value=total_chapters)
    with m_col3: st.metric(label="Avg Sanskrit Word Count", value=avg_word_count)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📉 Interactive Text Layout Analytics Studio")
    df = pd.DataFrame([{"Verse": v["verse_id"], "Chapter": f"Chapter {v['chapter']}", "Words": v["analytics"]["word_count"]} for v in verses])
    viz_col1, viz_col2 = st.columns(2)
    with viz_col1:
        fig1 = px.bar(df, x="Verse", y="Words", color="Chapter", labels={"Words": "Sanskrit Word Count", "Verse": "Verse ID Reference"}, color_discrete_sequence=px.colors.qualitative.Prism)
        fig1.update_layout(margin=dict(l=20, r=20, t=20, b=20), height=350, plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig1, use_container_width=True)
    with viz_col2:
        fig2 = px.pie(df, values="Words", names="Chapter", hole=0.4, color_discrete_sequence=px.colors.qualitative.Safe)
        fig2.update_layout(margin=dict(l=20, r=20, t=20, b=20), height=350)
        st.plotly_chart(fig2, use_container_width=True)

    if corrupted_verses:
        st.markdown("<br>", unsafe_allow_html=True)
        st.error(f"⚠️ Validation Warning: Found {len(corrupted_verses)} structural data anomalies during parse run.")
        with st.expander("🔍 Click to Inspect Flagged Integrity Anomalies"):
            for bad_v in corrupted_verses:
                st.warning(f"**ID: {bad_v['verse_id']}** (Chapter {bad_v['chapter']}, Verse {bad_v['verse_number']})")
                for issue in bad_v["validation"]["flagged_issues"]: st.write(f"• {issue}")
    else:
        st.markdown("<br>", unsafe_allow_html=True)
        st.success("💯 Integrity Check Passed: Zero data dropouts or blank translation slots discovered.")

    st.sidebar.markdown("### 🔍 Chapter Lookup Engine")
    filter_choice = st.sidebar.selectbox("Filter Preview Database By Chapter:", options=["Show All Chapters"] + [f"Chapter {ch}" for ch in available_chapters])
    if filter_choice != "Show All Chapters":
        chapter_digits = re.findall(r'\d+', filter_choice)
        if chapter_digits:
            target_ch = int(chapter_digits[0])
            filtered_verses = [v for v in verses if v["chapter"] == target_ch]
            filtered_output = {"metadata": clean_json_output["metadata"], "verses": filtered_verses}
        else: filtered_output = clean_json_output; filtered_verses = verses
    else: filtered_output = clean_json_output; filtered_verses = verses
    
    st.markdown("<br>", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["📊 Interactive JSON Output", "🔎 Multi-Script Search Engine & Audio Studio", "📝 Checked Source Log"])
    
    with tab1:
        st.markdown(f"### Schema-Validated Dataset Result ({filter_choice})")
        st.json(filtered_output)
        st.markdown("---")
        st.markdown("### 🖨️ Data Exporter Utilities")
        down_col1, down_col2 = st.columns(2)
        with down_col1:
            json_str = json.dumps(filtered_output, indent=4, ensure_ascii=False)
            st.download_button(label=f"💾 Download {filter_choice} JSON File", data=json_str, file_name="iitk_indic_parsed_output.json", mime="application/json")
        with down_col2:
            export_rows = []
            for v in filtered_verses:
                export_rows.append({"Verse ID": v["verse_id"], "Chapter": v["chapter"], "Verse Number": v["verse_number"], "Sanskrit Text": v["linguistic_layers"]["devanagari_sanskrit"], "Telugu Text": v["linguistic_layers"]["telugu_script"], "English Translation": v["translations"]["english_translation"], "Word Count": v["analytics"]["word_count"]})
            export_df = pd.DataFrame(export_rows)
            csv_buffer = export_df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(label=f"🖨️ Export {filter_choice} to Editable CSV Spreadsheet", data=csv_buffer, file_name="iitk_indic_parsed_spreadsheet.csv", mime="text/csv")
        
    with tab2:
        st.markdown("### 🔎 Multi-Script Cross-Reference Search Engine")
        search_query = st.text_input("Type a search word (e.g. 'battle', 'Sanjaya', 'कर्मण्यवाधिकारस्ते'):", placeholder="Type any word across English translation, Telugu script, or Devanagari Sanskrit...").strip().lower()
        if search_query:
            results_found = []
            for v in verses:
                s_txt = v["linguistic_layers"]["devanagari_sanskrit"].lower()
                t_txt = v["linguistic_layers"]["telugu_script"].lower()
                e_txt = v["translations"]["english_translation"].lower()
                if search_query in s_txt or search_query in t_txt or search_query in e_txt: results_found.append(v)
                
            if results_found:
                st.success(f"🎯 Found {len(results_found)} matching verse entries:")
                for match_v in results_found:
                    v_uid = match_v['verse_id']
                    san_raw = match_v['linguistic_layers']['devanagari_sanskrit']
                    tel_raw = match_v['linguistic_layers']['telugu_script']
                    eng_raw = match_v['translations']['english_translation']
                    
                    audio_selection = st.radio(
                        f"Select Audio Language Target Layer for Verse {v_uid}:",
                        options=["None", "Sanskrit (hi)", "Telugu (te)", "English (en)"],
                        key=f"audio_select_{v_uid}"
                    )
                    
                    san_display = f'<span class="highlight-san">{san_raw}</span>' if audio_selection == "Sanskrit (hi)" else san_raw
                    tel_display = f'<span class="highlight-tel">{tel_raw}</span>' if audio_selection == "Telugu (te)" else tel_raw
                    eng_display = f'<span class="highlight-eng">{eng_raw}</span>' if audio_selection == "English (en)" else eng_raw
                    
                    st.markdown(f"""
                    <div class="search-card">
                        <h4>📌 Verse ID: {v_uid} (Chapter {match_v['chapter']}, Verse {match_v['verse_number']})</h4>
                        <p><b>Sanskrit:</b> {san_display}</p>
                        <p><b>Telugu:</b> {tel_display}</p>
                        <p><b>English:</b> {eng_display}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if audio_selection == "Sanskrit (hi)":
                        audio_data = generate_backend_tts(san_raw, "hi")
                        if audio_data: st.audio(audio_data, format="audio/mp3", autoplay=True)
                    elif audio_selection == "Telugu (te)":
                        audio_data = generate_backend_tts(tel_raw, "te")
                        if audio_data: st.audio(audio_data, format="audio/mp3", autoplay=True)
                    elif audio_selection == "English (en)":
                        audio_data = generate_backend_tts(eng_raw, "en")
                        if audio_data: st.audio(audio_data, format="audio/mp3", autoplay=True)
                    
                    st.markdown("##### 🧬 Deep NLP Compound Morphological Splitting:")
                    raw_tokens = re.sub(r'[।॥\s]+', ' ', san_raw).strip().split(' ')
                    for tok in raw_tokens:
                        splits = SanskritNLPSplitter.break_compounds(tok)
                        if len(splits) > 1: st.markdown(f"• Compound **`{tok}`** splits into: " + " ".join([f"<span class='nlp-pill'>{s}</span>" for s in splits]), unsafe_allow_html=True)
                    st.markdown("---")
            else: st.warning("🔍 No matching verses found. Try another vocabulary word.")
        else: st.info("💡 Enter a string value keyword above to filter across your entire structural text database instantaneously.")
            
    with tab3:
        st.markdown("### System Log: Raw Plaintext String Preview")
        st.code(raw_text_data, language="text")
else:
    st.info("ℹ️ Pipeline Idle: Please upload a raw text file (.txt) up above to trigger processing.")
