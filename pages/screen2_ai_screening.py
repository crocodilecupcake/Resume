import streamlit as st
import PyPDF2, docx, io, re, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from shared_css import SHARED_CSS

st.set_page_config(page_title="AI Resume Screening", page_icon="🤖", layout="wide")
st.markdown(SHARED_CSS, unsafe_allow_html=True)

# ── Extra CSS: fix placeholder + input text + info-row visibility ─────────────
st.markdown("""
<style>
/* ── Placeholder text — visible grey ── */
input::placeholder, textarea::placeholder {
    color: #999999 !important;
    opacity: 1 !important;
    font-style: italic;
}
input::-webkit-input-placeholder, textarea::-webkit-input-placeholder {
    color: #999999 !important;
    opacity: 1 !important;
}
input::-moz-placeholder, textarea::-moz-placeholder {
    color: #999999 !important;
    opacity: 1 !important;
}
/* ── Typed text and input background ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: #ffffff !important;
    color: #111111 !important;
    border: 2px solid #cccccc !important;
    border-radius: 10px !important;
}
/* ── Info rows — dark bg with clearly visible labels & values ── */
.info-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 9px 14px;
    border-radius: 10px;
    background: #1e1e1e;
    margin-bottom: 7px;
    font-size: 13px;
    flex-wrap: wrap;
    gap: 4px;
    border: 1px solid #333333;
}
.info-label {
    color: #9ca3af;
    font-weight: 700;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    min-width: 100px;
    flex-shrink: 0;
}
.info-value {
    color: #ffffff !important;
    font-weight: 700;
    font-size: 13px;
    text-align: right;
    word-break: break-all;
    max-width: 68%;
    background: #2a2a2a;
    padding: 3px 10px;
    border-radius: 6px;
}
.info-value.not-detected {
    color: #f87171 !important;
    background: #3a1a1a !important;
    font-weight: 600;
    font-style: italic;
    font-size: 12px;
}
/* ── Chips ── */
.chip-green { display:inline-block; background:#d1fae5; color:#065f46; border-radius:20px; padding:4px 12px; font-size:12px; font-weight:700; margin:3px; }
.chip-red   { display:inline-block; background:#fee2e2; color:#991b1b; border-radius:20px; padding:4px 12px; font-size:12px; font-weight:700; margin:3px; }
/* ── Suggestion items ── */
.sug-item {
    background: #f5f5f5;
    border-radius: 12px;
    padding: 13px 16px;
    margin-bottom: 8px;
    border-left: 3px solid #6aef8a;
    font-size: 13px;
    color: #111111 !important;
    font-weight: 500;
    line-height: 1.5;
}
/* ── Dark card override — ensure children text is visible ── */
.card-dark .info-label { color: #aaaaaa !important; }
.card-dark .info-value { color: #ffffff !important; }
</style>
""", unsafe_allow_html=True)

