import streamlit as st
from deep_translator import GoogleTranslator

st.set_page_config(page_title="🌐 Language Translator", page_icon="🌍", layout="centered")

# Title
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🌐 Language Translator App</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Effortlessly translate text between multiple languages 🌏</p>", unsafe_allow_html=True)
st.markdown("---")

# Fetch supported languages dynamically
languages = GoogleTranslator().get_supported_languages(as_dict=True)
language_names = list(languages.keys())

# Sidebar for language selection
st.sidebar.header("🛠️ Settings")
source_language = st.sidebar.selectbox("Select Source Language", language_names, index=language_names.index("english"))
target_language = st.sidebar.selectbox("Select Target Language", language_names, index=language_names.index("french"))

st.sidebar.markdown("---")
st.sidebar.info("Select languages from the dropdown and enter your text below to translate.")

# Main input
text = st.text_area("📝 Enter text to translate:", height=150)
st.caption(f"Character Count: {len(text)}")

# Translate button
if st.button("🔄 Translate"):
    if text.strip():
        with st.spinner('Translating... 🚀'):
            translated = GoogleTranslator(
                source=source_language, 
                target=target_language
            ).translate(text)
        st.success("✅ Translation Completed!")
        st.text_area("🎯 Translated Text:", value=translated, height=150)
        
        # Download button
        st.download_button(
            label="💾 Download Translation",
            data=translated,
            file_name="translation.txt",
            mime="text/plain"
        )
    else:
        st.warning("⚠️ Please enter text to translate!")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center;'>Made with ❤️ by Tanna Prasanth kumar using Streamlit & Deep Translator</p>", unsafe_allow_html=True)
