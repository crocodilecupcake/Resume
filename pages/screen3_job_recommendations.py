import streamlit as st
import pandas as pd
import PyPDF2, docx, io, re, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from shared_css import SHARED_CSS

st.set_page_config(page_title="Job Recommendations", page_icon="💼", layout="wide")
st.markdown(SHARED_CSS, unsafe_allow_html=True)

@st.cache_data
def load_jobs():
    for path in ["jobs.csv","data/jobs.csv","/mnt/user-data/uploads/jobs.csv"]:
        if os.path.exists(path):
            df = pd.read_csv(path)
            df.columns = df.columns.str.strip().str.lower()
            df["skills_list"] = df["skills"].apply(lambda x: [s.strip().lower() for s in str(x).split("|")])
            return df
    return pd.DataFrame(columns=["role","skills","skills_list"])

jobs_df = load_jobs()
ALL_JOB_SKILLS = sorted(set(s for sl in jobs_df["skills_list"] for s in sl))
EXTRA  = ["html","css","javascript","react","figma","excel","power bi","tableau",
          "photoshop","unity","c#","go","rust","flutter","dart","swift","firebase",
          "redis","graphql","next.js","fastapi","django","flask"]
PICKER = sorted(set(ALL_JOB_SKILLS + EXTRA))
PRIORITY_MAP = {
    "python":"High","machine learning":"High","sql":"High","docker":"High",
    "aws":"High","tensorflow":"High","pytorch":"High","kubernetes":"Medium",
    "nlp":"Medium","computer vision":"Medium","mlops":"Medium","spark":"Medium",
    "react":"Medium","javascript":"Medium","go":"Low","rust":"Low",
}

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

def match_jobs(user_skills):
    ul = [s.lower() for s in user_skills]
    res = []
    for _, row in jobs_df.iterrows():
        req  = row["skills_list"]
        have = [s for s in req if s in ul]
        miss = [s for s in req if s not in ul]
        pct  = round(len(have)/len(req)*100) if req else 0
        res.append({"id":row.name,"role":row["role"],"required":req,"have":have,"miss":miss,"match":pct})
    return sorted(res, key=lambda x: x["match"], reverse=True)

def compute_gap(results):
    counter = {}
    for j in results[:10]:
        for s in j["miss"]: counter[s] = counter.get(s,0)+1
    return sorted(counter, key=counter.get, reverse=True)[:8]

