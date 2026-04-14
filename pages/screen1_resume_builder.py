import streamlit as st
import random, io, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from shared_css import SHARED_CSS

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER

st.set_page_config(page_title="Resume Builder", page_icon="📝", layout="wide")
st.markdown(SHARED_CSS, unsafe_allow_html=True)

# ── Extra CSS fixes specific to this page ────────────────────────────────────
st.markdown("""
<style>
/* Fix expander arrow showing inside section headers */
.streamlit-expanderHeader svg { display: inline !important; }
/* Make expander headers cleaner */
.streamlit-expanderHeader {
    font-size: 14px !important;
    font-weight: 600 !important;
    color: #111111 !important;
    background: #f5f5f5 !important;
    border-radius: 10px !important;
    padding: 10px 14px !important;
}
/* Placeholder color fix for ALL inputs */
input::placeholder, textarea::placeholder {
    color: #888888 !important;
    opacity: 1 !important;
    font-style: italic;
    font-size: 13px;
}
input::-webkit-input-placeholder, textarea::-webkit-input-placeholder {
    color: #888888 !important;
    opacity: 1 !important;
    font-style: italic;
}
input::-moz-placeholder, textarea::-moz-placeholder {
    color: #888888 !important;
    opacity: 1 !important;
    font-style: italic;
}
/* Force Streamlit inner inputs to show grey placeholders */
.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #888888 !important;
    opacity: 1 !important;
    font-style: italic;
}
/* White background + dark typed text */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: #ffffff !important;
    color: #111111 !important;
    border: 2px solid #cccccc !important;
    border-radius: 10px !important;
}
/* ── Template selector radio fix ── */
div[data-testid="stRadio"] label {
    background: #1e1e1e !important;
    color: #ffffff !important;
    border: 2px solid #3a3a3a !important;
    border-radius: 10px !important;
    padding: 6px 14px !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    cursor: pointer;
    transition: border-color 0.2s;
}
div[data-testid="stRadio"] label:hover {
    border-color: #6aef8a !important;
}
div[data-testid="stRadio"] > div {
    gap: 8px !important;
    flex-wrap: wrap !important;
}
/* Selected radio label */
div[data-testid="stRadio"] label[data-checked="true"],
div[data-testid="stRadio"] label[aria-checked="true"] {
    border-color: #6aef8a !important;
    background: #111111 !important;
    color: #6aef8a !important;
}
/* Radio circle dot — hide or style */
div[data-testid="stRadio"] label span:first-child {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

# ── Summary templates ─────────────────────────────────────────────────────────
SUMMARY_TEMPLATES = [
    "A results-driven {degree} graduate from {college} with strong expertise in {top3}. Passionate about leveraging technology to solve real-world problems and deliver measurable impact. Seeking opportunities to contribute in fast-paced, innovative environments.",
    "Motivated {degree} professional with a solid foundation in {top3}. Demonstrated ability to collaborate across teams and deliver high-quality technical solutions. Bringing a growth mindset and strong work ethic to impactful projects.",
    "Detail-oriented {degree} graduate specializing in {top3}. Committed to continuous learning and applying modern tools to build scalable, efficient systems. Ready to contribute strong analytical thinking to any dynamic team.",
    "Enthusiastic technology professional with a {degree} background and hands-on experience in {top3}. Known for clean execution, structured thinking, and a passion for innovation. Eager to make meaningful contributions in a challenging role.",
    "A dedicated {degree} graduate from {college} with practical understanding of {top3}. Combines technical expertise with strong problem-solving skills. Thrives under pressure and consistently delivers quality results.",
]
def gen_summary(degree, college, skills):
    top3 = ", ".join(skills[:3]) if skills else "software development and problem-solving"
    return random.choice(SUMMARY_TEMPLATES).format(
        degree=degree or "Engineering",
        college=college or "a reputed institution",
        top3=top3
    )

# ── Session state defaults ────────────────────────────────────────────────────
DEFAULTS = {
    "full_name": "", "email": "", "phone": "", "linkedin": "", "github": "", "address": "",
    "degree": "", "college": "", "grad_year": "", "cgpa": "",
    "career_objective": "",
    "summary": "",
    "skills": [], "experiences": [], "projects": [], "certifications": [],
    "hobbies": [],
    "languages": [],
    "template": "ATS Clean",
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Nav ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="nav-bar">
  <div class="nav-title">📝 Resume Builder</div>
  <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;">
    <div class="nav-badge">Module 1 / 3</div>
    <div style="color:#aaaaaa;font-size:12px;">Free · No API</div>
  </div>
</div>""", unsafe_allow_html=True)

if st.button("← Home", key="home_btn"):
    st.switch_page("app.py")

st.markdown("<br>", unsafe_allow_html=True)
left, right = st.columns([1, 1], gap="large")

