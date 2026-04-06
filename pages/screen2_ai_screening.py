import streamlit as st
import PyPDF2, docx, io, re, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from shared_css import SHARED_CSS

st.set_page_config(page_title="AI Resume Screening", page_icon="🤖", layout="wide")
st.markdown(SHARED_CSS, unsafe_allow_html=True)

KNOWN_SKILLS = [
    "python","javascript","react","node.js","sql","machine learning","deep learning",
    "tensorflow","pytorch","docker","aws","git","java","c++","c","fastapi","mongodb",
    "postgresql","pandas","numpy","scikit-learn","flutter","kotlin","rest api","typescript",
    "next.js","html","css","figma","power bi","excel","r","nlp","computer vision",
    "spark","kubernetes","redis","graphql","go","rust","unity","azure","gcp",
    "selenium","tableau","hadoop","scala","flask","django","firebase","swift","xcode",
    "linux","bash","networking","blockchain","solidity","opencv","mlops","etl",
    "data analysis","statistics","oop","algorithms","data structures","agile","scrum",
    "communication","leadership","problem solving","debugging","ui design","wireframing",
    "prototyping","testing","automation","ci/cd","cryptography","penetration testing",
    "ethical hacking","cybersecurity"
]
IMPORTANT = ["python","machine learning","sql","docker","git","aws","tensorflow","pytorch",
             "react","javascript","deep learning","kubernetes","nlp","computer vision","mlops"]
QUALITY_KW = ["improved","reduced","built","developed","designed","achieved","increased",
              "optimized","automated","deployed","implemented","managed","led","created",
              "launched","delivered","analysed","researched","scaled","%","award","winner",
              "rank","certification","published"]
ATS_KW = ["python","java","sql","machine learning","data analysis","api","cloud","agile",
          "docker","git","testing","communication","leadership","problem solving",
          "algorithms","deep learning","nlp","automation","ci/cd","kubernetes"]
SUGG_POOL = [
    "Add measurable achievements with numbers (e.g., 'improved API response time by 40%').",
    "Include a strong, keyword-rich Professional Summary at the top of your resume.",
    "List your tech stack explicitly — avoid vague terms like 'familiar with'.",
    "Use consistent date formatting (e.g., Jan 2024 – May 2024) throughout.",
    "Add GitHub or portfolio links to make your projects verifiable.",
    "Quantify project impact — users served, accuracy achieved, time saved.",
    "Avoid tables, images, and special characters — they break ATS parsers.",
    "Keep resume to 1 page if you have under 3 years of experience.",
    "Use strong action verbs: Built, Deployed, Optimized, Designed, Automated.",
    "Include certifications — even free ones from Coursera or Google count.",
    "Avoid first-person language (I, my, we) — use implied subject style.",
    "Include your CGPA if it is above 7.5 — it helps in campus placements.",
    "Tailor your resume keywords to match the specific job description.",
    "List internships and projects in separate sections for better clarity.",
]

def extract_text(f):
    nm = f.name.lower()
    if nm.endswith(".pdf"):
        try:
            r = PyPDF2.PdfReader(io.BytesIO(f.read()))
            return " ".join(p.extract_text() or "" for p in r.pages)
        except: return ""
    elif nm.endswith(".docx"):
        try:
            d = docx.Document(io.BytesIO(f.read()))
            return " ".join(p.text for p in d.paragraphs)
        except: return ""
    return f.read().decode("utf-8", errors="ignore")

