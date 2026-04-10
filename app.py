import streamlit as st
import pandas as pd
from ai_engine import generate_content, Slide, DataRow
from file_builder import create_pptx, create_xlsx

# 1. PAGE CONFIG
st.set_page_config(page_title="AIDeck | AI File Agent", page_icon="🤖", layout="wide") 

# 2. APP MEMORY
if "ai_data" not in st.session_state:
    st.session_state.ai_data = None
if "topic" not in st.session_state:
    st.session_state.topic = ""
if "active_theme" not in st.session_state:
    st.session_state.active_theme = "Breeze" 
if "draft_version" not in st.session_state:
    st.session_state.draft_version = 1 
if "cover_style" not in st.session_state:
    st.session_state.cover_style = "Modern Circle"

# 3. LIVE PREVIEW ENGINES
def render_cover_preview(title, theme_data, style):
    bg_col = theme_data.get("bg", "#FFFFFF")
    title_col = theme_data.get("color", "#0369A1")
    
    if style == "Modern Circle":
        html_string = f"""
        <div style="background-color: {bg_col}; padding: 30px; border-radius: 12px; border: 1px solid #ddd; width: 100%; aspect-ratio: 16/9; display: flex; align-items: center; justify-content: center; font-family: sans-serif; position: relative; box-sizing: border-box; box-shadow: 0 4px 10px rgba(0,0,0,0.05); overflow: hidden;">
            <div style="position: absolute; left: -10%; bottom: -20%; width: 50%; aspect-ratio: 1/1; background-color: {title_col}; opacity: 0.1; border-radius: 50%;"></div>
            <h1 style="color: {title_col}; font-size: 2.5rem; text-align: center; z-index: 1; margin: 0;">{title}</h1>
        </div>
        """
    elif style == "Split Accent":
        html_string = f"""
        <div style="background-color: {bg_col}; padding: 30px; border-radius: 12px; border: 1px solid #ddd; width: 100%; aspect-ratio: 16/9; display: flex; align-items: center; justify-content: flex-start; padding-left: 10%; font-family: sans-serif; position: relative; box-sizing: border-box; box-shadow: 0 4px 10px rgba(0,0,0,0.05); overflow: hidden;">
            <div style="position: absolute; left: 0; top: 0; bottom: 0; width: 25px; background-color: {title_col};"></div>
            <h1 style="color: {title_col}; font-size: 2.5rem; text-align: left; z-index: 1; margin: 0;">{title}</h1>
        </div>
        """
    else: 
        html_string = f"""
        <div style="background-color: {bg_col}; padding: 30px; border-radius: 12px; border: 1px solid #ddd; width: 100%; aspect-ratio: 16/9; display: flex; align-items: center; justify-content: center; font-family: sans-serif; position: relative; box-sizing: border-box; box-shadow: 0 4px 10px rgba(0,0,0,0.05); overflow: hidden;">
            <div style="position: absolute; top: 0; left: 0; right: 0; height: 20%; background-color: {title_col}; opacity: 0.15;"></div>
            <h1 style="color: {title_col}; font-size: 2.5rem; text-align: center; z-index: 1; margin: 0; margin-top: 10%;">{title}</h1>
        </div>
        """
    return html_string

def render_live_preview(title, bullets, theme_name, theme_data):
    bg_col = theme_data.get("bg", "#FFFFFF")
    title_col = theme_data.get("color", "#0369A1")
    text_col = theme_data.get("text", "#334155")
    bullet_html = "".join([f"<li style='color:{text_col}; margin-bottom:10px;'>{b}</li>" for b in bullets])
    
    return f"""
    <div style="background-color: {bg_col}; padding: 30px; border-radius: 12px; border: 1px solid #ddd; width: 100%; aspect-ratio: 16/9; overflow-y: auto; font-family: sans-serif; position: relative; box-sizing: border-box; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
        <div style="width: 100%; height: 8px; background-color: {title_col}; position: absolute; top: 0; left: 0; border-radius: 12px 12px 0 0;"></div>
        <h2 style="color: {title_col}; margin-top: 5px; font-size: 1.5rem; line-height: 1.2;">{title}</h2>
        <ul style="padding-left: 20px; font-size: 0.95rem; line-height: 1.5;">{bullet_html}</ul>
    </div>
    """

# 4. SIDEBAR
with st.sidebar:
    st.header("⚙️ Generation Settings")
    output_types = st.multiselect("What do you want to build?", ["Presentation (.pptx)", "Dataset (.xlsx)"])
    wants_ppt = "Presentation (.pptx)" in output_types
    wants_excel = "Dataset (.xlsx)" in output_types

    st.markdown("---")
    detail_level = st.radio("Level of Detail", ["Concise", "Standard", "Detailed"], index=1, horizontal=True)
    
    num_slides = st.slider("Number of Slides", 3, 10, 5) if wants_ppt else 5
    num_rows = st.slider("Dataset Rows", 5, 20, 10) if wants_excel else 10
    
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except:
        st.error("API Key missing!")
        api_key = None