def suggest_roles(results):
    beg = [j["role"] for j in results if 30<=j["match"]<60][:3]
    mid = [j["role"] for j in results if 60<=j["match"]<85][:3]
    adv = [j["role"] for j in results if j["match"]>=85][:3]
    if not beg: beg = [j["role"] for j in results[-5:]][:3]
    if not mid: mid = [j["role"] for j in results[len(results)//2:]][:3]
    if not adv: adv = [j["role"] for j in results[:3]]
    return beg, mid, adv

for k,v in {"job_results":None,"bookmarks":[],"user_skills":[]}.items():
    if k not in st.session_state: st.session_state[k] = v

# ── Nav ───────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="nav-bar">
  <div class="nav-title">💼 Job Recommendations</div>
  <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;">
    <div class="nav-badge">Module 3 / 3</div>
    <div style="color:#888888;font-size:12px;">{len(jobs_df)} Roles · Free</div>
  </div>
</div>""", unsafe_allow_html=True)

if st.button("← Home", key="home_btn"):
    st.switch_page("app.py")

if jobs_df.empty:
    st.error("⚠️ jobs.csv not found. Place jobs.csv in the same folder as app.py and restart.")
    st.stop()

st.markdown("<br>", unsafe_allow_html=True)
left, right = st.columns([1, 1.1], gap="large")

# ════════ LEFT ════════
with left:
    st.markdown("""
    <style>
    div[data-testid="stRadio"] label p {
        color: red !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="card"><div class="sl">01 — Input Source</div>', unsafe_allow_html=True)
    mode = st.radio("How do you want to input skills?",
                    ["📄 Upload Resume","⚡ Select Skills Manually"], horizontal=True, key="imode")

    if mode == "📄 Upload Resume":
        uploaded = st.file_uploader("Upload resume", type=["pdf","docx","txt"], label_visibility="collapsed")
        if uploaded:
            txt   = extract_text(uploaded)
            found = [s for s in ALL_JOB_SKILLS if s in txt.lower()]
            st.session_state.user_skills = found
            st.markdown(f'<div style="background:#f0f0f0;border-radius:12px;padding:12px 14px;font-size:13px;color:#111111;font-weight:600;margin-top:8px;">✅ Found <strong>{len(found)} skills</strong> in {uploaded.name}</div>', unsafe_allow_html=True)
            if found:
                chips  = "".join([f'<span class="chip-dark">{s.title()}</span>' for s in found[:18]])
                suffix = f'<span style="font-size:12px;color:#555555;"> +{len(found)-18} more</span>' if len(found)>18 else ""
                st.markdown(chips+suffix, unsafe_allow_html=True)
    else:
        sel = st.multiselect("Select your skills:", PICKER,
                             default=st.session_state.user_skills or [], key="sk_multi")
        st.session_state.user_skills = sel

    go = st.button("🚀 Find Matching Jobs", use_container_width=True, disabled=len(st.session_state.user_skills)==0)
    if go:
        st.session_state.job_results = match_jobs(st.session_state.user_skills)
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.job_results:
        res = st.session_state.job_results
        gap = compute_gap(res)

        st.markdown('<div class="card-purple"><div class="sl-purple">🎯 SKILL GAP — YOU ARE MISSING</div>', unsafe_allow_html=True)
        if gap:
            st.markdown("".join([f'<span class="chip-dark">{s.title()}</span>' for s in gap]), unsafe_allow_html=True)
        else:
            st.markdown('<p style="color:#111111;font-weight:700;font-size:14px;">🎉 You have all key skills!</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        if gap:
            st.markdown('<div class="card"><div class="sl">📚 What to Learn Next</div>', unsafe_allow_html=True)
            for s in gap[:5]:
                prio   = PRIORITY_MAP.get(s,"Low")
                pc     = {"High":"#ef4444","Medium":"#fbbf24","Low":"#22c55e"}[prio]
                reason = {"High":  f"'{s.title()}' appears in 70%+ of job postings — critical.",
                          "Medium":f"'{s.title()}' is frequently required in mid-level roles.",
                          "Low":   f"'{s.title()}' is a nice-to-have that differentiates you."}[prio]
                st.markdown(f'<div class="learn-item" style="border-left:3px solid {pc};"><div class="learn-title">{s.title()}</div><div class="learn-reason">{reason}</div><div style="font-size:11px;color:{pc};font-weight:700;margin-top:4px;">{prio} Priority</div></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        beg, mid, adv = suggest_roles(res)
        st.markdown('<div class="card-dark"><div class="sl-dark">🗺️ SUGGESTED ROLES BY LEVEL</div>', unsafe_allow_html=True)
        for label, roles, col in [("🟢 Beginner",beg,"#6aef8a"),("🟡 Intermediate",mid,"#fbbf24"),("🔴 Advanced",adv,"#f87171")]:
            if roles:
                st.markdown(f'<div style="font-size:12px;font-weight:700;color:{col};margin-bottom:4px;">{label}</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="font-size:13px;color:#cccccc;margin-bottom:12px;">{" · ".join(roles)}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ════════ RIGHT: JOB CARDS ════════
with right:
    if st.session_state.job_results:
        res   = st.session_state.job_results
        total = len(res)
        high  = sum(1 for j in res if j["match"]>=75)
        saved = len(st.session_state.bookmarks)

        st.markdown(f"""
        <div class="card-green">
            <div class="sl-green">📊 RESULTS SUMMARY</div>
            <div style="display:flex;gap:28px;flex-wrap:wrap;">
                <div>
                    <div style="font-size:38px;font-weight:700;font-family:'Space Mono',monospace;color:#111111;line-height:1;">{total}</div>
                    <div style="font-size:12px;color:#1a5c2a;font-weight:600;margin-top:3px;">Total Jobs</div>
                </div>
                <div>
                    <div style="font-size:38px;font-weight:700;font-family:'Space Mono',monospace;color:#111111;line-height:1;">{high}</div>
                    <div style="font-size:12px;color:#1a5c2a;font-weight:600;margin-top:3px;">High Match</div>
                </div>
                <div>
                    <div style="font-size:38px;font-weight:700;font-family:'Space Mono',monospace;color:#111111;line-height:1;">{saved}</div>
                    <div style="font-size:12px;color:#1a5c2a;font-weight:600;margin-top:3px;">Bookmarked</div>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

        st.markdown('<div class="card"><div class="sl">🔍 Filter Jobs</div>', unsafe_allow_html=True)
        fc1, fc2 = st.columns(2)
        min_m = fc1.slider("Min Match %", 0, 100, 0, 5, key="min_m")
        ftype = fc2.selectbox("Show", ["All Jobs","Bookmarked Only","High Match (75%+)"], key="ftype")
        st.markdown('</div>', unsafe_allow_html=True)

        filtered = res
        if ftype == "Bookmarked Only":    filtered = [j for j in res if j["id"] in st.session_state.bookmarks]
        elif ftype == "High Match (75%+)":filtered = [j for j in res if j["match"]>=75]
        filtered = [j for j in filtered if j["match"]>=min_m]

        st.markdown(f'<div style="font-size:13px;color:#444444;font-weight:600;margin-bottom:12px;">Showing {len(filtered)} of {total} jobs</div>', unsafe_allow_html=True)

        for job in filtered:
            jid      = job["id"]
            match    = job["match"]
            is_saved = jid in st.session_state.bookmarks
            bdg      = "badge-high" if match>=75 else "badge-medium" if match>=50 else "badge-low"
            c_cls    = "job-card saved" if is_saved else "job-card"
            have_c   = "".join([f'<span class="chip-green">✓ {s.title()}</span>' for s in job["have"]])
            miss_c   = "".join([f'<span class="chip-red">✗ {s.title()}</span>' for s in job["miss"]])

            st.markdown(f"""
            <div class="{c_cls}">
                <span class="match-badge {bdg}">{match}%</span>
                <div class="job-role">{job["role"]}</div>
                <div class="job-sub">{len(job["required"])} required · {len(job["have"])} you have · {len(job["miss"])} missing</div>
                <div style="margin-top:10px;">{have_c}{miss_c}</div>
            </div>""", unsafe_allow_html=True)

            col_bm, col_sp = st.columns([1,3])
            with col_bm:
                bm_lbl = "★ Saved" if is_saved else "☆ Save"
                if st.button(bm_lbl, key=f"bm_{jid}_{match}"):
                    if jid in st.session_state.bookmarks: st.session_state.bookmarks.remove(jid)
                    else: st.session_state.bookmarks.append(jid)
                    st.rerun()
            st.markdown("<div style='margin-bottom:6px;'></div>", unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="card-dark" style="min-height:340px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;">
            <div style="font-size:52px;margin-bottom:12px;">💼</div>
            <div style="font-size:20px;font-weight:700;color:#ffffff;margin-bottom:8px;">Jobs Await You</div>
            <div style="font-size:14px;color:#bbbbbb;max-width:280px;line-height:1.7;">
                Upload your resume or pick skills on the left, then click Find Matching Jobs
            </div>
        </div>
        <div class="card-green" style="margin-top:0;">
            <div class="sl-green">HOW IT WORKS</div>
            <div style="font-size:14px;color:#111111;font-weight:500;line-height:2.2;">
                🎯 Matches skills to 88 real job roles<br>
                📊 Shows match % for every position<br>
                🔍 Identifies skill gaps instantly<br>
                📚 Recommends what to learn next<br>
                🗺️ Suggests roles by experience level
            </div>
        </div>""", unsafe_allow_html=True)