def analyze(text, jd=""):
    tl    = text.lower()
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    name  = "Unknown"
    for line in lines[:5]:
        words = line.split()
        if 1 < len(words) <= 5 and all(w[0].isupper() for w in words if w.isalpha()):
            name = line; break
    emails = re.findall(r"[\w.\-]+@[\w.\-]+\.[a-z]{2,}", text)
    email  = emails[0] if emails else "—"
    phones = re.findall(r"[\+\(]?[0-9][0-9\s\-\(\)]{8,}[0-9]", text)
    phone  = phones[0].strip() if phones else "—"
    detected = [s for s in KNOWN_SKILLS if s in tl]
    missing  = [s for s in IMPORTANT if s not in tl][:6]
    edu_kw   = ["b.e","b.tech","m.tech","bsc","msc","bachelor","master","engineering","university","college","cgpa"]
    edu_lines = [l.strip() for l in lines if any(k in l.lower() for k in edu_kw)]
    education = edu_lines[0] if edu_lines else "Not detected"
    exp_pat   = re.findall(r"(\d+)\s*(year|yr|months?)", tl)
    exp_yrs   = round(min(sum(int(v)/12 if "month" in u else int(v) for v,u in exp_pat), 15), 1)

    has_summary    = any(k in tl for k in ["summary","objective","profile","about"])
    has_skills     = any(k in tl for k in ["skills","technologies","tools","stack"])
    has_experience = any(k in tl for k in ["experience","internship","work","employment"])
    has_projects   = any(k in tl for k in ["project","built","developed","created"])
    has_education  = any(k in tl for k in ["education","university","college","b.e","b.tech"])
    has_certs      = any(k in tl for k in ["certification","certified","course","hackathon","award"])
    has_contact    = email != "—" or phone != "—"
    has_links      = any(k in tl for k in ["github","linkedin","portfolio"])
    wc             = len(text.split())

    fmt = min(100, 40 + 10*has_summary + 10*has_skills + 10*has_contact + 10*has_links + 10*has_education + 10*has_certs)
    if wc < 150: fmt = max(20, fmt-20)
    elif wc > 900: fmt = max(50, fmt-10)

    skills_sc    = min(100, 30 + len(detected)*5)
    quality_hits = sum(1 for k in QUALITY_KW if k in tl)
    exp_sc       = min(100, max(20 if not has_experience else 0, 30 + quality_hits*7) - (30 if not has_experience else 0))

    if jd:
        jd_w = set(re.findall(r'\b\w+\b', jd.lower()))
        rs_w = set(re.findall(r'\b\w+\b', tl))
        com  = jd_w & rs_w
        kw_sc  = min(100, int(len(com)/max(len(jd_w),1)*200))
        kw_pct = min(100, int(len(com)/max(len(jd_w),1)*150))
    else:
        ah = sum(1 for k in ATS_KW if k in tl)
        kw_sc  = min(100, 30 + ah*5)
        kw_pct = min(100, 20 + ah*5)

    overall = int(0.25*fmt + 0.30*skills_sc + 0.25*exp_sc + 0.20*kw_sc)
    ats = min(100, 40 + 15*has_skills + 10*has_contact + 10*(has_experience or has_projects) + 10*(wc>200) + 15*(kw_pct>40))

    sugs = []
    if not has_summary:    sugs.append("Add a Professional Summary — it's the first thing recruiters read.")
    if quality_hits < 3:   sugs.append("Add measurable achievements with numbers (e.g., improved speed by 40%).")
    if len(detected) < 5:  sugs.append("List more technical skills explicitly — recruiters scan for keywords.")
    if not has_links:      sugs.append("Add your GitHub and LinkedIn — it significantly boosts credibility.")
    if not has_certs:      sugs.append("Add certifications or courses (Coursera, Google, AWS) to stand out.")
    if wc < 200:           sugs.append("Your resume is too short — expand projects and experience sections.")
    if ats < 60:           sugs.append("Avoid tables and multi-column layouts — they confuse ATS parsers.")
    pool = SUGG_POOL[:]
    random.shuffle(pool)
    for s in pool:
        if s not in sugs and len(sugs) < 5: sugs.append(s)

    return {"name":name,"email":email,"phone":phone,"education":education,"exp_yrs":exp_yrs,
            "overall":overall,"fmt":fmt,"skills_sc":skills_sc,"exp_sc":exp_sc,
            "kw_sc":kw_sc,"ats":ats,"kw_pct":kw_pct,"detected":detected,"missing":missing,"sugs":sugs[:5]}

