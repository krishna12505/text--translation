import streamlit as st
from deep_translator import GoogleTranslator
import time

# Page configuration
st.set_page_config(
    page_title="🌐 Language Translator", 
    page_icon="🌍", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #4CAF50, #2196F3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        padding-top: 1rem;
    }
    .sub-header {
        font-size: 1.4rem;
        color: #555;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .stButton > button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        padding: 0.75rem;
        border-radius: 10px;
        border: none;
    }
    .stTextArea textarea {
        min-height: 300px !important;
        font-size: 1.1rem !important;
        border-radius: 10px !important;
        border: 2px solid #e0e0e0 !important;
        padding: 12px !important;
    }
    .footer {
        text-align: center;
        margin-top: 2rem;
        color: #888;
        padding: 1rem;
        border-top: 1px solid #eee;
    }
    .char-counter {
        font-size: 0.9rem;
        color: #888;
        text-align: right;
        margin-top: 5px;
    }
</style>
""", unsafe_allow_html=True)

# App header
st.markdown("<div class='main-header'>🌐 Language Translator Pro</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Professional translation tool for multiple languages 🌏</div>", unsafe_allow_html=True)

# Initialize session state variables properly
if 'translation_history' not in st.session_state:
    st.session_state.translation_history = []
if 'translated_text' not in st.session_state:
    st.session_state.translated_text = ""
if 'source_language' not in st.session_state:
    st.session_state.source_language = "english"
if 'target_language' not in st.session_state:
    st.session_state.target_language = "french"
if 'input_text' not in st.session_state:
    st.session_state.input_text = ""
if 'translation_done' not in st.session_state:
    st.session_state.translation_done = False

# Get supported languages with error handling
try:
    @st.cache_data(ttl=3600)
    def get_languages():
        return GoogleTranslator().get_supported_languages(as_dict=True)
    
    languages = get_languages()
    language_names = list(languages.keys())
except Exception as e:
    st.warning(f"Could not load all languages. Using default set instead.")
    language_names = ["english", "french", "spanish", "german", "chinese", "japanese", "arabic", "russian"]

# Sidebar settings
with st.sidebar:
    st.header("🛠️ Translation Settings")
    
    # Language selection
    source_language = st.selectbox(
        "From:", 
        language_names,
        index=language_names.index(st.session_state.source_language) if st.session_state.source_language in language_names else 0,
        key="source_lang_select"
    )
    st.session_state.source_language = source_language
    
    target_language = st.selectbox(
        "To:", 
        language_names,
        index=language_names.index(st.session_state.target_language) if st.session_state.target_language in language_names else 1,
        key="target_lang_select"
    )
    st.session_state.target_language = target_language
    
    # Swap languages button
    if st.button("🔄 Swap Languages"):
        temp = st.session_state.source_language
        st.session_state.source_language = st.session_state.target_language
        st.session_state.target_language = temp
        st.rerun()
    
    # Advanced options
    st.markdown("---")
    auto_detect = st.checkbox("Auto-detect source language", value=False)
    show_history = st.checkbox("Show Translation History", value=True)
    max_history = st.slider("Max History Items:", min_value=1, max_value=20, value=5)

# Main content area
st.markdown("---")

# Two-column layout for source and target
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"📝 Source Text ({source_language.title()})")
    
    # Source text area - directly update session state
    text_input = st.text_area(
        "Enter text to translate:",
        value=st.session_state.input_text,
        height=350,
        key="text_area_input",
        placeholder="Type or paste your text here..."
    )
    # Update session state
    st.session_state.input_text = text_input
    
    # Character counter
    st.markdown(f"<div class='char-counter'>Character count: {len(text_input)}</div>", unsafe_allow_html=True)

with col2:
    st.subheader(f"🎯 Translated Text ({target_language.title()})")
    
    # Display the translated text
    output_area = st.empty()
    output_area.text_area(
        "Translation result:",
        value=st.session_state.translated_text,
        height=350,
        key="translation_output",
        placeholder="Translation will appear here...",
        disabled=True
    )
    
    # Download button (only if translation exists)
    if st.session_state.translated_text:
        st.download_button(
            label="💾 Download Translation",
            data=st.session_state.translated_text,
            file_name=f"translation_{source_language}_to_{target_language}.txt",
            mime="text/plain"
        )

# Function to perform translation
def translate_text():
    with st.spinner('Translating... Please wait'):
        source = 'auto' if auto_detect else st.session_state.source_language
        
        try:
            # Perform the actual translation
            translated = GoogleTranslator(
                source=source, 
                target=st.session_state.target_language
            ).translate(st.session_state.input_text)
            
            # Update session state with the translation result
            st.session_state.translated_text = translated
            
            # Add to history (managing maximum entries)
            if len(st.session_state.translation_history) >= max_history:
                st.session_state.translation_history.pop(0)
            
            st.session_state.translation_history.append({
                "source_lang": st.session_state.source_language if not auto_detect else "auto",
                "target_lang": st.session_state.target_language,
                "original": st.session_state.input_text,
                "translated": translated,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            })
            
            # Mark translation as done
            st.session_state.translation_done = True
            
            return True
        except Exception as e:
            st.error(f"Translation Error: {str(e)}")
            return False

# Translation button - using a separate container
translate_container = st.container()
with translate_container:
    if st.button("🔄 Translate Now", type="primary"):
        if st.session_state.input_text.strip():
            success = translate_text()
            if success:
                st.success("✅ Translation Completed!")
                
                # Update the output area directly
                output_area.text_area(
                    "Translation result:",
                    value=st.session_state.translated_text,
                    height=350,
                    key="translation_output_updated",
                    placeholder="Translation will appear here...",
                    disabled=True
                )
        else:
            st.warning("⚠️ Please enter text to translate!")

# Display translation history
if show_history and st.session_state.translation_history:
    st.markdown("---")
    st.subheader("📚 Translation History")
    
    for i, entry in enumerate(reversed(st.session_state.translation_history)):
        with st.expander(f"{entry['source_lang'].title()} → {entry['target_lang'].title()} ({entry['timestamp']})"):
            st.markdown("**Original:**")
            st.info(entry['original'])
            st.markdown("**Translated:**")
            st.success(entry['translated'])
            
            # Add a "Use this text" button to load previous translations
            if st.button(f"Use as input", key=f"use_text_{i}"):
                st.session_state.input_text = entry['original']
                st.rerun()
    
    # Clear history button
    if st.button("Clear History"):
        st.session_state.translation_history = []
        st.session_state.translated_text = ""
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div class='footer'>
    <p>Made with ❤️ using Streamlit & Deep Translator</p>
    <p style='font-size: 0.8rem; margin-top: 0.5rem;'>Supports 100+ languages</p>
</div>
""", unsafe_allow_html=True)