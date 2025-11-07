import streamlit as st
import docx2txt
from PyPDF2 import PdfReader

st.set_page_config(page_title="CV Scoring Tool", page_icon="📄", layout="centered")

st.title("📄 CV Scoring Tool - General Qualification (Interactive Version)")

st.markdown("""
This tool evaluates **General Qualification (15%)** based on World Bank-style criteria  
for a **Contract Management Specialist / Team Leader** role.
""")

# --- Define scoring rules ---
SCORING_RULES = {
    "phd": 1.00,
    "doctor": 1.00,
    "master": 0.95,
    "m.tech": 0.95,
    "m.e": 0.95,
    "bachelor": 0.90,
    "b.tech": 0.90,
    "b.e": 0.90,
    "diploma": 0.70,
    
}

FULL_MARKS = 17.25  # total marks for General Qualification

# --- Upload section ---
uploaded_file = st.file_uploader("📤 Upload the candidate's CV (PDF or DOCX):", type=["pdf", "docx"])

if uploaded_file:
    # Extract text from file
    if uploaded_file.name.endswith(".pdf"):
        reader = PdfReader(uploaded_file)
        text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
    else:
        text = docx2txt.process(uploaded_file)

    text_lower = text.lower()

    # --- Detect degree keywords ---
    matched_levels = [key for key in SCORING_RULES.keys() if key in text_lower]

    if matched_levels:
        # pick best qualification found
        best_match = max(matched_levels, key=lambda k: SCORING_RULES[k])
        auto_rating = SCORING_RULES[best_match]
        st.success(f"🎓 Detected qualification: **{best_match.title()}**")

        # --- Manual adjustment ---
        st.markdown("### Adjust Rating (Evaluator Control)")
        adjusted_rating = st.slider(
            "Select final rating percentage based on overall qualification impression:",
            min_value=0,
            max_value=100,
            value=int(auto_rating * 100),
            step=1
        ) / 100

        # Compute final score
        score = round(FULL_MARKS * adjusted_rating, 2)
        st.metric("General Qualification Score", f"{score} / {FULL_MARKS}")
        st.progress(adjusted_rating)

    else:
        st.warning("No relevant qualification keywords found in the CV. Please verify manually.")
        adjusted_rating = st.slider(
            "Manually set a rating percentage if qualification was not detected:",
            min_value=0, max_value=100, value=0, step=1
        ) / 100
        score = round(FULL_MARKS * adjusted_rating, 2)
        st.metric("General Qualification Score", f"{score} / {FULL_MARKS}")
        st.progress(adjusted_rating)

    with st.expander("🔍 View extracted text"):
        st.text_area("CV Content Preview", text, height=300)

else:
    st.info("👆 Upload a PDF or DOCX resume to begin scoring.")
    
    # -------------------------
# Section 3: Overseas / Country Experience
# -------------------------
st.header("Section 3: Overseas / Country Experience")
st.write("**Weightage: 15% (17.25 marks)**")
st.write("Criteria: Familiarity & Experience in other countries")

# Input: Overseas Experience
overseas_experience = st.selectbox(
    "Select candidate's level of international experience:",
    [
        "Has international work experience (any country other than India)",
        "Worked on international projects remotely",
        "Has exposure through studies/internship abroad",
        "Worked only in India but aware of global standards",
        "Only domestic Indian experience (no global exposure)"
    ]
)

# Rating logic
if overseas_experience == "Has international work experience (any country other than India)":
    rating_overseas = 100
elif overseas_experience == "Worked on international projects remotely":
    rating_overseas = 95
elif overseas_experience == "Has exposure through studies/internship abroad":
    rating_overseas = 90
elif overseas_experience == "Worked only in India but aware of global standards":
    rating_overseas = 80
else:
    rating_overseas = 60

overseas_score = 17.25 * (rating_overseas / 100)
st.metric(label="Overseas / Country Experience Score", value=f"{overseas_score:.2f} / 17.25")



