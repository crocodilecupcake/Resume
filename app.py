import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from shared_css import SHARED_CSS

st.set_page_config(page_title="AI Resume System", page_icon="📰", layout="wide", initial_sidebar_state="collapsed")

st.markdown(SHARED_CSS, unsafe_allow_html=True)

st.markdown("""
<style>
/* ── HOME PAGE EXTRAS ── */
.hero {
    background: #111111;
    border-radius: 20px;
    padding: 36px 28px;
    margin-bottom: 20px;
    position: relative;
    overflow: hidden;
}
@media (min-width: 768px) {
    .hero { border-radius: 24px; padding: 56px 48px; margin-bottom: 24px; }
}
.hero::before {
    content:''; position:absolute; top:-80px; right:-80px;
    width:300px; height:300px;
    background:radial-gradient(circle,#6aef8a33 0%,transparent 70%);
    border-radius:50%; pointer-events:none;
}
.hero::after {
    content:''; position:absolute; bottom:-60px; left:20%;
    width:220px; height:220px;
    background:radial-gradient(circle,#c4b5fd22 0%,transparent 70%);
    border-radius:50%; pointer-events:none;
}
.hero-badge {
    display:inline-block; background:#6aef8a; color:#111111;
    border-radius:20px; padding:5px 16px; font-size:12px;
    font-weight:700; letter-spacing:1px; text-transform:uppercase; margin-bottom:16px;
}
.hero-title {
    font-size:36px; font-weight:800; color:#ffffff;
    line-height:1.1; letter-spacing:-1px; margin-bottom:14px;
}
@media (min-width: 768px) { .hero-title { font-size:52px; letter-spacing:-1.5px; } }
.hero-title span { color:#6aef8a; }
.hero-subtitle { font-size:15px; color:#cccccc; max-width:580px; line-height:1.7; margin-bottom:28px; }
@media (min-width: 768px) { .hero-subtitle { font-size:17px; } }
.hero-stats { display:flex; gap:28px; flex-wrap:wrap; }
.stat-num { font-size:28px; font-weight:700; color:#6aef8a; font-family:'Space Mono',monospace; line-height:1; }
@media (min-width: 768px) { .stat-num { font-size:32px; } }
.stat-label { font-size:11px; color:#aaaaaa; font-weight:500; margin-top:4px; }

.module-card {
    border-radius:20px; padding:24px; margin-bottom:14px;
    position:relative; overflow:hidden; min-height:260px;
    transition: transform 0.2s, box-shadow 0.2s;
}
@media (min-width: 768px) { .module-card { padding:28px 24px; min-height:300px; } }
.module-card:hover { transform:translateY(-3px); box-shadow:0 12px 36px rgba(0,0,0,0.12); }
.card-m1 { background:#111111; }
.card-m2 { background:#6aef8a; }
.card-m3 { background:#c4b5fd; }
.module-num { font-family:'Space Mono',monospace; font-size:11px; font-weight:700; letter-spacing:2px; margin-bottom:12px; }
.card-m1 .module-num { color:#555555; }
.card-m2 .module-num { color:#1a6b31; }
.card-m3 .module-num { color:#5b3fa3; }
.module-icon { font-size:34px; margin-bottom:12px; display:block; }
.module-title { font-size:20px; font-weight:700; margin-bottom:8px; line-height:1.2; }
.card-m1 .module-title { color:#ffffff; }
.card-m2 .module-title,.card-m3 .module-title { color:#111111; }
.module-desc { font-size:13px; line-height:1.6; margin-bottom:16px; }
.card-m1 .module-desc { color:#bbbbbb; }
.card-m2 .module-desc { color:#1a5c2a; }
.card-m3 .module-desc { color:#3d2a77; }
.module-features { list-style:none; padding:0; margin:0 0 20px 0; }
.module-features li { font-size:12px; font-weight:600; padding:3px 0; }
.card-m1 .module-features li { color:#dddddd; }
.card-m2 .module-features li { color:#1a5c2a; }
.card-m3 .module-features li { color:#3d2070; }
.card-m1 .module-features li::before { content:'→ '; color:#6aef8a; }
.card-m2 .module-features li::before,.card-m3 .module-features li::before { content:'→ '; color:#111111; }

.how-card { background:#ffffff; border-radius:20px; padding:24px; margin-bottom:14px; box-shadow:0 2px 8px rgba(0,0,0,0.05); }
.step-num { font-family:'Space Mono',monospace; font-size:32px; font-weight:700; color:#eeeeee; line-height:1; margin-bottom:8px; }
.step-title { font-size:15px; font-weight:700; color:#111111; margin-bottom:6px; }
.step-desc { font-size:13px; color:#444444; line-height:1.6; }

.tech-pill { display:inline-block; background:#111111; color:#6aef8a; border-radius:20px; padding:5px 13px; font-size:12px; font-weight:700; margin:3px; font-family:'Space Mono',monospace; }

/* override btn colors for home page module buttons */
.btn-green .stButton > button { background:#6aef8a !important; color:#111111 !important; }
.btn-purple .stButton > button { background:#c4b5fd !important; color:#111111 !important; }
</style>
""", unsafe_allow_html=True)

# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">✦ Free · No API · No Cost</div>
    <div class="hero-title">AI Resume<br><span>Screening & Job</span><br>Recommendation System</div>
    <div class="hero-subtitle">
        Build a job-winning resume, get AI screening feedback, and find jobs
        that actually match your skills — all free, no accounts, no API keys.
    </div>
    <div class="hero-stats">
        <div><div class="stat-num">88</div><div class="stat-label">Job Roles</div></div>
        <div><div class="stat-num">3</div><div class="stat-label">Modules</div></div>
        <div><div class="stat-num">0₹</div><div class="stat-label">Cost</div></div>
        <div><div class="stat-num">ATS</div><div class="stat-label">Compatible</div></div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── MODULE CARDS ──────────────────────────────────────────────────────────────
st.markdown('<div class="sl" style="margin-bottom:14px;">THREE MODULES — PICK WHERE TO START</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3, gap="medium")

with c1:
    st.markdown("""
    <div class="module-card card-m1">
        <div class="module-num">MODULE 01</div>
        <span class="module-icon">📝</span>
        <div class="module-title">Resume Builder</div>
        <div class="module-desc">Fill in your details and watch your resume build live. Download clean PDF instantly.</div>
        <ul class="module-features">
            <li>Live resume preview</li>
            <li>AI-style summary generator</li>
            <li>ATS Clean + Dark templates</li>
            <li>One-click PDF download</li>
            <li>Completeness tracker</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="btn-green">', unsafe_allow_html=True)
    if st.button("Open Resume Builder →", key="btn1"):
        st.switch_page("pages/screen1_resume_builder.py")
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="module-card card-m2">
        <div class="module-num">MODULE 02</div>
        <span class="module-icon">🧠</span>
        <div class="module-title">AI Screening</div>
        <div class="module-desc">Upload any resume and get a score, ATS check, skill extraction, and 5 improvement tips.</div>
        <ul class="module-features">
            <li>Resume score 0–100</li>
            <li>Skill extraction</li>
            <li>ATS compatibility check</li>
            <li>Missing skills detection</li>
            <li>5 actionable suggestions</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open Resume Screening →", key="btn2"):
        st.switch_page("pages/screen2_ai_screening.py")

with c3:
    st.markdown("""
    <div class="module-card card-m3">
        <div class="module-num">MODULE 03</div>
        <span class="module-icon">💼</span>
        <div class="module-title">Job Matcher</div>
        <div class="module-desc">Get matched to 88 real job roles with a % score, skill gap analysis, and learning roadmap.</div>
        <ul class="module-features">
            <li>Match % for each role</li>
            <li>Skill gap analysis</li>
            <li>What to learn next</li>
            <li>Roles by experience level</li>
            <li>Save / bookmark jobs</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="btn-purple">', unsafe_allow_html=True)
    if st.button("Open Job Matcher →", key="btn3"):
        st.switch_page("pages/screen3_job_recommendations.py")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── HOW IT WORKS ─────────────────────────────────────────────────────────────
st.markdown('<div class="sl" style="margin-bottom:14px;">HOW IT WORKS</div>', unsafe_allow_html=True)

h1, h2, h3, h4 = st.columns(4, gap="medium")
steps = [
    ("01","Fill Your Details","Enter your personal info, skills, education, experience and projects in the Resume Builder."),
    ("02","Generate & Download","Auto-generate your professional summary, preview your resume live, download as PDF."),
    ("03","Screen Your Resume","Upload it to Screening — get ATS score, skill gap, and 5 personalized improvement tips."),
    ("04","Find Matching Jobs","Get matched to 88 job roles with % scores, see what skills you're missing, and what to learn next."),
]
for col, (num, title, desc) in zip([h1,h2,h3,h4], steps):
    with col:
        st.markdown(f"""
        <div class="how-card">
            <div class="step-num">{num}</div>
            <div class="step-title">{title}</div>
            <div class="step-desc">{desc}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── BOTTOM ────────────────────────────────────────────────────────────────────
bl, br = st.columns([1.2, 1], gap="large")

with bl:
    st.markdown("""
    <div class="card">
        <div class="sl">BUILT WITH</div>
        <div>
            <span class="tech-pill">Streamlit</span>
            <span class="tech-pill">Python</span>
            <span class="tech-pill">Pandas</span>
            <span class="tech-pill">PyPDF2</span>
            <span class="tech-pill">python-docx</span>
            <span class="tech-pill">ReportLab</span>
            <span class="tech-pill">Rule-Based AI</span>
            <span class="tech-pill">Regex NLP</span>
        </div>
        <div style="margin-top:18px;font-size:13px;color:#333333;line-height:1.8;">
            No OpenAI. No Anthropic. No paid APIs.<br>
            All intelligence is <strong>rule-based logic</strong> — skill matching, scoring formulas,
            template-driven summary generation, and keyword analysis.
            Runs completely offline after install.
        </div>
    </div>
    """, unsafe_allow_html=True)

with br:
    st.markdown("""
    <div class="card-dark">
        <div class="sl-dark">PROJECT HIGHLIGHTS</div>
        <div style="display:flex;flex-direction:column;gap:12px;">
            <div style="display:flex;align-items:flex-start;gap:10px;">
                <div style="width:8px;height:8px;background:#6aef8a;border-radius:50%;flex-shrink:0;margin-top:5px;"></div>
                <div style="font-size:13px;color:#dddddd;">88 job roles matched from real dataset</div>
            </div>
            <div style="display:flex;align-items:flex-start;gap:10px;">
                <div style="width:8px;height:8px;background:#6aef8a;border-radius:50%;flex-shrink:0;margin-top:5px;"></div>
                <div style="font-size:13px;color:#dddddd;">Skill extraction via regex + dictionary scan</div>
            </div>
            <div style="display:flex;align-items:flex-start;gap:10px;">
                <div style="width:8px;height:8px;background:#6aef8a;border-radius:50%;flex-shrink:0;margin-top:5px;"></div>
                <div style="font-size:13px;color:#dddddd;">ATS score from 8-factor rule formula</div>
            </div>
            <div style="display:flex;align-items:flex-start;gap:10px;">
                <div style="width:8px;height:8px;background:#6aef8a;border-radius:50%;flex-shrink:0;margin-top:5px;"></div>
                <div style="font-size:13px;color:#dddddd;">PDF generation with ReportLab</div>
            </div>
            <div style="display:flex;align-items:flex-start;gap:10px;">
                <div style="width:8px;height:8px;background:#c4b5fd;border-radius:50%;flex-shrink:0;margin-top:5px;"></div>
                <div style="font-size:13px;color:#dddddd;">Supports PDF, DOCX and TXT resumes</div>
            </div>
            <div style="display:flex;align-items:flex-start;gap:10px;">
                <div style="width:8px;height:8px;background:#c4b5fd;border-radius:50%;flex-shrink:0;margin-top:5px;"></div>
                <div style="font-size:13px;color:#dddddd;">Fully free — no keys, no accounts, no limits</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
