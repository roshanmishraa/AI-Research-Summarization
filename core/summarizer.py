import streamlit as st
import google.generativeai as genai

# Gemini API key from Streamlit secrets
genai.configure(api_key=st.secrets["gemini"]["api_key"])

# Use the free-tier model (text-bison-001 is correct for most free accounts)
model = genai.GenerativeModel("gemini-1.5-flash")


def summarize_text(text):
    prompt = f"""Summarize the following document in 150 words or less:\n\n{text}"""

    try:
        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception as e:
        return f"❌ Error during summarization: {str(e)}"

