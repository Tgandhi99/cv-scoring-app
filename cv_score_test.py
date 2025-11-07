import streamlit as st
import docx2txt
from PyPDF2 import PdfReader

st.set_page_config(page_title="CV Scoring Tool", page_icon="📄", layout="centered")

st.title("📄 CV Scoring Tool - General Qualification (Interactive Version)")

st.markdown("""
This tool evaluates all qualification based on World Bank-style criteria  
for a **Contract Management Specialist / Team Leader** role.
""")

# --- Define scoring rules ---
SCORING_RULES = {
    "phd": 1.00,
    "doctor": 1.00,
    "graduate": 1.00,
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
    # ----------------------------
# SECTION 2: PROJECT-RELATED EXPERIENCE (70%, 80.5 marks)
# ----------------------------
st.markdown("### **Section 2 – Project-Related Experience (70%, 80.5 marks)**")

with st.expander("🔹 Expand to rate Project-Related Experience (6 sub-parts)"):
    st.markdown("Each subpart has the same rating scale (100%, 90–99%, 80–89%, 70–79%, 1–69%, 0%).")

    def rating_to_score(rating_percent, total_marks):
        return rating_percent / 100 * total_marks

    # Common rating dropdown
    rating_options = {
        "100%": 100,
        "90–99%": 94.5,
        "80–89%": 84.5,
        "70–79%": 74.5,
        "1–69%": 50,
        "0%": 0
    }

    total_section2_score = 0

    # Part 1
    rating1 = st.selectbox("**Part 1 – Total Professional Experience (≥20 years preferred)**", list(rating_options.keys()), key="exp1")
    score1 = rating_to_score(rating_options[rating1], 13.5)
    st.write(f"Score: {score1:.2f} / 13.5")
    total_section2_score += score1

    # Part 2
    rating2 = st.selectbox("**Part 2 – Experience in quality label certification (LEED, GRIHA)**", list(rating_options.keys()), key="exp2")
    score2 = rating_to_score(rating_options[rating2], 13.5)
    st.write(f"Score: {score2:.2f} / 13.5")
    total_section2_score += score2

    # Part 3
    rating3 = st.selectbox("**Part 3 – Experience in project planning, resource calculations, delay analysis, correspondence management, FIDIC**", list(rating_options.keys()), key="exp3")
    score3 = rating_to_score(rating_options[rating3], 13.5)
    st.write(f"Score: {score3:.2f} / 13.5")
    total_section2_score += score3

    # Part 4
    rating4 = st.selectbox("**Part 4 – Experience as Team Leader / Deputy Team Leader (consulting, high-value infra projects)**", list(rating_options.keys()), key="exp4")
    score4 = rating_to_score(rating_options[rating4], 13.5)
    st.write(f"Score: {score4:.2f} / 13.5")
    total_section2_score += score4

    # Part 5
    rating5 = st.selectbox("**Part 5 – Experience handling hospital or hotel contracts**", list(rating_options.keys()), key="exp5")
    score5 = rating_to_score(rating_options[rating5], 13.5)
    st.write(f"Score: {score5:.2f} / 13.5")
    total_section2_score += score5

    # Part 6
    rating6 = st.selectbox("**Part 6 – Understanding of legal issues in contracts**", list(rating_options.keys()), key="exp6")
    score6 = rating_to_score(rating_options[rating6], 13.5)
    st.write(f"Score: {score6:.2f} / 13.5")
    total_section2_score += score6

    st.markdown("---")
    st.subheader(f"**Total Section 2 Score: {total_section2_score:.2f} / 80.5**")

    
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

# ----------------------------
# FINAL TOTAL SCORE
# ----------------------------
total_final_score = score + total_section2_score + overseas_score
st.markdown("---")
st.markdown(f"## 🏁 **Final Total Score: {total_final_score:.2f} / 115 marks**")


