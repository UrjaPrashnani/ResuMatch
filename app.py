from dotenv import load_dotenv

load_dotenv()
import base64
import streamlit as st
import os
import io
from PIL import Image 
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_cotent,prompt):
    model=genai.GenerativeModel('gemini-2.5-pro')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ## Convert the PDF to image
        images=pdf2image.convert_from_bytes(uploaded_file.read())

        first_page=images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

## Streamlit App

st.set_page_config(page_title="ResuMatch - ATS")

st.header("🧠 ResuMatch - Smart ATS Evaluator")
st.write("Upload your resume and get a personalized JD match score with keyword analysis 💼✨")
input_text=st.text_area("Job Description: ",key="input")
uploaded_file=st.file_uploader("Upload your resume(PDF)...",type=["pdf"])


if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")


submit = st.button("Submit")



input_prompt = """
Hey Act Like a skilled or very experience ATS(Application Tracking System)
with a deep understanding of tech field,software engineering,data science ,data analyst
and big data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving thr resumes. Assign the percentage Matching based 
on Jd and
the missing keywords with high accuracy
resume:{text}
description:{jd}

I want the response in one single string having the structure
JD Match:%

MissingKeywords:

Profile Summary:
"""



if submit:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")

st.markdown("""<style>
/* Background gradient for the entire page */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #dbeafe, #f8fafc);
    color: #1e293b;
    font-family: 'Segoe UI', sans-serif;
}
/* Transparent header with shadow */
[data-testid="stHeader"] {
    background: rgba(255, 255, 255, 0.0);
    box-shadow: none;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background: linear-gradient(135deg, #e0f2fe, #f0f9ff);
    border-right: 2px solid #bfdbfe;
}
/* Title styling */
h1, h2, h3 {
    color: #1e40af;
    text-align: center;
    font-weight: 700;
}

/* Text area and uploader container */
textarea, .stTextArea textarea {
    border-radius: 10px !important;
    border: 1.5px solid #93c5fd !important;
    background-color: #f8fafc !important;
    padding: 10px !important;
    color: #1e293b !important;
}

/* Upload button */
div[data-testid="stFileUploader"] {
    background-color: #ffffff;
    border-radius: 12px;
    padding: 15px;
    border: 2px dashed #93c5fd;
    transition: all 0.3s ease;
}
div[data-testid="stFileUploader"]:hover {
    border-color: #3b82f6;
}

/* Submit button styling */
div.stButton > button:first-child {
    background: linear-gradient(90deg, #2563eb, #3b82f6);
    color: white;
    font-weight: 600;
    border: none;
    border-radius: 12px;
    padding: 10px 24px;
    transition: 0.3s ease-in-out;
    box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
}
div.stButton > button:first-child:hover {
    background: linear-gradient(90deg, #1d4ed8, #2563eb);
    transform: scale(1.05);
}


/* Subheader and messages */
.css-10trblm, .stSubheader {
    color: #1e3a8a !important;
    text-align: center !important;
}
       </style>
""" ,unsafe_allow_html=True)







