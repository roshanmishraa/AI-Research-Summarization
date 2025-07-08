import pdfplumber

def extract_text_from_pdf(file):
    try:
        if file.name.endswith(".txt"):
            return file.read().decode("utf-8")

        with pdfplumber.open(file) as pdf:
            full_text = ""
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"
            return full_text.strip()

    except Exception as e:
        return f"❌ Error while extracting text: {str(e)}"