# ── Data ──────────────────────────────────────────────────────────────────────
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
IMPORTANT = [
    "python","machine learning","sql","docker","git","aws","tensorflow","pytorch",
    "react","javascript","deep learning","kubernetes","nlp","computer vision","mlops"
]
QUALITY_KW = [
    "improved","reduced","built","developed","designed","achieved","increased",
    "optimized","automated","deployed","implemented","managed","led","created",
    "launched","delivered","analysed","researched","scaled","%","award","winner",
    "rank","certification","published"
]
ATS_KW = [
    "python","java","sql","machine learning","data analysis","api","cloud","agile",
    "docker","git","testing","communication","leadership","problem solving",
    "algorithms","deep learning","nlp","automation","ci/cd","kubernetes"
]
SUGG_POOL = [
    "Add measurable achievements with numbers (e.g., improved API response time by 40%).",
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

# ── Text extractor ─────────────────────────────────────────────────────────
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

# ── Analyzer ──────────────────────────────────────────────────────────────────
def analyze(text, jd=""):
    tl    = text.lower()
    lines = [l.strip() for l in text.split("\n") if l.strip()]

    # ── Name detection ──────────────────────────────────────────────────────
    name = "Not detected"
    for line in lines[:8]:
        words = line.split()
        if (2 <= len(words) <= 4
                and all(w[0].isupper() for w in words if w.isalpha())
                and not any(ch.isdigit() for ch in line)
                and len(line) < 50):
            name = line
            break

    # ── Email detection — robust multi-pattern ───────────────────────────────
    email = "Not detected"
    # Collapse all whitespace/newlines first for PDF-extracted text
    text_collapsed = re.sub(r'\s+', '', text)
    # Pattern 1: standard email in original text
    em1 = re.findall(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}', text)
    if em1:
        email = em1[0].strip().rstrip('.,;)')
    else:
        # Pattern 2: spaces around @ (PDF extracts weirdly sometimes)
        em2 = re.findall(r'[a-zA-Z0-9._%+\-]+\s*@\s*[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}', text)
        if em2:
            email = re.sub(r'\s+', '', em2[0]).rstrip('.,;)')
        else:
            # Pattern 3: fully collapsed text (handles broken line emails)
            em3 = re.findall(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}', text_collapsed)
            if em3:
                email = em3[0].strip().rstrip('.,;)')
            else:
                # Pattern 4: lowercase fallback
                em4 = re.findall(r'[a-z0-9._%+\-]+@[a-z0-9.\-]+\.[a-z]{2,}', tl)
                if em4:
                    email = em4[0].strip().rstrip('.,;)')

    # ── Phone detection — robust multi-pattern ──────────────────────────────
    phone = "Not detected"
    text_no_space = re.sub(r'[\s]', '', text)
    text_clean     = re.sub(r'[\s\-\.\(\)]', '', text)  # digits + country code only

    # Pattern 1: +91 followed by 10 digits (spaces/dashes allowed)
    ph1 = re.findall(r'\+91[\s\-]?[6-9]\d{9}', text)
    if ph1:
        digits = re.sub(r'\D', '', ph1[0])
        phone = f'+91 {digits[2:7]} {digits[7:]}'
    else:
        # Pattern 2: Indian mobile in no-space text
        ph2 = re.findall(r'(?:91)?[6-9]\d{9}', text_no_space)
        if ph2:
            raw = ph2[0]
            digits = re.sub(r'\D', '', raw)
            if len(digits) == 12 and digits.startswith('91'):
                phone = f'+91 {digits[2:7]} {digits[7:]}'
            elif len(digits) == 10:
                phone = f'{digits[:5]} {digits[5:]}'
            else:
                phone = raw
        else:
            # Pattern 3: any 10-digit number starting with 6-9
            ph3 = re.findall(r'\b[6-9]\d{9}\b', text_clean)
            if ph3:
                d = ph3[0]
                phone = f'{d[:5]} {d[5:]}'
            else:
                # Pattern 4: general 10+ digit with separators
                ph4 = re.findall(r'(?:\+?\d[\d\s\-\.]{8,}\d)', text)
                if ph4:
                    candidate = re.sub(r'[^\d+]', '', ph4[0])
                    if 10 <= len(candidate) <= 13:
                        phone = re.sub(r'\s+', ' ', ph4[0]).strip()
                else:
                    # Pattern 5: dashes/dots e.g. 98765-43210
                    ph5 = re.findall(r'\b[6-9]\d{2}[\s\-\.]\d{3}[\s\-\.]\d{4}\b', text)
                    if ph5:
                        phone = ph5[0]

    # ── Skills ───────────────────────────────────────────────────────────────
    detected = [s for s in KNOWN_SKILLS if s in tl]
    missing  = [s for s in IMPORTANT if s not in tl][:6]

    # ── Education ────────────────────────────────────────────────────────────
    edu_kw = ["b.e","b.tech","m.tech","bsc","msc","bachelor","master","engineering",
              "university","college","cgpa","gpa","percentage","diploma"]
    edu_lines = [l.strip() for l in lines if any(k in l.lower() for k in edu_kw)]
    education = edu_lines[0][:80] if edu_lines else "Not detected"

    # ── Experience years — improved detection ────────────────────────────────
    exp_yrs = 0
    # Pattern 1: explicit "X year(s)" or "X yr(s)" or "X months"
    exp_pat = re.findall(r'(\d+)\s*(year|yr|months?)', tl)
    if exp_pat:
        exp_yrs = round(min(sum(int(v)/12 if "month" in u else int(v) for v, u in exp_pat), 15), 1)
    # Pattern 2: count date ranges like "Jun 2022 – Aug 2023" or "2021 - 2023"
    if exp_yrs == 0:
        date_ranges = re.findall(
            r'(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)?\s*(20\d{2})\s*[–\-–—to]+\s*(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)?\s*(20\d{2}|present|current)',
            tl
        )
        total_months = 0
        import datetime
        cur_year = datetime.datetime.now().year
        for start_yr, end_yr in date_ranges:
            sy = int(start_yr)
            ey = cur_year if end_yr in ('present', 'current') else int(end_yr)
            total_months += max(0, (ey - sy) * 12)
        if total_months > 0:
            exp_yrs = round(min(total_months / 12, 15), 1)
    # Pattern 3: look for "X+ years experience" type phrasing
    if exp_yrs == 0:
        plus_pat = re.findall(r'(\d+)\+\s*(?:year|yr)', tl)
        if plus_pat:
            exp_yrs = int(plus_pat[0])

    # ── Section detection ─────────────────────────────────────────────────────
    has_summary    = any(k in tl for k in ["summary","objective","profile","about"])
    has_skills     = any(k in tl for k in ["skills","technologies","tools","stack"])
    has_experience = any(k in tl for k in ["experience","internship","work","employment"])
    has_projects   = any(k in tl for k in ["project","built","developed","created"])
    has_education  = any(k in tl for k in ["education","university","college","b.e","b.tech","diploma"])
    has_certs      = any(k in tl for k in ["certification","certified","course","hackathon","award"])
    has_contact    = (email != "Not detected") or (phone != "Not detected")
    has_links      = any(k in tl for k in ["github","linkedin","portfolio","behance"])
    wc             = len(text.split())

    # ── Scoring ───────────────────────────────────────────────────────────────
    fmt = min(100,
              40
              + 10 * has_summary
              + 10 * has_skills
              + 10 * has_contact
              + 10 * has_links
              + 10 * has_education
              + 10 * has_certs)
    if wc < 150: fmt = max(20, fmt - 20)
    elif wc > 900: fmt = max(50, fmt - 10)

    skills_sc    = min(100, 30 + len(detected) * 5)
    quality_hits = sum(1 for k in QUALITY_KW if k in tl)
    exp_sc       = min(100, 30 + quality_hits * 7)
    if not has_experience: exp_sc = max(20, exp_sc - 30)

    if jd:
        jd_w  = set(re.findall(r'\b\w+\b', jd.lower()))
        res_w = set(re.findall(r'\b\w+\b', tl))
        com   = jd_w & res_w
        kw_sc  = min(100, int(len(com) / max(len(jd_w), 1) * 200))
        kw_pct = min(100, int(len(com) / max(len(jd_w), 1) * 150))
    else:
        ah     = sum(1 for k in ATS_KW if k in tl)
        kw_sc  = min(100, 30 + ah * 5)
        kw_pct = min(100, 20 + ah * 5)

    overall = int(0.25 * fmt + 0.30 * skills_sc + 0.25 * exp_sc + 0.20 * kw_sc)
    ats     = min(100,
                  40
                  + 15 * has_skills
                  + 10 * has_contact
                  + 10 * (has_experience or has_projects)
                  + 10 * (wc > 200)
                  + 15 * (kw_pct > 40))

    # ── Suggestions ───────────────────────────────────────────────────────────
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
        if s not in sugs and len(sugs) < 5:
            sugs.append(s)

    return {
        "name": name, "email": email, "phone": phone,
        "education": education, "exp_yrs": exp_yrs,
        "overall": overall, "fmt": fmt, "skills_sc": skills_sc,
        "exp_sc": exp_sc, "kw_sc": kw_sc,
        "ats": ats, "kw_pct": kw_pct,
        "detected": detected, "missing": missing, "sugs": sugs[:5],
    }

# ── Session state ─────────────────────────────────────────────────────────────
if "result" not in st.session_state:
    st.session_state.result = None

# ── Nav ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="nav-bar">
  <div class="nav-title">🤖 AI Resume Screening</div>
  <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;">
    <div class="nav-badge-purple">Module 2 / 3</div>
    <div style="color:#aaaaaa;font-size:12px;">Free · No API</div>
  </div>
</div>""", unsafe_allow_html=True)

if st.button("← Home", key="home_btn"):
    st.switch_page("app.py")

st.markdown("<br>", unsafe_allow_html=True)
left, right = st.columns([1, 1.15], gap="large")

# ════════ LEFT ════════
with left:
    st.markdown('<div class="card"><div class="sl">01 — Upload Resume</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader(
        "Upload resume (PDF / DOCX / TXT)",
        type=["pdf", "docx", "txt"],
        label_visibility="collapsed"
    )
    jd = st.text_area(
        "Job Description (optional — improves keyword scoring)",
        placeholder="Paste the job description here to get targeted keyword analysis...",
        height=110,
        key="jd_in"
    )
    if uploaded:
        st.markdown(
            f'<div style="background:#f0f0f0;border-radius:12px;padding:12px 14px;'
            f'font-size:13px;color:#111111;font-weight:600;margin-top:8px;">'
            f'📄 {uploaded.name} — ready to analyze</div>',
            unsafe_allow_html=True
        )

    go = st.button("🔍 Analyze Resume", use_container_width=True, disabled=uploaded is None)
    if go and uploaded:
        with st.spinner("Analyzing your resume..."):
            text = extract_text(uploaded)
            if len(text.strip()) < 50:
                st.error("Could not extract text. Please use a text-based PDF or DOCX file (not a scanned image).")
            else:
                st.session_state.result = analyze(text, jd)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Extracted info ────────────────────────────────────────────────────────
    if st.session_state.result:
        r = st.session_state.result

        # Render the extracted info card using inline styles for guaranteed visibility
        st.markdown(
            '<div style="background:#111111;border-radius:20px;padding:20px 22px;margin-bottom:14px;">'
            '<div style="font-size:11px;font-weight:700;letter-spacing:2px;'
            'text-transform:uppercase;color:#ffffff;margin-bottom:14px;">👤 EXTRACTED INFORMATION</div>',
            unsafe_allow_html=True
        )
        for label, val in [
            ("Name",       r["name"]),
            ("Email",      r["email"]),
            ("Phone",      r["phone"]),
            ("Education",  r["education"]),
            ("Experience", f'{r["exp_yrs"]} yr(s)'),
        ]:
            is_nd = (str(val) == "Not detected")
            if is_nd:
                val_style = (
                    'color:#f87171 !important;font-style:italic;font-weight:600;font-size:12px;'
                    'background:#3a1a1a;padding:3px 10px;border-radius:6px;'
                )
            else:
                val_style = (
                    'color:#ffffff !important;font-weight:700;font-size:13px;'
                    'background:#2a2a2a;padding:3px 10px;border-radius:6px;'
                )
            st.markdown(
                f'<div style="display:flex;justify-content:space-between;align-items:center;'
                f'padding:9px 14px;border-radius:10px;background:#1e1e1e;margin-bottom:7px;'
                f'flex-wrap:wrap;gap:4px;border:1px solid #333333;">'
                f'<span style="color:#9ca3af;font-weight:700;font-size:11px;text-transform:uppercase;'
                f'letter-spacing:0.8px;min-width:100px;">{label}</span>'
                f'<span style="{val_style}text-align:right;word-break:break-all;max-width:68%;">{val}</span>'
                f'</div>',
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)

        # ── Skills chips ──────────────────────────────────────────────────────
        st.markdown('<div class="card"><div class="sl">✅ Detected Skills</div>', unsafe_allow_html=True)
        if r["detected"]:
            st.markdown(
                "".join([f'<span class="chip-green">{s.title()}</span>' for s in r["detected"]]),
                unsafe_allow_html=True
            )
        else:
            st.markdown('<p style="color:#555555;font-size:13px;">No recognizable skills detected.</p>', unsafe_allow_html=True)

        st.markdown('<div class="sl" style="margin-top:16px;">⚠️ Missing Important Skills</div>', unsafe_allow_html=True)
        if r["missing"]:
            st.markdown(
                "".join([f'<span class="chip-red">{s.title()}</span>' for s in r["missing"]]),
                unsafe_allow_html=True
            )
        else:
            st.markdown('<p style="color:#065f46;font-size:13px;font-weight:700;">✅ No critical skills missing!</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ════════ RIGHT ════════
with right:
    if st.session_state.result:
        r     = st.session_state.result
        score = r["overall"]
        sc    = "#6aef8a" if score >= 70 else "#fbbf24" if score >= 50 else "#f87171"
        verdict = "🔥 Strong Resume" if score >= 70 else "⚡ Needs Improvement" if score >= 50 else "❗ Weak — Improve Now"
        note    = (
            "Well-structured and ATS-ready. You're in good shape!"
            if score >= 70 else
            "Add more skills, achievements, and keywords."
            if score >= 50 else
            "Significant improvements needed to pass ATS filters."
        )

        # Score card
        st.markdown(f"""
        <div class="card-dark">
            <div class="sl-dark">📊 OVERALL RESUME SCORE</div>
            <div style="display:flex;align-items:center;gap:20px;flex-wrap:wrap;">
                <div>
                    <div style="font-size:72px;font-weight:700;font-family:'Space Mono',monospace;
                         color:{sc};line-height:1;">{score}</div>
                    <div style="font-size:12px;color:#888888;margin-top:4px;">out of 100</div>
                </div>
                <div>
                    <div style="font-size:15px;font-weight:700;color:#ffffff;margin-bottom:6px;">{verdict}</div>
                    <div style="font-size:13px;color:#cccccc;line-height:1.6;">{note}</div>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

        # Breakdown bars
        st.markdown('<div class="card"><div class="sl">Score Breakdown</div>', unsafe_allow_html=True)
        for label, val, col in [
            ("Formatting",         r["fmt"],       "#6aef8a"),
            ("Skills Relevance",   r["skills_sc"], "#c4b5fd"),
            ("Experience Quality", r["exp_sc"],    "#fbbf24"),
            ("Keyword Match",      r["kw_sc"],     "#6aef8a"),
        ]:
            st.markdown(f"""
            <div style="margin-bottom:14px;">
                <div style="display:flex;justify-content:space-between;font-size:13px;
                     font-weight:700;color:#111111;margin-bottom:6px;">
                    <span>{label}</span>
                    <span style="color:{col};font-family:'Space Mono',monospace;">{val} / 100</span>
                </div>
                <div style="background:#eeeeee;border-radius:20px;height:10px;">
                    <div style="width:{val}%;background:{col};border-radius:20px;height:10px;"></div>
                </div>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # ATS card
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
            <div style="font-size:11px;font-weight:700;letter-spacing:2px;text-transform:uppercase;
                 color:{lc};margin-bottom:12px;">🤖 ATS COMPATIBILITY</div>
            <div style="display:flex;align-items:center;gap:28px;flex-wrap:wrap;">
                <div>
                    <div style="font-size:44px;font-weight:700;font-family:'Space Mono',monospace;
                         color:#111111;">{ats}</div>
                    <div style="font-size:12px;color:{lc};font-weight:600;">ATS Score</div>
                </div>
                <div style="width:1px;height:44px;background:{'#11111133' if ats_ok else '#dddddd'};"></div>
                <div>
                    <div style="font-size:44px;font-weight:700;font-family:'Space Mono',monospace;
                         color:#111111;">{kw_pct}%</div>
                    <div style="font-size:12px;color:{lc};font-weight:600;">Keyword Match</div>
                </div>
                <div>
                    <span style="background:{bdg_bg};color:{bdg_tc};border-radius:12px;
                         padding:8px 14px;font-weight:700;font-size:13px;">
                        {'✅ ATS Friendly' if ats_ok else '❌ ATS Risk'}
                    </span>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

        # Suggestions
        st.markdown('<div class="card"><div class="sl">💡 Improvement Suggestions</div>', unsafe_allow_html=True)
        for i, s in enumerate(r["sugs"], 1):
            st.markdown(
                f'<div class="sug-item"><strong style="color:#111111;">#{i}</strong> &nbsp; {s}</div>',
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="card-dark" style="min-height:340px;display:flex;flex-direction:column;
             align-items:center;justify-content:center;text-align:center;">
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
