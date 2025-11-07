{\rtf1\ansi\ansicpg1252\cocoartf2761
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import streamlit as st\
\
st.title("CV Scoring Test App")\
\
st.header("Step 1: Upload a Resume")\
uploaded_file = st.file_uploader("Upload a resume (PDF or DOCX)", type=["pdf", "docx"])\
\
if uploaded_file is not None:\
    st.success("File uploaded successfully!")\
\
    st.header("Step 2: General Qualification Scoring")\
\
    st.write("**Criteria:** Graduate Civil Engineer")\
    st.write("**Total Weight:** 15% (17.25 marks)")\
\
    # Simulated degree detection (you'll replace with actual parsing later)\
    degree = st.selectbox(\
        "Select candidate's qualification:",\
        ["PhD", "Postgraduate", "Graduate", "Diploma", "Other"]\
    )\
\
    if degree == "PhD":\
        rating = 100\
    elif degree == "Postgraduate":\
        rating = 95\
    elif degree == "Graduate":\
        rating = 90\
    elif degree == "Diploma":\
        rating = 75\
    else:\
        rating = 50\
\
    score = 17.25 * (rating / 100)\
    st.metric("Qualification Score", f"\{score:.2f\} / 17.25", f"\{rating\}%")\
}