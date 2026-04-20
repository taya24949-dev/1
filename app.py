import streamlit as st
import google.generativeai as genai
import pdfplumber
from docx import Document
import io

# עיצוב דף האתר
st.set_page_config(page_title="Syllabus To-Do List", layout="centered")
st.title("🎓 Syllabus To-Do Master")
st.subheader("העלי סילבוסים וקבלי צ'ק-ליסט שבועי מאוחד")

# הזנת מפתח API בצורה מאובטחת
api_key = st.sidebar.text_input("
AIzaSyB86uJxPLLcgrmGxvHLtQFRJAlYyHvOjqs", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # העלאת קבצים
    uploaded_files = st.file_uploader("בחרי קבצי PDF או Word", accept_multiple_files=True)

    if st.button("בנה לי צ'ק-ליסט!"):
        if uploaded_files:
            all_text = ""
            for file in uploaded_files:
                # קריאת הקבצים
                if file.name.endswith(".pdf"):
                    with pdfplumber.open(io.BytesIO(file.read())) as pdf:
                        all_text += "\n".join([p.extract_text() for p in pdf.pages if p.extract_text()])
                else:
                    doc = Document(io.BytesIO(file.read()))
                    all_text += "\n".join([p.text for p in doc.paragraphs])
            
            # שליחה ל-AI
            prompt = f"צור רשימת משימות שבועית מאוחדת עם [ ] לכל משימה בעברית מהטקסטים הבאים:\n{all_text}"
            response = model.generate_content(prompt)
            
            # הצגת התוצאה
            st.markdown("### 📋 הצ'ק-ליסט המאוחד שלך:")
            st.write(response.text)
        else:
            st.warning("נא להעלות לפחות קובץ אחד.")
else:
    st.info("אנא הזיני מפתח API בסרגל הצד כדי להתחיל.")
