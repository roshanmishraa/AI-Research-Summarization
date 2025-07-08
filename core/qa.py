import google.generativeai as genai
import streamlit as st

# Configure Gemini API key
genai.configure(api_key=st.secrets["gemini"]["api_key"])

# Use the free model
model = genai.GenerativeModel("gemini-1.5-flash")


def answer_question(document_text, user_question, history=""):
    prompt = f"""
Based only on the document below, answer the user's question and give a justification.

Document:
{document_text}

{history}

Current Question:
{user_question}

Provide an accurate answer with justification.
"""
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"❌ Error: {str(e)}"


def generate_challenge_questions(document_text):
    prompt = f"""
From the following document, create three logic-based or comprehension-based questions to test understanding:

{document_text}
"""
    try:
        response = model.generate_content(prompt)
        questions = response.text.strip().split("\n")
        return [{"question": q.strip()} for q in questions if q.strip()]
    except Exception as e:
        return [{"question": f"❌ Error: {str(e)}"}]


def evaluate_user_answer(document_text, question, user_answer):
    prompt = f"""
Document:
{document_text}

Question: {question}
User's Answer: {user_answer}

Evaluate the user's answer. Provide feedback with justification from the document.
"""
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"❌ Error: {str(e)}"


def extract_highlighted_snippet(document_text, user_question):
    prompt = f"""
From the following document, extract a direct snippet or paragraph that supports the answer to the user's question.

Document:
{document_text}

Question:
{user_question}

Only return a short paragraph or sentence that directly supports the answer.
"""
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"❌ Error: {str(e)}"