# ════════════════════════════════════════════════════════════════
# LEFT — INPUT FORM
# ════════════════════════════════════════════════════════════════
with left:

    # ── 01 Personal Info ──────────────────────────────────────────
    st.markdown('<div class="card"><div class="sl">01 — Personal Information</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    st.session_state.full_name = c1.text_input("Full Name",  st.session_state.full_name,  placeholder="Yash Sharma")
    st.session_state.email     = c2.text_input("Email",      st.session_state.email,      placeholder="yash@email.com")
    c3, c4 = st.columns(2)
    st.session_state.phone     = c3.text_input("Phone",      st.session_state.phone,      placeholder="+91 9876543210")
    st.session_state.address   = c4.text_input("City",       st.session_state.address,    placeholder="Nashik, India")
    c5, c6 = st.columns(2)
    st.session_state.linkedin  = c5.text_input("LinkedIn",   st.session_state.linkedin,   placeholder="linkedin.com/in/yash")
    st.session_state.github    = c6.text_input("GitHub",     st.session_state.github,     placeholder="github.com/yash")
    st.markdown('</div>', unsafe_allow_html=True)

    # ── 02 Education ──────────────────────────────────────────────
    st.markdown('<div class="card"><div class="sl">02 — Education</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    st.session_state.degree    = c1.text_input("Degree",          st.session_state.degree,    placeholder="B.E. Computer Engineering")
    st.session_state.college   = c2.text_input("College",         st.session_state.college,   placeholder="XYZ University")
    c3, c4 = st.columns(2)
    st.session_state.grad_year = c3.text_input("Graduation Year", st.session_state.grad_year, placeholder="2025")
    st.session_state.cgpa      = c4.text_input("CGPA / %",        st.session_state.cgpa,      placeholder="8.5 / 10")
    st.markdown('</div>', unsafe_allow_html=True)

    # ── 03 Career Objective ───────────────────────────────────────
    st.markdown('<div class="card"><div class="sl">03 — Career Objective</div>', unsafe_allow_html=True)
    st.session_state.career_objective = st.text_area(
        "Career Objective",
        st.session_state.career_objective,
        placeholder="e.g. To obtain a challenging position as a Software Engineer where I can apply my skills in Python and Machine Learning to build impactful products...",
        height=90,
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # ── 04 Professional Summary ───────────────────────────────────
    st.markdown('<div class="card"><div class="sl">04 — Professional Summary</div>', unsafe_allow_html=True)
    st.session_state.summary = st.text_area(
        "Summary", st.session_state.summary,
        placeholder="Write your summary or click Generate below...",
        height=100,
        label_visibility="collapsed"
    )
    if st.button("✨ Auto-Generate Summary (AI Style)", use_container_width=True):
        st.session_state.summary = gen_summary(
            st.session_state.degree, st.session_state.college, st.session_state.skills
        )
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # ── 05 Skills ─────────────────────────────────────────────────
    ALL_SKILLS = [
        "Python","JavaScript","React","Node.js","SQL","Machine Learning","Deep Learning",
        "TensorFlow","Docker","AWS","Git","Java","C++","FastAPI","MongoDB","PostgreSQL",
        "Pandas","NumPy","Scikit-learn","Flutter","Kotlin","REST APIs","TypeScript",
        "Next.js","HTML","CSS","Figma","Power BI","Excel","R","NLP","Computer Vision",
        "PyTorch","Spark","Kubernetes","Redis","GraphQL","Go","Rust","Unity"
    ]
    st.markdown('<div class="card"><div class="sl">05 — Skills</div>', unsafe_allow_html=True)
    rem = [s for s in ALL_SKILLS if s not in st.session_state.skills]
    sc1, sc2 = st.columns([3, 1])
    new_sk = sc1.selectbox("Pick a skill", ["Select..."] + rem, key="sk_sel")
    if sc2.button("Add", key="add_sk"):
        if new_sk != "Select..." and new_sk not in st.session_state.skills:
            st.session_state.skills.append(new_sk); st.rerun()
    custom = st.text_input("Or type a custom skill", placeholder="e.g. LangChain, Figma...", key="csk_in")
    if st.button("Add Custom Skill", key="csk_btn"):
        if custom and custom not in st.session_state.skills:
            st.session_state.skills.append(custom); st.rerun()
    if st.session_state.skills:
        st.markdown(
            "".join([f'<span class="skill-tag">{s}</span>' for s in st.session_state.skills])
            + "<div style='margin-top:8px;'></div>",
            unsafe_allow_html=True
        )
        rm = st.selectbox("Remove a skill", ["Select to remove..."] + st.session_state.skills, key="rm_sk")
        if st.button("Remove Selected", key="rm_sk_btn"):
            if rm in st.session_state.skills:
                st.session_state.skills.remove(rm); st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # ── 06 Work Experience ────────────────────────────────────────
    st.markdown('<div class="card"><div class="sl">06 — Work Experience</div>', unsafe_allow_html=True)
    with st.expander("➕ Add Experience"):
        ec1, ec2 = st.columns(2)
        e_co   = ec1.text_input("Company",  key="e_co",   placeholder="Google")
        e_role = ec2.text_input("Role",     key="e_role", placeholder="SDE Intern")
        e_dur  = st.text_input("Duration",  key="e_dur",  placeholder="June 2024 – Aug 2024")
        e_resp = st.text_area("Responsibilities", key="e_resp",
                              placeholder="• Built REST APIs\n• Improved DB speed by 30%", height=80)
        if st.button("Save Experience", key="save_exp"):
            if e_co and e_role:
                st.session_state.experiences.append({
                    "company": e_co, "role": e_role,
                    "duration": e_dur, "responsibilities": e_resp
                })
                st.rerun()
    for i, exp in enumerate(st.session_state.experiences):
        st.markdown(
            f'<div class="item-row"><strong>{exp["role"]}</strong> @ {exp["company"]}'
            f'<div class="item-sub">{exp["duration"]}</div></div>',
            unsafe_allow_html=True
        )
        if st.button("Remove", key=f"rm_exp_{i}"):
            st.session_state.experiences.pop(i); st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # ── 07 Projects ───────────────────────────────────────────────
    st.markdown('<div class="card"><div class="sl">07 — Projects</div>', unsafe_allow_html=True)
    with st.expander("➕ Add Project"):
        pt  = st.text_input("Project Title", key="pt",  placeholder="AI Chatbot")
        pd2 = st.text_area("Description",   key="pd2", placeholder="Built using Python + Streamlit...", height=70)
        ps  = st.text_input("Tech Stack",   key="ps",  placeholder="Python, Streamlit, NLP")
        if st.button("Save Project", key="save_proj"):
            if pt:
                st.session_state.projects.append({"title": pt, "description": pd2, "tech": ps})
                st.rerun()
    for i, proj in enumerate(st.session_state.projects):
        st.markdown(
            f'<div class="item-row"><strong>{proj["title"]}</strong>'
            f'<div class="item-sub" style="font-family:monospace;">{proj["tech"]}</div></div>',
            unsafe_allow_html=True
        )
        if st.button("Remove", key=f"rm_proj_{i}"):
            st.session_state.projects.pop(i); st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # ── 08 Certifications ─────────────────────────────────────────
    st.markdown('<div class="card"><div class="sl">08 — Certifications & Achievements</div>', unsafe_allow_html=True)
    with st.expander("➕ Add Certification / Award"):
        cn = st.text_input("Name", key="cn", placeholder="AWS Cloud Practitioner")
        ct = st.selectbox("Type", ["Certification", "Hackathon", "Award", "Other"], key="ct")
        if st.button("Save", key="save_cert"):
            if cn:
                st.session_state.certifications.append({"name": cn, "type": ct})
                st.rerun()
    for i, cert in enumerate(st.session_state.certifications):
        st.markdown(
            f'<div class="item-row">🏆 <strong>{cert["name"]}</strong>'
            f'<div class="item-sub">{cert["type"]}</div></div>',
            unsafe_allow_html=True
        )
        if st.button("Remove", key=f"rm_cert_{i}"):
            st.session_state.certifications.pop(i); st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # ── 09 Languages Known ────────────────────────────────────────
    ALL_LANGUAGES = [
        "English","Hindi","Marathi","Tamil","Telugu","Kannada","Malayalam","Bengali",
        "Gujarati","Punjabi","Urdu","French","German","Spanish","Japanese","Chinese",
        "Arabic","Portuguese","Russian","Korean"
    ]
    PROFICIENCY = ["Native", "Fluent", "Professional", "Conversational", "Basic"]
    st.markdown('<div class="card"><div class="sl">09 — Languages Known</div>', unsafe_allow_html=True)
    la1, la2, la3 = st.columns([2, 2, 1])
    lang_pick  = la1.selectbox("Language", ALL_LANGUAGES, key="lang_pick")
    lang_prof  = la2.selectbox("Proficiency", PROFICIENCY, key="lang_prof")
    if la3.button("Add", key="add_lang"):
        entry = f"{lang_pick} ({lang_prof})"
        if entry not in st.session_state.languages:
            st.session_state.languages.append(entry); st.rerun()
    lang_custom = st.text_input("Or type a language", placeholder="e.g. Konkani", key="lang_custom_in")
    lc1, lc2 = st.columns([2, 1])
    lang_cprof = lc1.selectbox("Proficiency for custom", PROFICIENCY, key="lang_cprof")
    if lc2.button("Add Custom", key="add_lang_custom"):
        if lang_custom:
            entry = f"{lang_custom} ({lang_cprof})"
            if entry not in st.session_state.languages:
                st.session_state.languages.append(entry); st.rerun()
    if st.session_state.languages:
        st.markdown(
            "".join([f'<span class="skill-tag" style="background:#1e3a5f;color:#90cdf4;">{l}</span>'
                     for l in st.session_state.languages])
            + "<div style='margin-top:8px;'></div>",
            unsafe_allow_html=True
        )
        rm_lang = st.selectbox("Remove a language", ["Select to remove..."] + st.session_state.languages, key="rm_lang")
        if st.button("Remove Selected", key="rm_lang_btn"):
            if rm_lang in st.session_state.languages:
                st.session_state.languages.remove(rm_lang); st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # ── 10 Hobbies & Interests ────────────────────────────────────
    HOBBY_SUGGESTIONS = [
        "Reading","Travelling","Photography","Gaming","Cooking","Music","Drawing",
        "Blogging","Open Source Contribution","Badminton","Chess","Cricket",
        "Cycling","Yoga","Volunteering","UI Design","Podcasting","Sketching"
    ]
    st.markdown('<div class="card"><div class="sl">10 — Hobbies & Interests</div>', unsafe_allow_html=True)
    hb1, hb2 = st.columns([3, 1])
    hobby_pick = hb1.selectbox("Pick a hobby", ["Select..."] + [h for h in HOBBY_SUGGESTIONS if h not in st.session_state.hobbies], key="hb_pick")
    if hb2.button("Add", key="add_hb"):
        if hobby_pick != "Select..." and hobby_pick not in st.session_state.hobbies:
            st.session_state.hobbies.append(hobby_pick); st.rerun()
    hobby_custom = st.text_input("Or type a custom hobby", placeholder="e.g. Drone Photography", key="hb_custom_in")
    if st.button("Add Custom Hobby", key="add_hb_custom"):
        if hobby_custom and hobby_custom not in st.session_state.hobbies:
            st.session_state.hobbies.append(hobby_custom); st.rerun()
    if st.session_state.hobbies:
        st.markdown(
            "".join([f'<span class="skill-tag" style="background:#2d1b4e;color:#c4b5fd;">{h}</span>'
                     for h in st.session_state.hobbies])
            + "<div style='margin-top:8px;'></div>",
            unsafe_allow_html=True
        )
        rm_hb = st.selectbox("Remove a hobby", ["Select to remove..."] + st.session_state.hobbies, key="rm_hb")
        if st.button("Remove Selected", key="rm_hb_btn"):
            if rm_hb in st.session_state.hobbies:
                st.session_state.hobbies.remove(rm_hb); st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
# RIGHT — LIVE PREVIEW
# ════════════════════════════════════════════════════════════════
with right:

    # ── Template selector ──────────────────────────────────────────────────────
    st.markdown(
        '<div class="card-dark"><div class="sl-dark">🎨 CHOOSE TEMPLATE</div>',
        unsafe_allow_html=True
    )
    template = st.radio(
        "template_radio_label",
        ["ATS Clean", "Modern Dark", "Creative Sidebar", "Minimal Pro"],
        horizontal=True,
        key="tmpl_radio",
        label_visibility="collapsed"
    )
    st.session_state.template = template
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Shared color tokens ────────────────────────────────────────────────────
    if template == "Modern Dark":
        BG  = "#111111"; TC  = "#ffffff"; SC  = "#cccccc"
        BRD = "#2a2a2a"; AC  = "#6aef8a"; dark = True
        SIDE_BG = None
    elif template == "Creative Sidebar":
        BG  = "#ffffff"; TC  = "#1a1a2e"; SC  = "#4a4a6a"
        BRD = "#e8e8f0"; AC  = "#6c63ff"; dark = False
        SIDE_BG = "#1a1a2e"
    elif template == "Minimal Pro":
        BG  = "#fafafa"; TC  = "#111111"; SC  = "#555555"
        BRD = "#eeeeee"; AC  = "#c0392b"; dark = False
        SIDE_BG = None
    else:  # ATS Clean
        BG  = "#ffffff"; TC  = "#111111"; SC  = "#444444"
        BRD = "#f0f2ee"; AC  = "#1a5c2a"; dark = False
        SIDE_BG = None

    # ── Section header helper ──────────────────────────────────────────────────
    def sec(t):
        if template == "Creative Sidebar":
            return (
                f'<div style="font-size:9px;letter-spacing:2.5px;font-weight:800;'
                f'text-transform:uppercase;color:#6c63ff;padding:2px 0 4px 0;'
                f'border-bottom:2px solid #6c63ff;margin:14px 0 6px 0;">{t}</div>'
            )
        elif template == "Minimal Pro":
            return (
                f'<div style="font-size:8px;letter-spacing:3px;font-weight:700;'
                f'text-transform:uppercase;color:#c0392b;padding:2px 0;'
                f'margin:14px 0 5px 0;">{t}</div>'
                f'<div style="border-bottom:1px solid #e0e0e0;margin-bottom:6px;"></div>'
            )
        else:
            return (
                f'<div style="font-size:9px;letter-spacing:2px;font-weight:700;text-transform:uppercase;'
                f'background:{BRD};color:{AC if dark else "#111111"};padding:3px 8px;'
                f'border-radius:4px;margin:12px 0 6px 0;display:inline-block;">{t}</div>'
                f'<div style="border-bottom:1px solid {"#333" if dark else "#e5e5e5"};margin-bottom:6px;"></div>'
            )

    contacts = " | ".join(filter(None, [
        st.session_state.email, st.session_state.phone,
        st.session_state.linkedin, st.session_state.github, st.session_state.address
    ]))

    # ════════════════════════════════════════
    # TEMPLATE: CREATIVE SIDEBAR
    # ════════════════════════════════════════
    if template == "Creative Sidebar":
        # Two-column sidebar layout
        html = (
            f'<div style="background:{BG};border-radius:16px;overflow:hidden;'
            f'box-shadow:0 4px 24px rgba(0,0,0,0.12);font-family:Arial,sans-serif;'
            f'display:flex;min-height:600px;">'
        )
        # LEFT sidebar
        html += (
            f'<div style="width:34%;background:{SIDE_BG};padding:24px 18px;'
            f'box-sizing:border-box;flex-shrink:0;">'
        )
        # Avatar circle with initials
        initials = "".join([w[0].upper() for w in (st.session_state.full_name or "YN").split()[:2]])
        html += (
            f'<div style="width:70px;height:70px;border-radius:50%;background:#6c63ff;'
            f'display:flex;align-items:center;justify-content:center;'
            f'font-size:22px;font-weight:700;color:#ffffff;margin:0 auto 14px auto;">'
            f'{initials}</div>'
        )
        html += (
            f'<div style="font-size:16px;font-weight:700;color:#ffffff;'
            f'text-align:center;line-height:1.3;margin-bottom:4px;">'
            f'{st.session_state.full_name or "Your Name"}</div>'
        )
        if st.session_state.degree:
            html += (
                f'<div style="font-size:9px;color:#a0a0c0;text-align:center;'
                f'margin-bottom:16px;letter-spacing:1px;">{st.session_state.degree}</div>'
            )
        # Contact info in sidebar
        if contacts:
            html += '<div style="margin-top:10px;">'
            html += '<div style="font-size:8px;letter-spacing:2px;font-weight:700;color:#6c63ff;text-transform:uppercase;margin-bottom:8px;">Contact</div>'
            for item in filter(None, [st.session_state.email, st.session_state.phone,
                                       st.session_state.address, st.session_state.linkedin,
                                       st.session_state.github]):
                html += f'<div style="font-size:9px;color:#c0c0e0;margin-bottom:4px;word-break:break-all;">{item}</div>'
            html += '</div>'
        # Skills in sidebar
        if st.session_state.skills:
            html += '<div style="margin-top:14px;">'
            html += '<div style="font-size:8px;letter-spacing:2px;font-weight:700;color:#6c63ff;text-transform:uppercase;margin-bottom:8px;">Skills</div>'
            for s in st.session_state.skills:
                html += (
                    f'<div style="background:rgba(108,99,255,0.25);color:#d0d0ff;'
                    f'border-radius:4px;padding:3px 8px;font-size:9px;font-weight:600;'
                    f'margin-bottom:4px;font-family:monospace;">{s}</div>'
                )
            html += '</div>'
        # Languages in sidebar
        if st.session_state.languages:
            html += '<div style="margin-top:14px;">'
            html += '<div style="font-size:8px;letter-spacing:2px;font-weight:700;color:#6c63ff;text-transform:uppercase;margin-bottom:8px;">Languages</div>'
            for l in st.session_state.languages:
                html += f'<div style="font-size:9px;color:#c0c0e0;margin-bottom:3px;">• {l}</div>'
            html += '</div>'
        # Hobbies in sidebar
        if st.session_state.hobbies:
            html += '<div style="margin-top:14px;">'
            html += '<div style="font-size:8px;letter-spacing:2px;font-weight:700;color:#6c63ff;text-transform:uppercase;margin-bottom:8px;">Interests</div>'
            for h in st.session_state.hobbies:
                html += (
                    f'<span style="display:inline-block;background:rgba(108,99,255,0.2);'
                    f'color:#c0c0ff;border-radius:20px;padding:2px 8px;font-size:8px;'
                    f'margin:2px;">{h}</span>'
                )
            html += '</div>'
        html += '</div>'  # end sidebar

        # RIGHT main content
        html += f'<div style="flex:1;padding:24px 22px;box-sizing:border-box;background:{BG};overflow:hidden;">'
        if st.session_state.career_objective or st.session_state.summary:
            html += sec("Profile")
            txt = st.session_state.career_objective or st.session_state.summary
            html += f'<div style="font-size:10px;color:{SC};line-height:1.7;margin-bottom:4px;">{txt}</div>'
        if st.session_state.degree or st.session_state.college:
            html += sec("Education")
            html += f'<div style="font-weight:700;font-size:11px;color:{TC};">{st.session_state.degree or "Degree"}</div>'
            edu_line = " | ".join(filter(None,[st.session_state.college, st.session_state.grad_year, st.session_state.cgpa]))
            html += f'<div style="font-size:9px;color:{SC};margin-bottom:4px;">{edu_line}</div>'
        if st.session_state.experiences:
            html += sec("Work Experience")
            for e in st.session_state.experiences:
                html += f'<div style="margin-bottom:8px;">'
                html += f'<div style="display:flex;justify-content:space-between;">'
                html += f'<span style="font-weight:700;font-size:11px;color:{TC};">{e["role"]}</span>'
                html += f'<span style="font-size:9px;color:{AC};">{e["duration"]}</span>'
                html += f'</div>'
                html += f'<div style="font-size:9px;color:{AC};font-weight:600;margin-bottom:2px;">{e["company"]}</div>'
                html += f'<div style="font-size:9px;color:{SC};line-height:1.5;">{e["responsibilities"].replace(chr(10),"<br>")}</div>'
                html += '</div>'
        if st.session_state.projects:
            html += sec("Projects")
            for p in st.session_state.projects:
                html += f'<div style="margin-bottom:7px;">'
                html += f'<span style="font-weight:700;font-size:11px;color:{TC};">{p["title"]}</span>'
                if p["tech"]:
                    html += f'<span style="font-size:8px;color:{AC};font-family:monospace;margin-left:6px;">[{p["tech"]}]</span>'
                html += f'<div style="font-size:9px;color:{SC};margin-top:1px;">{p["description"]}</div>'
                html += '</div>'
        if st.session_state.certifications:
            html += sec("Certifications")
            for c in st.session_state.certifications:
                html += f'<div style="font-size:10px;color:{SC};margin-bottom:3px;">🏆 <strong>{c["name"]}</strong> <span style="color:{AC};">({c["type"]})</span></div>'
        html += '</div>'  # end main
        html += '</div>'  # end flex wrapper

    # ════════════════════════════════════════
    # TEMPLATE: MINIMAL PRO
    # ════════════════════════════════════════
    elif template == "Minimal Pro":
        html = (
            f'<div style="background:{BG};border-radius:16px;padding:30px 36px;'
            f'min-height:560px;box-shadow:0 2px 16px rgba(0,0,0,0.07);'
            f'font-family:Georgia,serif;">'
        )
        # Header
        html += (
            f'<div style="border-left:4px solid {AC};padding-left:14px;margin-bottom:14px;">'
            f'<div style="font-size:26px;font-weight:700;color:{TC};letter-spacing:-0.5px;line-height:1.2;">'
            f'{st.session_state.full_name or "Your Name"}</div>'
        )
        if st.session_state.degree:
            html += f'<div style="font-size:12px;color:{AC};font-style:italic;margin-top:2px;">{st.session_state.degree}</div>'
        html += '</div>'
        if contacts:
            html += (
                f'<div style="font-size:9px;color:{SC};letter-spacing:0.5px;'
                f'margin-bottom:14px;font-family:Arial,sans-serif;">{contacts}</div>'
            )
        html += f'<div style="border-bottom:1px solid {AC};margin-bottom:12px;"></div>'

        if st.session_state.career_objective or st.session_state.summary:
            html += sec("Profile")
            txt = st.session_state.career_objective or st.session_state.summary
            html += f'<div style="font-size:10.5px;color:{SC};line-height:1.8;font-style:italic;margin-bottom:4px;">{txt}</div>'
        if st.session_state.degree or st.session_state.college:
            html += sec("Education")
            html += f'<div style="font-weight:700;font-size:11px;color:{TC};">{st.session_state.degree}</div>'
            edu_line = " · ".join(filter(None,[st.session_state.college, st.session_state.grad_year, st.session_state.cgpa]))
            html += f'<div style="font-size:9.5px;color:{SC};margin-bottom:4px;">{edu_line}</div>'
        if st.session_state.skills:
            html += sec("Skills")
            html += f'<div style="font-size:10px;color:{SC};line-height:2;">'
            html += "  ·  ".join(st.session_state.skills)
            html += '</div>'
        if st.session_state.experiences:
            html += sec("Experience")
            for e in st.session_state.experiences:
                html += f'<div style="margin-bottom:10px;">'
                html += f'<div style="display:flex;justify-content:space-between;align-items:baseline;">'
                html += f'<span style="font-weight:700;font-size:11px;color:{TC};">{e["role"]}</span>'
                html += f'<span style="font-size:9px;color:{SC};font-style:italic;">{e["duration"]}</span>'
                html += f'</div>'
                html += f'<div style="font-size:10px;color:{AC};margin-bottom:2px;font-style:italic;">{e["company"]}</div>'
                html += f'<div style="font-size:9.5px;color:{SC};line-height:1.6;">{e["responsibilities"].replace(chr(10),"<br>")}</div>'
                html += '</div>'
        if st.session_state.projects:
            html += sec("Projects")
            for p in st.session_state.projects:
                html += f'<div style="margin-bottom:8px;">'
                html += f'<span style="font-weight:700;font-size:11px;color:{TC};">{p["title"]}</span>'
                if p["tech"]:
                    html += f' <span style="font-size:9px;color:{SC};font-style:italic;font-family:monospace;">— {p["tech"]}</span>'
                html += f'<div style="font-size:9.5px;color:{SC};margin-top:1px;">{p["description"]}</div>'
                html += '</div>'
        if st.session_state.languages:
            html += sec("Languages")
            html += f'<div style="font-size:10px;color:{SC};">' + "  ·  ".join(st.session_state.languages) + '</div>'
        if st.session_state.hobbies:
            html += sec("Interests")
            html += f'<div style="font-size:10px;color:{SC};margin-top:2px;">' + "  ·  ".join(st.session_state.hobbies) + '</div>'
        if st.session_state.certifications:
            html += sec("Certifications")
            for c in st.session_state.certifications:
                html += f'<div style="font-size:10px;color:{SC};margin-bottom:2px;">— <strong>{c["name"]}</strong> ({c["type"]})</div>'
        html += '</div>'

    # ════════════════════════════════════════
    # TEMPLATE: ATS Clean + Modern Dark
    # ════════════════════════════════════════
    else:
        html  = f'<div style="background:{BG};border-radius:16px;padding:28px 32px;min-height:560px;box-shadow:0 4px 24px rgba(0,0,0,0.1);font-family:Arial,sans-serif;">'
        html += f'<div style="margin-bottom:10px;">'
        html += f'<div style="font-size:22px;font-weight:700;color:{TC};line-height:1.2;margin-bottom:4px;">{st.session_state.full_name or "Your Name"}</div>'
        if contacts:
            html += f'<div style="font-size:10px;color:{SC};line-height:1.6;word-break:break-word;">{contacts}</div>'
        html += f'</div>'
        html += f'<div style="border-bottom:2px solid {AC};margin-bottom:10px;"></div>'

        if st.session_state.career_objective:
            html += sec("Career Objective")
            html += f'<div style="font-size:11px;color:{SC};line-height:1.6;margin-bottom:4px;">{st.session_state.career_objective}</div>'
        if st.session_state.summary:
            html += sec("Professional Summary")
            html += f'<div style="font-size:11px;color:{SC};line-height:1.6;margin-bottom:4px;">{st.session_state.summary}</div>'
        if st.session_state.degree or st.session_state.college:
            html += sec("Education")
            html += f'<div style="font-weight:700;font-size:12px;color:{TC};">{st.session_state.degree or "Degree"}</div>'
            html += f'<div style="font-size:10px;color:{SC};margin-top:1px;margin-bottom:4px;">{" | ".join(filter(None,[st.session_state.college,st.session_state.grad_year,st.session_state.cgpa]))}</div>'
        if st.session_state.skills:
            html += sec("Skills")
            html += '<div style="margin-bottom:4px;">'
            html += "".join([
                f'<span style="display:inline-block;background:{"#222" if dark else "#111"};color:{AC};'
                f'border-radius:20px;padding:2px 9px;font-size:9px;font-weight:700;margin:2px;font-family:monospace;">{s}</span>'
                for s in st.session_state.skills
            ])
            html += '</div>'
        if st.session_state.experiences:
            html += sec("Work Experience")
            for e in st.session_state.experiences:
                html += f'<div style="margin-bottom:8px;">'
                html += f'<div style="display:flex;justify-content:space-between;align-items:baseline;">'
                html += f'<span style="font-weight:700;font-size:12px;color:{TC};">{e["role"]}</span>'
                html += f'<span style="font-size:10px;color:{SC};">{e["duration"]}</span>'
                html += f'</div>'
                html += f'<div style="font-size:10px;color:{AC};font-weight:600;">{e["company"]}</div>'
                html += f'<div style="font-size:10px;color:{SC};margin-top:2px;line-height:1.5;">{e["responsibilities"].replace(chr(10),"<br>")}</div>'
                html += '</div>'
        if st.session_state.projects:
            html += sec("Projects")
            for p in st.session_state.projects:
                html += f'<div style="margin-bottom:8px;">'
                html += f'<div style="font-weight:700;font-size:12px;color:{TC};">{p["title"]}</div>'
                html += f'<div style="font-size:9px;color:{AC};font-family:monospace;">{p["tech"]}</div>'
                html += f'<div style="font-size:10px;color:{SC};margin-top:2px;">{p["description"]}</div>'
                html += '</div>'
        if st.session_state.certifications:
            html += sec("Certifications & Achievements")
            html += f'<div style="font-size:11px;color:{SC};">'
            html += " &nbsp;·&nbsp; ".join([f'<strong>🏆</strong> {c["name"]}' for c in st.session_state.certifications])
            html += '</div>'
        if st.session_state.languages:
            html += sec("Languages Known")
            html += f'<div style="font-size:11px;color:{SC};">' + "  ·  ".join(st.session_state.languages) + '</div>'
        if st.session_state.hobbies:
            html += sec("Hobbies & Interests")
            html += f'<div style="font-size:11px;color:{SC};">' + "  ·  ".join(st.session_state.hobbies) + '</div>'
        html += '</div>'

    st.markdown(html, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # ── PDF Generation ────────────────────────────────────────────────────────
    def make_pdf():
        buf = io.BytesIO()
        doc = SimpleDocTemplate(
            buf, pagesize=A4,
            leftMargin=1.8*cm, rightMargin=1.8*cm,
            topMargin=1.8*cm, bottomMargin=1.8*cm
        )

        # ── Styles ──────────────────────────────────────────────────────────
        GREEN  = colors.HexColor('#3dcc6a')
        BLACK  = colors.HexColor('#111111')
        DARK   = colors.HexColor('#222222')
        MID    = colors.HexColor('#444444')
        LIGHT  = colors.HexColor('#f4f4f4')
        ACCENT = colors.HexColor('#1a5c2a')

        s_name = ParagraphStyle(
            'name', fontName='Helvetica-Bold', fontSize=20,
            textColor=BLACK, spaceAfter=2, leading=24
        )
        s_contact = ParagraphStyle(
            'contact', fontName='Helvetica', fontSize=8.5,
            textColor=MID, spaceAfter=0, leading=13
        )
        s_section = ParagraphStyle(
            'section', fontName='Helvetica-Bold', fontSize=8,
            textColor=BLACK, spaceBefore=10, spaceAfter=4,
            leading=10, backColor=LIGHT,
            leftIndent=0, rightIndent=0,
            borderPadding=(3, 6, 3, 6),
            textTransform='uppercase'
        )
        s_item_title = ParagraphStyle(
            'ititle', fontName='Helvetica-Bold', fontSize=10.5,
            textColor=BLACK, spaceAfter=1, leading=13
        )
        s_item_sub = ParagraphStyle(
            'isub', fontName='Helvetica', fontSize=8.5,
            textColor=MID, spaceAfter=2, leading=12
        )
        s_item_co = ParagraphStyle(
            'ico', fontName='Helvetica-Bold', fontSize=8.5,
            textColor=ACCENT, spaceAfter=1, leading=12
        )
        s_body = ParagraphStyle(
            'body', fontName='Helvetica', fontSize=9.5,
            textColor=DARK, spaceAfter=4, leading=14
        )
        s_skills = ParagraphStyle(
            'skills', fontName='Helvetica', fontSize=9.5,
            textColor=DARK, spaceAfter=4, leading=14
        )

        story = []

        # ── Name + contact + rule ────────────────────────────────────────────
        name_text = st.session_state.full_name or "Your Name"
        story.append(Paragraph(name_text, s_name))

        contact_parts = list(filter(None, [
            st.session_state.email, st.session_state.phone,
            st.session_state.linkedin, st.session_state.github,
            st.session_state.address
        ]))
        if contact_parts:
            story.append(Paragraph(" | ".join(contact_parts), s_contact))

        story.append(Spacer(1, 3))
        story.append(HRFlowable(
            width="100%", thickness=2,
            color=GREEN, spaceAfter=0, spaceBefore=0
        ))
        story.append(Spacer(1, 4))

        # ── Career Objective ─────────────────────────────────────────────────
        if st.session_state.career_objective.strip():
            story.append(Paragraph("CAREER OBJECTIVE", s_section))
            story.append(Paragraph(st.session_state.career_objective.strip(), s_body))

        # ── Professional Summary ─────────────────────────────────────────────
        if st.session_state.summary.strip():
            story.append(Paragraph("PROFESSIONAL SUMMARY", s_section))
            story.append(Paragraph(st.session_state.summary.strip(), s_body))

        # ── Education ────────────────────────────────────────────────────────
        if st.session_state.degree or st.session_state.college:
            story.append(Paragraph("EDUCATION", s_section))
            story.append(Paragraph(st.session_state.degree or "", s_item_title))
            edu_sub = " | ".join(filter(None, [
                st.session_state.college,
                st.session_state.grad_year,
                st.session_state.cgpa
            ]))
            if edu_sub:
                story.append(Paragraph(edu_sub, s_item_sub))

        # ── Skills ───────────────────────────────────────────────────────────
        if st.session_state.skills:
            story.append(Paragraph("SKILLS", s_section))
            story.append(Paragraph("  |  ".join(st.session_state.skills), s_skills))

        # ── Work Experience ──────────────────────────────────────────────────
        if st.session_state.experiences:
            story.append(Paragraph("WORK EXPERIENCE", s_section))
            for e in st.session_state.experiences:
                block = []
                block.append(Paragraph(f'<b>{e["role"]}</b>', s_item_title))
                block.append(Paragraph(
                    f'{e["company"]}  |  {e["duration"]}' if e["duration"] else e["company"],
                    s_item_co
                ))
                if e["responsibilities"].strip():
                    resp = e["responsibilities"].strip().replace("\n", "<br/>")
                    block.append(Paragraph(resp, s_body))
                block.append(Spacer(1, 3))
                story.extend(block)

        # ── Projects ─────────────────────────────────────────────────────────
        if st.session_state.projects:
            story.append(Paragraph("PROJECTS", s_section))
            for p in st.session_state.projects:
                block = []
                block.append(Paragraph(f'<b>{p["title"]}</b>', s_item_title))
                if p["tech"]:
                    block.append(Paragraph(f'Tech Stack: {p["tech"]}', s_item_co))
                if p["description"].strip():
                    block.append(Paragraph(p["description"].strip(), s_body))
                block.append(Spacer(1, 3))
                story.extend(block)

        # ── Certifications ───────────────────────────────────────────────────
        if st.session_state.certifications:
            story.append(Paragraph("CERTIFICATIONS & ACHIEVEMENTS", s_section))
            for c in st.session_state.certifications:
                story.append(Paragraph(f'• <b>{c["name"]}</b>  ({c["type"]})', s_body))

        # ── Languages Known ──────────────────────────────────────────────────
        if st.session_state.languages:
            story.append(Paragraph("LANGUAGES KNOWN", s_section))
            story.append(Paragraph("  |  ".join(st.session_state.languages), s_skills))

        # ── Hobbies & Interests ──────────────────────────────────────────────
        if st.session_state.hobbies:
            story.append(Paragraph("HOBBIES & INTERESTS", s_section))
            story.append(Paragraph("  |  ".join(st.session_state.hobbies), s_skills))

        doc.build(story)
        buf.seek(0)
        return buf.getvalue()

    # ── Extra PDF generators for Creative Sidebar & Minimal Pro ─────────────

    def make_pdf_creative_sidebar():
        """Two-column PDF: dark left sidebar + white right content."""
        from reportlab.platypus import Table, TableStyle
        buf = io.BytesIO()
        doc = SimpleDocTemplate(
            buf, pagesize=A4,
            leftMargin=0, rightMargin=0,
            topMargin=0, bottomMargin=0
        )

        PURPLE     = colors.HexColor('#6c63ff')
        DARK_NAVY  = colors.HexColor('#1a1a2e')
        WHITE      = colors.HexColor('#ffffff')
        LIGHT_BLUE = colors.HexColor('#c0c0e0')
        MID_BLUE   = colors.HexColor('#a0a0c0')
        BODY_DARK  = colors.HexColor('#333333')
        PAGE_W, PAGE_H = A4
        SIDE_W = PAGE_W * 0.33
        MAIN_W = PAGE_W - SIDE_W
        PAD = 0.45 * cm

        # ── Sidebar styles ──────────────────────────────────────────────────
        s_name_s = ParagraphStyle('ns', fontName='Helvetica-Bold', fontSize=13,
                                  textColor=WHITE, spaceAfter=2, leading=16, alignment=TA_CENTER)
        s_degree_s = ParagraphStyle('ds', fontName='Helvetica', fontSize=7.5,
                                    textColor=MID_BLUE, spaceAfter=8, leading=10, alignment=TA_CENTER)
        s_sec_s = ParagraphStyle('secs', fontName='Helvetica-Bold', fontSize=7,
                                 textColor=PURPLE, spaceBefore=10, spaceAfter=4,
                                 leading=9, letterSpacing=2)
        s_contact_s = ParagraphStyle('cs', fontName='Helvetica', fontSize=7.5,
                                     textColor=LIGHT_BLUE, spaceAfter=3, leading=11)
        s_skill_s = ParagraphStyle('sks', fontName='Helvetica-Bold', fontSize=7.5,
                                   textColor=colors.HexColor('#d0d0ff'), spaceAfter=3,
                                   leading=10, backColor=colors.HexColor('#2e2b5f'),
                                   leftIndent=4, rightIndent=4,
                                   borderPadding=(2, 6, 2, 6))
        s_hobby_s = ParagraphStyle('hs', fontName='Helvetica', fontSize=7.5,
                                   textColor=LIGHT_BLUE, spaceAfter=2, leading=10)

        # ── Main column styles ──────────────────────────────────────────────
        s_sec_m = ParagraphStyle('secm', fontName='Helvetica-Bold', fontSize=7.5,
                                 textColor=PURPLE, spaceBefore=10, spaceAfter=3,
                                 leading=9, letterSpacing=2,
                                 borderPadding=(0, 0, 3, 0))
        s_role_m = ParagraphStyle('rm', fontName='Helvetica-Bold', fontSize=10,
                                  textColor=colors.HexColor('#1a1a2e'), spaceAfter=1, leading=13)
        s_co_m   = ParagraphStyle('cm', fontName='Helvetica-Bold', fontSize=8,
                                  textColor=PURPLE, spaceAfter=1, leading=11)
        s_sub_m  = ParagraphStyle('sm', fontName='Helvetica', fontSize=8,
                                  textColor=colors.HexColor('#555577'), spaceAfter=2, leading=11)
        s_body_m = ParagraphStyle('bm', fontName='Helvetica', fontSize=8.5,
                                  textColor=BODY_DARK, spaceAfter=4, leading=13)

        # Build sidebar flowables
        sidebar_items = []
        sidebar_items.append(Spacer(1, 0.5*cm))

        # Initials circle (approximated as bold centered text with box)
        initials = "".join([w[0].upper() for w in (st.session_state.full_name or "YN").split()[:2]])
        s_init = ParagraphStyle('init', fontName='Helvetica-Bold', fontSize=20,
                                textColor=WHITE, alignment=TA_CENTER,
                                backColor=PURPLE, leading=28,
                                borderPadding=(10, 12, 10, 12))
        sidebar_items.append(Paragraph(initials, s_init))
        sidebar_items.append(Spacer(1, 8))
        sidebar_items.append(Paragraph(st.session_state.full_name or "Your Name", s_name_s))
        if st.session_state.degree:
            sidebar_items.append(Paragraph(st.session_state.degree, s_degree_s))

        # Contact
        contact_items = list(filter(None, [
            st.session_state.email, st.session_state.phone,
            st.session_state.address, st.session_state.linkedin, st.session_state.github
        ]))
        if contact_items:
            sidebar_items.append(Paragraph("CONTACT", s_sec_s))
            for item in contact_items:
                sidebar_items.append(Paragraph(item, s_contact_s))

        # Skills
        if st.session_state.skills:
            sidebar_items.append(Paragraph("SKILLS", s_sec_s))
            for sk in st.session_state.skills:
                sidebar_items.append(Paragraph(sk, s_skill_s))
                sidebar_items.append(Spacer(1, 2))

        # Languages
        if st.session_state.languages:
            sidebar_items.append(Paragraph("LANGUAGES", s_sec_s))
            for l in st.session_state.languages:
                sidebar_items.append(Paragraph(f"• {l}", s_contact_s))

        # Hobbies
        if st.session_state.hobbies:
            sidebar_items.append(Paragraph("INTERESTS", s_sec_s))
            sidebar_items.append(Paragraph("  ·  ".join(st.session_state.hobbies), s_hobby_s))

        # Build main column flowables
        main_items = []
        main_items.append(Spacer(1, 0.4*cm))

        def sec_m(title):
            return [
                Paragraph(title.upper(), s_sec_m),
                HRFlowable(width="100%", thickness=1.5, color=PURPLE, spaceAfter=4, spaceBefore=0)
            ]

        if st.session_state.career_objective or st.session_state.summary:
            main_items += sec_m("Profile")
            txt = st.session_state.career_objective or st.session_state.summary
            main_items.append(Paragraph(txt.strip(), s_body_m))

        if st.session_state.degree or st.session_state.college:
            main_items += sec_m("Education")
            main_items.append(Paragraph(st.session_state.degree or "", s_role_m))
            edu_sub = " | ".join(filter(None, [st.session_state.college, st.session_state.grad_year, st.session_state.cgpa]))
            if edu_sub:
                main_items.append(Paragraph(edu_sub, s_sub_m))

        if st.session_state.experiences:
            main_items += sec_m("Work Experience")
            for e in st.session_state.experiences:
                main_items.append(Paragraph(f'<b>{e["role"]}</b>', s_role_m))
                main_items.append(Paragraph(e["company"], s_co_m))
                if e["duration"]:
                    main_items.append(Paragraph(e["duration"], s_sub_m))
                if e["responsibilities"].strip():
                    main_items.append(Paragraph(e["responsibilities"].strip().replace("\n", "<br/>"), s_body_m))
                main_items.append(Spacer(1, 3))

        if st.session_state.projects:
            main_items += sec_m("Projects")
            for p in st.session_state.projects:
                main_items.append(Paragraph(f'<b>{p["title"]}</b>', s_role_m))
                if p["tech"]:
                    main_items.append(Paragraph(f'[{p["tech"]}]', s_co_m))
                if p["description"].strip():
                    main_items.append(Paragraph(p["description"].strip(), s_body_m))
                main_items.append(Spacer(1, 3))

        if st.session_state.certifications:
            main_items += sec_m("Certifications")
            for c in st.session_state.certifications:
                main_items.append(Paragraph(f'• <b>{c["name"]}</b>  ({c["type"]})', s_body_m))

        # Render each column into a frame-based table
        from reportlab.platypus import Frame, PageTemplate, BaseDocTemplate
        from reportlab.platypus import FrameBreak

        # Use Table for two-column layout
        from reportlab.platypus import KeepInFrame

        sidebar_frame = KeepInFrame(
            SIDE_W - 2*PAD, PAGE_H - 2*PAD,
            sidebar_items,
            mode='shrink'
        )
        main_frame = KeepInFrame(
            MAIN_W - 2*PAD, PAGE_H - 2*PAD,
            main_items,
            mode='shrink'
        )

        table_data = [[sidebar_frame, main_frame]]
        table = Table(
            table_data,
            colWidths=[SIDE_W, MAIN_W],
            rowHeights=[PAGE_H]
        )
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, 0), DARK_NAVY),
            ('BACKGROUND', (1, 0), (1, 0), colors.white),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING',  (0, 0), (0, 0), PAD),
            ('RIGHTPADDING', (0, 0), (0, 0), PAD),
            ('LEFTPADDING',  (1, 0), (1, 0), PAD),
            ('RIGHTPADDING', (1, 0), (1, 0), PAD),
            ('TOPPADDING',   (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING',(0, 0), (-1, -1), 0),
        ]))

        doc.build([table])
        buf.seek(0)
        return buf.getvalue()

    def make_pdf_minimal_pro():
        """Clean serif-style PDF with red accent — Minimal Pro."""
        buf = io.BytesIO()
        doc = SimpleDocTemplate(
            buf, pagesize=A4,
            leftMargin=2*cm, rightMargin=2*cm,
            topMargin=2*cm, bottomMargin=2*cm
        )

        RED    = colors.HexColor('#c0392b')
        BLACK  = colors.HexColor('#111111')
        DARK   = colors.HexColor('#333333')
        MID    = colors.HexColor('#555555')
        LIGHT  = colors.HexColor('#eeeeee')

        s_name = ParagraphStyle(
            'mpname', fontName='Times-Bold', fontSize=22,
            textColor=BLACK, spaceAfter=2, leading=26
        )
        s_degree_h = ParagraphStyle(
            'mpdeg', fontName='Times-Italic', fontSize=11,
            textColor=RED, spaceAfter=4, leading=14
        )
        s_contact = ParagraphStyle(
            'mpcont', fontName='Helvetica', fontSize=8,
            textColor=MID, spaceAfter=0, leading=12
        )
        s_section = ParagraphStyle(
            'mpsec', fontName='Helvetica-Bold', fontSize=7,
            textColor=RED, spaceBefore=12, spaceAfter=2,
            leading=9, letterSpacing=3
        )
        s_item_title = ParagraphStyle(
            'mpititle', fontName='Times-Bold', fontSize=11,
            textColor=BLACK, spaceAfter=1, leading=14
        )
        s_item_sub = ParagraphStyle(
            'mpisub', fontName='Helvetica', fontSize=8,
            textColor=MID, spaceAfter=2, leading=11
        )
        s_item_co = ParagraphStyle(
            'mpico', fontName='Helvetica-Oblique', fontSize=8.5,
            textColor=RED, spaceAfter=1, leading=12
        )
        s_body = ParagraphStyle(
            'mpbody', fontName='Times-Roman', fontSize=9.5,
            textColor=DARK, spaceAfter=4, leading=14
        )
        s_skills = ParagraphStyle(
            'mpskills', fontName='Helvetica', fontSize=9,
            textColor=DARK, spaceAfter=4, leading=14
        )

        story = []

        # Header with left red bar (approximated via bold name + underline)
        story.append(Paragraph(st.session_state.full_name or "Your Name", s_name))
        if st.session_state.degree:
            story.append(Paragraph(st.session_state.degree, s_degree_h))

        contact_parts = list(filter(None, [
            st.session_state.email, st.session_state.phone,
            st.session_state.linkedin, st.session_state.github,
            st.session_state.address
        ]))
        if contact_parts:
            story.append(Paragraph("  ·  ".join(contact_parts), s_contact))

        story.append(Spacer(1, 4))
        story.append(HRFlowable(width="100%", thickness=1.5, color=RED, spaceAfter=0, spaceBefore=0))
        story.append(Spacer(1, 4))

        def sec_mp(title):
            story.append(Paragraph(title.upper(), s_section))
            story.append(HRFlowable(width="100%", thickness=0.5, color=LIGHT, spaceAfter=4, spaceBefore=1))

        if st.session_state.career_objective or st.session_state.summary:
            sec_mp("Profile")
            txt = st.session_state.career_objective or st.session_state.summary
            story.append(Paragraph(f'<i>{txt.strip()}</i>', s_body))

        if st.session_state.degree or st.session_state.college:
            sec_mp("Education")
            story.append(Paragraph(st.session_state.degree or "", s_item_title))
            edu_sub = " · ".join(filter(None, [st.session_state.college, st.session_state.grad_year, st.session_state.cgpa]))
            if edu_sub:
                story.append(Paragraph(edu_sub, s_item_sub))

        if st.session_state.skills:
            sec_mp("Skills")
            story.append(Paragraph("  ·  ".join(st.session_state.skills), s_skills))

        if st.session_state.experiences:
            sec_mp("Experience")
            for e in st.session_state.experiences:
                block = []
                block.append(Paragraph(f'<b>{e["role"]}</b>', s_item_title))
                block.append(Paragraph(e["company"], s_item_co))
                if e["duration"]:
                    block.append(Paragraph(e["duration"], s_item_sub))
                if e["responsibilities"].strip():
                    block.append(Paragraph(e["responsibilities"].strip().replace("\n", "<br/>"), s_body))
                block.append(Spacer(1, 3))
                story.extend(block)

        if st.session_state.projects:
            sec_mp("Projects")
            for p in st.session_state.projects:
                block = []
                block.append(Paragraph(f'<b>{p["title"]}</b>', s_item_title))
                if p["tech"]:
                    block.append(Paragraph(f'Tech: {p["tech"]}', s_item_co))
                if p["description"].strip():
                    block.append(Paragraph(p["description"].strip(), s_body))
                block.append(Spacer(1, 3))
                story.extend(block)

        if st.session_state.certifications:
            sec_mp("Certifications & Achievements")
            for c in st.session_state.certifications:
                story.append(Paragraph(f'• <b>{c["name"]}</b>  ({c["type"]})', s_body))

        if st.session_state.languages:
            sec_mp("Languages")
            story.append(Paragraph("  ·  ".join(st.session_state.languages), s_skills))

        if st.session_state.hobbies:
            sec_mp("Hobbies & Interests")
            story.append(Paragraph("  ·  ".join(st.session_state.hobbies), s_skills))

        doc.build(story)
        buf.seek(0)
        return buf.getvalue()

    # ── Download section — PDF + HTML for every template ─────────────────────
    st.markdown(
        '<div class="card-dark"><div class="sl-dark">⬇️ DOWNLOAD YOUR RESUME</div>',
        unsafe_allow_html=True
    )
    fname = st.session_state.full_name.replace(" ", "_") if st.session_state.full_name else "resume"
    tname = st.session_state.template.replace(" ", "_").lower()

    # Route PDF generation to the correct template renderer
    _t = st.session_state.template
    if _t == "Creative Sidebar":
        pdf_bytes = make_pdf_creative_sidebar()
        pdf_label = "📄 Download as PDF — Creative Sidebar layout"
    elif _t == "Minimal Pro":
        pdf_bytes = make_pdf_minimal_pro()
        pdf_label = "📄 Download as PDF — Minimal Pro layout"
    else:
        # ATS Clean AND Modern Dark both use the existing make_pdf()
        pdf_bytes = make_pdf()
        if _t == "Modern Dark":
            pdf_label = "📄 Download as PDF — Modern Dark layout (ATS-compatible)"
        else:
            pdf_label = "📄 Download as PDF (ATS Clean layout — best for job applications)"

    st.download_button(
        label=pdf_label,
        data=pdf_bytes,
        file_name=f"{fname}_{tname}_resume.pdf",
        mime="application/pdf",
        use_container_width=True,
        key="dl_pdf_main"
    )

    st.markdown(
        '<div style="font-size:11px;color:#888888;margin:8px 0 4px 0;'
        'text-transform:uppercase;letter-spacing:1px;font-weight:600;">'
        '— or download as styled HTML (keeps template colors &amp; layout) —</div>',
        unsafe_allow_html=True
    )

    html_full = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{st.session_state.full_name or 'Resume'} — {st.session_state.template}</title>
<style>
  body {{ margin: 0; padding: 20px; background: #f4f4f4; font-family: Arial, sans-serif; }}
  .wrapper {{ max-width: 820px; margin: 0 auto; }}
</style>
</head>
<body>
<div class="wrapper">
{html}
</div>
</body>
</html>"""

    st.download_button(
        label=f"🎨 Download as HTML — {st.session_state.template} Template",
        data=html_full.encode("utf-8"),
        file_name=f"{fname}_{tname}_resume.html",
        mime="text/html",
        use_container_width=True,
        key="dl_html_template"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Completeness meter ────────────────────────────────────────────────────
    filled = sum([
        bool(st.session_state.full_name),
        bool(st.session_state.email),
        bool(st.session_state.career_objective or st.session_state.summary),
        bool(st.session_state.skills),
        bool(st.session_state.experiences),
        bool(st.session_state.projects),
        bool(st.session_state.degree),
    ])
    pct = int(filled / 7 * 100)
    st.markdown(f"""
    <div class="card-green" style="margin-top:16px;">
        <div class="sl-green">RESUME COMPLETENESS</div>
        <div style="font-size:44px;font-weight:700;color:#111111;font-family:'Space Mono',monospace;line-height:1;">{pct}%</div>
        <div style="background:#111111;border-radius:20px;height:6px;margin:10px 0 12px;">
            <div style="background:#ffffff;border-radius:20px;height:6px;width:{pct}%;"></div>
        </div>
        <div style="font-size:13px;font-weight:700;color:#111111;">
            ⚡ {len(st.session_state.skills)} Skills &nbsp;·&nbsp;
            💼 {len(st.session_state.experiences)} Experience &nbsp;·&nbsp;
            🚀 {len(st.session_state.projects)} Projects
        </div>
    </div>""", unsafe_allow_html=True)
