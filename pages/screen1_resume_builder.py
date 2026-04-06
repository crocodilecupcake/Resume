import streamlit as st
import random, io, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from shared_css import SHARED_CSS
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, HRFlowable
from reportlab.lib.units import cm

st.set_page_config(page_title="Resume Builder", page_icon="📝", layout="wide")
st.markdown(SHARED_CSS, unsafe_allow_html=True)

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
        degree=degree or "Engineering", college=college or "a reputed institution", top3=top3)

DEFAULTS = {
    "full_name":"","email":"","phone":"","linkedin":"","github":"","address":"",
    "degree":"","college":"","grad_year":"","cgpa":"",
    "summary":"","skills":[],"experiences":[],"projects":[],"certifications":[],
    "template":"ATS Clean",
}
for k,v in DEFAULTS.items():
    if k not in st.session_state: st.session_state[k] = v

# ── Nav ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="nav-bar">
  <div class="nav-title">📝 Resume Builder</div>
  <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;">
    <div class="nav-badge">Module 1 / 3</div>
    <div style="color:#888888;font-size:12px;">Free · No API</div>
  </div>
</div>""", unsafe_allow_html=True)

if st.button("← Home", key="home_btn"):
    st.switch_page("app.py")

st.markdown("<br>", unsafe_allow_html=True)
left, right = st.columns([1,1], gap="large")

# ════════ FORM ════════
with left:

    # Personal
    st.markdown('<div class="card"><div class="sl">01 — Personal Information</div>', unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    st.session_state.full_name = c1.text_input("Full Name",   st.session_state.full_name, placeholder="Yash Sharma")
    st.session_state.email     = c2.text_input("Email",       st.session_state.email,     placeholder="yash@email.com")
    c3,c4 = st.columns(2)
    st.session_state.phone     = c3.text_input("Phone",       st.session_state.phone,     placeholder="+91 9876543210")
    st.session_state.address   = c4.text_input("City",        st.session_state.address,   placeholder="Nashik, India")
    c5,c6 = st.columns(2)
    st.session_state.linkedin  = c5.text_input("LinkedIn",    st.session_state.linkedin,  placeholder="linkedin.com/in/yash")
    st.session_state.github    = c6.text_input("GitHub",      st.session_state.github,    placeholder="github.com/yash")
    st.markdown('</div>', unsafe_allow_html=True)

    # Education
    st.markdown('<div class="card"><div class="sl">02 — Education</div>', unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    st.session_state.degree    = c1.text_input("Degree",          st.session_state.degree,    placeholder="B.E. Computer Engineering")
    st.session_state.college   = c2.text_input("College",         st.session_state.college,   placeholder="XYZ University")
    c3,c4 = st.columns(2)
    st.session_state.grad_year = c3.text_input("Graduation Year", st.session_state.grad_year, placeholder="2025")
    st.session_state.cgpa      = c4.text_input("CGPA / %",        st.session_state.cgpa,      placeholder="8.5 / 10")
    st.markdown('</div>', unsafe_allow_html=True)

    # Summary
    st.markdown('<div class="card"><div class="sl">03 — Professional Summary</div>', unsafe_allow_html=True)
    st.session_state.summary = st.text_area(
        "Summary", st.session_state.summary,
        placeholder="Write your summary or hit Generate below...", height=100)
    if st.button("✨ Auto-Generate Summary (AI Style)", use_container_width=True):
        st.session_state.summary = gen_summary(st.session_state.degree, st.session_state.college, st.session_state.skills)
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Skills
    ALL_SKILLS = [
        "Python","JavaScript","React","Node.js","SQL","Machine Learning","Deep Learning",
        "TensorFlow","Docker","AWS","Git","Java","C++","FastAPI","MongoDB","PostgreSQL",
        "Pandas","NumPy","Scikit-learn","Flutter","Kotlin","REST APIs","TypeScript",
        "Next.js","HTML","CSS","Figma","Power BI","Excel","R","NLP","Computer Vision",
        "PyTorch","Spark","Kubernetes","Redis","GraphQL","Go","Rust","Unity"
    ]
    st.markdown('<div class="card"><div class="sl">04 — Skills</div>', unsafe_allow_html=True)
    rem = [s for s in ALL_SKILLS if s not in st.session_state.skills]
    sc1,sc2 = st.columns([3,1])
    new_sk = sc1.selectbox("Pick a skill", ["Select..."]+rem, key="sk_sel")
    if sc2.button("Add", key="add_sk"):
        if new_sk != "Select..." and new_sk not in st.session_state.skills:
            st.session_state.skills.append(new_sk); st.rerun()
    custom = st.text_input("Or type a custom skill", placeholder="e.g. LangChain, Figma...", key="csk_in")
    if st.button("Add Custom Skill", key="csk_btn"):
        if custom and custom not in st.session_state.skills:
            st.session_state.skills.append(custom); st.rerun()
    if st.session_state.skills:
        st.markdown("".join([f'<span class="skill-tag">{s}</span>' for s in st.session_state.skills])+"<div style='margin-top:8px;'></div>", unsafe_allow_html=True)
        rm = st.selectbox("Remove a skill", ["Select to remove..."]+st.session_state.skills, key="rm_sk")
        if st.button("Remove Selected", key="rm_sk_btn"):
            if rm in st.session_state.skills:
                st.session_state.skills.remove(rm); st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Experience
    st.markdown('<div class="card"><div class="sl">05 — Work Experience</div>', unsafe_allow_html=True)
    with st.expander("➕ Add Experience"):
        ec1,ec2 = st.columns(2)
        e_co   = ec1.text_input("Company",  key="e_co",   placeholder="Google")
        e_role = ec2.text_input("Role",     key="e_role", placeholder="SDE Intern")
        e_dur  = st.text_input("Duration",  key="e_dur",  placeholder="June 2024 – Aug 2024")
        e_resp = st.text_area("Responsibilities", key="e_resp",
                              placeholder="• Built REST APIs\n• Improved DB speed by 30%", height=80)
        if st.button("Save Experience", key="save_exp"):
            if e_co and e_role:
                st.session_state.experiences.append({"company":e_co,"role":e_role,"duration":e_dur,"responsibilities":e_resp})
                st.rerun()
    for i,exp in enumerate(st.session_state.experiences):
        st.markdown(f'<div class="item-row"><strong>{exp["role"]}</strong> @ {exp["company"]}<div class="item-sub">{exp["duration"]}</div></div>', unsafe_allow_html=True)
        if st.button("Remove", key=f"rm_exp_{i}"):
            st.session_state.experiences.pop(i); st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Projects
    st.markdown('<div class="card"><div class="sl">06 — Projects</div>', unsafe_allow_html=True)
    with st.expander("➕ Add Project"):
        pt = st.text_input("Project Title", key="pt", placeholder="AI Chatbot")
        pd2 = st.text_area("Description",  key="pd2",placeholder="Built using Python + Streamlit...", height=70)
        ps = st.text_input("Tech Stack",   key="ps", placeholder="Python, Streamlit, NLP")
        if st.button("Save Project", key="save_proj"):
            if pt:
                st.session_state.projects.append({"title":pt,"description":pd2,"tech":ps}); st.rerun()
    for i,proj in enumerate(st.session_state.projects):
        st.markdown(f'<div class="item-row"><strong>{proj["title"]}</strong><div class="item-sub" style="font-family:monospace;">{proj["tech"]}</div></div>', unsafe_allow_html=True)
        if st.button("Remove", key=f"rm_proj_{i}"):
            st.session_state.projects.pop(i); st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Certs
    st.markdown('<div class="card"><div class="sl">07 — Certifications & Achievements</div>', unsafe_allow_html=True)
    with st.expander("➕ Add Certification / Award"):
        cn = st.text_input("Name", key="cn", placeholder="AWS Cloud Practitioner")
        ct = st.selectbox("Type", ["Certification","Hackathon","Award","Other"], key="ct")
        if st.button("Save", key="save_cert"):
            if cn:
                st.session_state.certifications.append({"name":cn,"type":ct}); st.rerun()
    for i,cert in enumerate(st.session_state.certifications):
        st.markdown(f'<div class="item-row">🏆 <strong>{cert["name"]}</strong><div class="item-sub">{cert["type"]}</div></div>', unsafe_allow_html=True)
        if st.button("Remove", key=f"rm_cert_{i}"):
            st.session_state.certifications.pop(i); st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ════════ PREVIEW ════════
with right:

    st.markdown("""
    <style>
    div[data-testid="stRadio"] label p {
        color: red !important;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown('<div class="card-dark"><div class="sl-dark">🎨 CHOOSE TEMPLATE</div>', unsafe_allow_html=True)
    template = st.radio("", ["ATS Clean","Modern Dark"], horizontal=True, key="tmpl_radio", label_visibility="collapsed")
    st.session_state.template = template
    st.markdown('</div>', unsafe_allow_html=True)

    dark = (template == "Modern Dark")
    BG  = "#111111" if dark else "#ffffff"
    TC  = "#ffffff" if dark else "#111111"
    SC  = "#cccccc" if dark else "#333333"
    BRD = "#2a2a2a" if dark else "#f0f2ee"
    AC  = "#6aef8a"

    def sec(t):
        return (f'<div style="font-size:10px;letter-spacing:2px;font-weight:700;text-transform:uppercase;'
                f'background:{BRD};color:{AC if dark else "#111111"};padding:4px 10px;'
                f'border-radius:6px;margin:14px 0 8px 0;">{t}</div>')

    contacts = " | ".join(filter(None,[st.session_state.email,st.session_state.phone,
                                       st.session_state.linkedin,st.session_state.github,
                                       st.session_state.address]))
    html  = f'<div style="background:{BG};border-radius:20px;padding:28px;min-height:560px;box-shadow:0 4px 24px rgba(0,0,0,0.1);">'
    html += f'<div style="border-bottom:3px solid {AC};padding-bottom:10px;margin-bottom:8px;">'
    html += f'<div style="font-size:24px;font-weight:700;color:{TC};">{st.session_state.full_name or "Your Name"}</div>'
    html += f'<div style="font-size:11px;color:{SC};margin-top:4px;">{contacts or "email | phone | linkedin | github"}</div></div>'

    if st.session_state.summary:
        html += sec("Summary")
        html += f'<div style="font-size:12px;color:{SC};line-height:1.7;">{st.session_state.summary}</div>'
    if st.session_state.degree or st.session_state.college:
        html += sec("Education")
        html += f'<div style="font-weight:700;font-size:13px;color:{TC};">{st.session_state.degree or "Degree"}</div>'
        html += f'<div style="font-size:11px;color:{SC};margin-top:2px;">{st.session_state.college} | {st.session_state.grad_year} | {st.session_state.cgpa}</div>'
    if st.session_state.skills:
        html += sec("Skills")
        html += "".join([f'<span style="display:inline-block;background:{"#222" if dark else "#111"};color:{AC};border-radius:20px;padding:2px 10px;font-size:10px;font-weight:700;margin:2px;font-family:monospace;">{s}</span>' for s in st.session_state.skills])
    if st.session_state.experiences:
        html += sec("Work Experience")
        for e in st.session_state.experiences:
            html += f'<div style="margin-bottom:10px;"><div style="font-weight:700;font-size:13px;color:{TC};">{e["role"]}</div>'
            html += f'<div style="font-size:11px;color:{SC};">{e["company"]} | {e["duration"]}</div>'
            html += f'<div style="font-size:11px;color:{SC};margin-top:3px;line-height:1.5;">{e["responsibilities"].replace(chr(10),"<br>")}</div></div>'
    if st.session_state.projects:
        html += sec("Projects")
        for p in st.session_state.projects:
            html += f'<div style="margin-bottom:10px;"><div style="font-weight:700;font-size:13px;color:{TC};">{p["title"]}</div>'
            html += f'<div style="font-size:10px;color:{AC};font-family:monospace;">{p["tech"]}</div>'
            html += f'<div style="font-size:11px;color:{SC};margin-top:2px;">{p["description"]}</div></div>'
    if st.session_state.certifications:
        html += sec("Certifications & Achievements")
        html += f'<div style="font-size:12px;color:{SC};">'+" &nbsp;·&nbsp; ".join([f'🏆 {c["name"]}' for c in st.session_state.certifications])+'</div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    def make_pdf():
        buf = io.BytesIO()
        doc = SimpleDocTemplate(buf,pagesize=A4,leftMargin=2*cm,rightMargin=2*cm,topMargin=2*cm,bottomMargin=2*cm)
        sn  = ParagraphStyle('n', fontName='Helvetica-Bold',fontSize=22,textColor=colors.HexColor('#111111'),spaceAfter=4)
        sc2 = ParagraphStyle('c', fontName='Helvetica',fontSize=9,textColor=colors.HexColor('#444444'),spaceAfter=10)
        sh  = ParagraphStyle('h', fontName='Helvetica-Bold',fontSize=9,textColor=colors.HexColor('#111111'),spaceBefore=12,spaceAfter=5,backColor=colors.HexColor('#f0f2ee'),leftIndent=4,borderPadding=3)
        st2 = ParagraphStyle('t', fontName='Helvetica-Bold',fontSize=12,textColor=colors.HexColor('#111111'),spaceAfter=2)
        ss  = ParagraphStyle('s', fontName='Helvetica',fontSize=9,textColor=colors.HexColor('#444444'),spaceAfter=3)
        sb  = ParagraphStyle('b', fontName='Helvetica',fontSize=10,textColor=colors.HexColor('#222222'),spaceAfter=4,leading=14)
        story = []
        story.append(Paragraph(st.session_state.full_name or "Your Name", sn))
        pts = list(filter(None,[st.session_state.email,st.session_state.phone,st.session_state.linkedin,st.session_state.github,st.session_state.address]))
        story.append(Paragraph(" | ".join(pts), sc2))
        story.append(HRFlowable(width="100%",thickness=2,color=colors.HexColor('#6aef8a')))
        if st.session_state.summary:
            story.append(Paragraph("PROFESSIONAL SUMMARY",sh)); story.append(Paragraph(st.session_state.summary,sb))
        if st.session_state.degree:
            story.append(Paragraph("EDUCATION",sh)); story.append(Paragraph(st.session_state.degree,st2))
            story.append(Paragraph(f"{st.session_state.college} | {st.session_state.grad_year} | {st.session_state.cgpa}",ss))
        if st.session_state.skills:
            story.append(Paragraph("SKILLS",sh)); story.append(Paragraph(" | ".join(st.session_state.skills),sb))
        if st.session_state.experiences:
            story.append(Paragraph("WORK EXPERIENCE",sh))
            for e in st.session_state.experiences:
                story.append(Paragraph(e["role"],st2)); story.append(Paragraph(f"{e['company']} | {e['duration']}",ss))
                story.append(Paragraph(e["responsibilities"].replace("\n","<br/>"),sb))
        if st.session_state.projects:
            story.append(Paragraph("PROJECTS",sh))
            for p in st.session_state.projects:
                story.append(Paragraph(p["title"],st2)); story.append(Paragraph(f"Tech: {p['tech']}",ss))
                story.append(Paragraph(p["description"],sb))
        if st.session_state.certifications:
            story.append(Paragraph("CERTIFICATIONS & ACHIEVEMENTS",sh))
            for c in st.session_state.certifications: story.append(Paragraph(f"• {c['name']} ({c['type']})",sb))
        doc.build(story); buf.seek(0); return buf.getvalue()

    if st.button("⬇️ Download Resume as PDF", use_container_width=True):
        pdf = make_pdf()
        st.download_button("📄 Save PDF Now", pdf,
            f"{st.session_state.full_name or 'resume'}_resume.pdf","application/pdf",use_container_width=True)

    filled = sum([bool(st.session_state.full_name),bool(st.session_state.email),bool(st.session_state.summary),
                  bool(st.session_state.skills),bool(st.session_state.experiences),
                  bool(st.session_state.projects),bool(st.session_state.degree)])
    pct = int(filled/7*100)
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