if "result" not in st.session_state: st.session_state.result = None

# ── Nav ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="nav-bar">
  <div class="nav-title">🤖 AI Resume Screening</div>
  <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;">
    <div class="nav-badge-purple">Module 2 / 3</div>
    <div style="color:#888888;font-size:12px;">Free · No API</div>
  </div>
</div>""", unsafe_allow_html=True)
if st.button("← Home", key="home_btn"):
    st.switch_page("app.py")
st.markdown("<br>", unsafe_allow_html=True)

left, right = st.columns([1, 1.15], gap="large")

# ════════ LEFT ════════
with left:
    st.markdown('<div class="card"><div class="sl">01 — Upload Resume</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload resume (PDF / DOCX / TXT)", type=["pdf","docx","txt"], label_visibility="collapsed")
    jd = st.text_area("Job Description (optional — improves keyword scoring)",
                       placeholder="Paste the job description here to get targeted analysis...",
                       height=110, key="jd_in")
    if uploaded:
        st.markdown(f'<div style="background:#f0f0f0;border-radius:12px;padding:12px 14px;font-size:13px;color:#111111;font-weight:600;margin-top:8px;">📄 {uploaded.name} — ready</div>', unsafe_allow_html=True)
    go = st.button("🔍 Analyze Resume", use_container_width=True, disabled=uploaded is None)
    if go and uploaded:
        with st.spinner("Analyzing..."):
            text = extract_text(uploaded)
            if len(text.strip()) < 50:
                st.error("Could not extract enough text. Use a text-based PDF or DOCX file.")
            else:
                st.session_state.result = analyze(text, jd)
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.result:
        r = st.session_state.result
        st.markdown('<div class="card-dark"><div class="sl-dark">👤 EXTRACTED INFORMATION</div>', unsafe_allow_html=True)
        for label, val in [("Name",r["name"]),("Email",r["email"]),("Phone",r["phone"]),
                            ("Education",r["education"]),("Experience",f"{r['exp_yrs']} yr(s)")]:
            st.markdown(f'<div class="info-row"><span class="info-label">{label}</span><span class="info-value">{val}</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card"><div class="sl">✅ Detected Skills</div>', unsafe_allow_html=True)
        if r["detected"]:
            st.markdown("".join([f'<span class="chip-green">{s.title()}</span>' for s in r["detected"]]), unsafe_allow_html=True)
        else:
            st.markdown('<p style="color:#555555;font-size:13px;">No recognizable skills detected.</p>', unsafe_allow_html=True)
        st.markdown('<div class="sl" style="margin-top:16px;">⚠️ Missing Important Skills</div>', unsafe_allow_html=True)
        if r["missing"]:
            st.markdown("".join([f'<span class="chip-red">{s.title()}</span>' for s in r["missing"]]), unsafe_allow_html=True)
        else:
            st.markdown('<p style="color:#065f46;font-size:13px;font-weight:700;">✅ No critical skills missing!</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ════════ RIGHT ════════
with right:
    if st.session_state.result:
        r     = st.session_state.result
        score = r["overall"]
        sc    = "#6aef8a" if score>=70 else "#fbbf24" if score>=50 else "#f87171"
        verdict = "🔥 Strong Resume" if score>=70 else "⚡ Needs Improvement" if score>=50 else "❗ Weak — Improve Now"
        note    = ("Well-structured and ATS-ready." if score>=70 else
                   "Add skills, achievements, and keywords." if score>=50 else
                   "Significant improvements needed to pass ATS.")

        st.markdown(f"""
        <div class="card-dark">
            <div class="sl-dark">📊 OVERALL RESUME SCORE</div>
            <div style="display:flex;align-items:center;gap:20px;flex-wrap:wrap;">
                <div>
                    <div style="font-size:72px;font-weight:700;font-family:'Space Mono',monospace;color:{sc};line-height:1;">{score}</div>
                    <div style="font-size:12px;color:#888888;margin-top:4px;">out of 100</div>
                </div>
                <div>
                    <div style="font-size:15px;font-weight:700;color:#ffffff;margin-bottom:6px;">{verdict}</div>
                    <div style="font-size:13px;color:#cccccc;line-height:1.6;">{note}</div>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

        st.markdown('<div class="card"><div class="sl">Score Breakdown</div>', unsafe_allow_html=True)
        for label, val, col in [
            ("Formatting",         r["fmt"],       "#6aef8a"),
            ("Skills Relevance",   r["skills_sc"], "#c4b5fd"),
            ("Experience Quality", r["exp_sc"],    "#fbbf24"),
            ("Keyword Match",      r["kw_sc"],     "#6aef8a"),
        ]:
            st.markdown(f"""
            <div class="prog-wrap">
                <div class="prog-label">
                    <span>{label}</span>
                    <span style="color:{col};font-family:'Space Mono',monospace;">{val} / 100</span>
                </div>
                <div class="prog-track"><div class="prog-fill" style="width:{val}%;background:{col};"></div></div>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        ats    = r["ats"]
        kw_pct = r["kw_pct"]
        ats_ok = ats >= 60
        bg_a   = "#6aef8a" if ats_ok else "#ffffff"
        lc     = "#1a5c2a" if ats_ok else "#555555"
        bdg_bg = "#111111" if ats_ok else "#fee2e2"
        bdg_tc = "#6aef8a" if ats_ok else "#991b1b"

        st.markdown(f"""
        <div style="background:{bg_a};border-radius:20px;padding:22px;margin-bottom:14px;
             {'box-shadow:0 2px 8px rgba(0,0,0,0.05);' if not ats_ok else ''}">
            <div style="font-size:11px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:{lc};margin-bottom:12px;">🤖 ATS COMPATIBILITY</div>
            <div style="display:flex;align-items:center;gap:24px;flex-wrap:wrap;">
                <div>
                    <div style="font-size:40px;font-weight:700;font-family:'Space Mono',monospace;color:#111111;">{ats}</div>
                    <div style="font-size:12px;color:{lc};font-weight:600;">ATS Score</div>
                </div>
                <div style="width:1px;height:44px;background:{'#11111133' if ats_ok else '#dddddd'};"></div>
                <div>
                    <div style="font-size:40px;font-weight:700;font-family:'Space Mono',monospace;color:#111111;">{kw_pct}%</div>
                    <div style="font-size:12px;color:{lc};font-weight:600;">Keyword Match</div>
                </div>
                <div>
                    <span style="background:{bdg_bg};color:{bdg_tc};border-radius:12px;padding:8px 14px;font-weight:700;font-size:13px;">
                        {'✅ ATS Friendly' if ats_ok else '❌ ATS Risk'}
                    </span>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

        st.markdown('<div class="card"><div class="sl">💡 Improvement Suggestions</div>', unsafe_allow_html=True)
        for i, s in enumerate(r["sugs"], 1):
            st.markdown(f'<div class="sug-item"><strong>#{i}</strong> &nbsp; {s}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="card-dark" style="min-height:340px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;">
            <div style="font-size:52px;margin-bottom:12px;">🤖</div>
            <div style="font-size:20px;font-weight:700;color:#ffffff;margin-bottom:8px;">Ready to Analyze</div>
            <div style="font-size:14px;color:#bbbbbb;max-width:280px;line-height:1.7;">
                Upload a PDF or DOCX resume on the left and hit Analyze
            </div>
        </div>
        <div class="card-green" style="margin-top:0;">
            <div class="sl-green">WHAT YOU WILL GET</div>
            <div style="font-size:14px;color:#111111;font-weight:500;line-height:2.2;">
                📊 Overall Score (0–100)<br>
                🔍 Automatic skill extraction<br>
                🤖 ATS compatibility check<br>
                ⚠️ Missing skills list<br>
                💡 5 personalized suggestions
            </div>
        </div>""", unsafe_allow_html=True)