# VIEW 1: Input Screen
if st.session_state.ai_data is None:
    st.title("🤖 AIDeck")
    topic_input = st.text_input("Project Topic", placeholder="e.g. Artemis 2 Mission")
    
    if st.button("Generate Draft", type="primary", use_container_width=True):
        if topic_input and api_key and (wants_ppt or wants_excel):
            with st.spinner("AI is drafting..."):
                result = generate_content(topic_input, num_slides, num_rows, detail_level, api_key)
                if isinstance(result, str):
                    st.error(f"AI Error: {result}")
                else:
                    st.session_state.topic = topic_input
                    st.session_state.ai_data = result
                    st.session_state.draft_version = 1 
                    st.rerun()
        else:
            st.warning("Please enter a topic and select file types.")

# VIEW 2: Review Screen
else:
    st.header(f"Drafting: {st.session_state.topic.title()}")
    THEMES = {
        "Breeze": {"font": "Helvetica", "color": "#0369A1", "bg": "#FFFFFF", "text": "#334155"},
        "Dark Executive": {"font": "Calibri", "color": "#63B3ED", "bg": "#0F172A", "text": "#94A3B8"},
        "Consultant": {"font": "Courier New", "color": "#2C5282", "bg": "#F7FAFC", "text": "#1A365D"}
    }

    tab_list = []
    if wants_ppt: tab_list += ["📝 Content", "🎨 Themes"]
    if wants_excel: tab_list += ["📊 Excel"]
    
    # --- FAIL-SAFE CHECK ---
    if not tab_list:
        st.warning("⚠️ Please select at least one output type in the sidebar to view your draft.")
        st.stop()
    
    tabs = st.tabs(tab_list)
    t_ptr = 0
    
    if wants_ppt:
        with tabs[t_ptr]:
            with st.expander("Cover Slide (Starting Card)", expanded=True):
                c1, c2 = st.columns([1, 1.2])
                with c1:
                    new_deck_title = st.text_input("Main Title", value=st.session_state.topic, key="deck_title_input")
                    st.session_state.topic = new_deck_title 
                    selected_cover = st.radio("Cover Style Layout", ["Modern Circle", "Split Accent", "Top Banner"], index=["Modern Circle", "Split Accent", "Top Banner"].index(st.session_state.cover_style))
                    st.session_state.cover_style = selected_cover
                with c2:
                    st.markdown(render_cover_preview(new_deck_title, THEMES[st.session_state.active_theme], selected_cover), unsafe_allow_html=True)
            
            st.divider()

            edited_slides = []
            for i, slide in enumerate(st.session_state.ai_data.presentation[:num_slides]):
                with st.expander(f"Slide {i+1}: {slide.title}", expanded=(i==0)):
                    c1, c2 = st.columns([1, 1.2])
                    with c1:
                        v_key = st.session_state.draft_version
                        nt = st.text_input("Title", value=slide.title, key=f"t_{v_key}_{i}")
                        nb_raw = st.text_area("Bullets", value="\n".join(slide.bullets), key=f"b_{v_key}_{i}", height=180)
                        nb = [b.strip() for b in nb_raw.split("\n") if b.strip()]
                        edited_slides.append(Slide(title=nt, bullets=nb))
                    with c2:
                        st.markdown(render_live_preview(nt, nb, st.session_state.active_theme, THEMES[st.session_state.active_theme]), unsafe_allow_html=True)
        t_ptr += 1
        
        with tabs[t_ptr]:
            tcols = st.columns(3)
            for i, (name, style) in enumerate(THEMES.items()):
                with tcols[i%3]:
                    st.markdown(f"<div style='background-color:{style['bg']}; padding:20px; border-radius:10px; border:2px solid {style['color']}; text-align:center;'><h4 style='color:{style['color']};'>{name}</h4></div>", unsafe_allow_html=True)
                    if st.session_state.active_theme == name:
                        st.button("✅ Active", key=f"btn_active_{name}", disabled=True, use_container_width=True)
                    else:
                        if st.button(f"Use {name}", key=f"btn_{name}", use_container_width=True):
                            st.session_state.active_theme = name
                            st.rerun()
        t_ptr += 1

    if wants_excel:
        with tabs[t_ptr]:
            df = pd.DataFrame([row.model_dump() for row in st.session_state.ai_data.dataset[:num_rows]])
            edf = st.data_editor(df, num_rows="dynamic", use_container_width=True, hide_index=True)
            edited_dataset = [DataRow(**row) for row in edf.to_dict('records') if all(row.values())]

    st.divider()
    acols = st.columns(3)
    with acols[0]:
        if wants_ppt and st.button("🚀 Build PPTX", type="primary", use_container_width=True):
            theme = THEMES[st.session_state.active_theme]
            f = create_pptx(edited_slides, st.session_state.topic, st.session_state.active_theme, theme['font'], theme['color'], theme['bg'], theme['text'])
            st.download_button("📥 Download PPTX", data=f, file_name="Slides.pptx", use_container_width=True)
    
    with acols[2]:
        if st.button("🔄 Update Draft", type="secondary", use_container_width=True):
            for key in list(st.session_state.keys()):
                if key.startswith("t_") or key.startswith("b_"):
                    del st.session_state[key]
            st.session_state.ai_data = None
            st.session_state.draft_version += 1 
            with st.spinner("Refining..."):
                res = generate_content(st.session_state.topic, num_slides, num_rows, detail_level, api_key)
                if not isinstance(res, str):
                    st.session_state.ai_data = res
                    st.rerun()

    if st.button("🗑️ Reset Agent"):
        st.session_state.clear()
        st.rerun()