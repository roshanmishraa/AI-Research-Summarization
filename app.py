import streamlit as st
from core.parser import extract_text_from_pdf
from core.summarizer import summarize_text
from core.qa import answer_question, generate_challenge_questions, evaluate_user_answer, extract_highlighted_snippet

st.set_page_config(page_title="Smart Research Assistant", layout="wide")
st.title("📚 Smart Assistant for Research Summarization")

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

uploaded_file = st.file_uploader("Upload a PDF or TXT file", type=["pdf", "txt"])

if uploaded_file:
    with st.spinner("Reading document..."):
        text = extract_text_from_pdf(uploaded_file)

    with st.spinner("Generating summary (≤150 words)..."):
        summary = summarize_text(text)
        st.subheader("📌 Document Summary:")
        st.write(summary)

    mode = st.radio("Choose Mode", ["Ask Anything", "Challenge Me"])

    if mode == "Ask Anything":
        st.subheader("🤖 Ask Anything About the Document")
        user_question = st.text_input("Enter your question:")

        if user_question:
            with st.spinner("Generating answer with justification..."):
                history = ""
                for q, a in st.session_state.chat_history[-3:]:
                    history += f"Previous Q: {q}\nPrevious A: {a}\n"

                response = answer_question(text, user_question, history)
                snippet = extract_highlighted_snippet(text, user_question)

                st.markdown("**Answer:**")
                st.write(response)

                if snippet:
                    st.markdown("**🔍 Supporting Snippet from Document:**")
                    st.info(snippet)

                st.session_state.chat_history.append((user_question, response))

        if st.session_state.chat_history:
            st.subheader("🗂️ Conversation History")
            for i, (q, a) in enumerate(reversed(st.session_state.chat_history[-5:])):
                st.markdown(f"**Q:** {q}")
                st.markdown(f"**A:** {a}")

    elif mode == "Challenge Me":
        st.subheader("🧠 Challenge Questions")
        if st.button("Generate Questions"):
            questions = generate_challenge_questions(text)
            for i, q in enumerate(questions):
                st.markdown(f"**Q{i+1}: {q['question']}**")
                user_answer = st.text_input(f"Your Answer to Q{i+1}", key=f"q{i+1}")
                if user_answer:
                    evaluation = evaluate_user_answer(text, q['question'], user_answer)
                    st.markdown(f"✅ **Evaluation:** {evaluation}")
