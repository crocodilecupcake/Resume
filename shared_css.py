SHARED_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background: #f0f2ee !important;
    font-family: 'DM Sans', sans-serif;
}
[data-testid="stSidebar"], [data-testid="stToolbar"],
[data-testid="stDecoration"], [data-testid="stStatusWidget"] { display: none !important; }

/* ── Remove default streamlit padding on mobile ── */
.main .block-container {
    padding: 1rem 1rem 2rem 1rem !important;
    max-width: 100% !important;
}
@media (min-width: 768px) {
    .main .block-container {
        padding: 2rem 2rem 3rem 2rem !important;
    }
}

/* ─────────────────────────────────────────
   INPUT FIELDS — placeholder fix
───────────────────────────────────────── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > div {
    border-radius: 12px !important;
    border: 2px solid #cccccc !important;
    background: #ffffff !important;
    color: #111111 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    padding: 10px 14px !important;
    transition: border-color 0.2s !important;
}

/* THE CRITICAL FIX — placeholder visibility */
.stTextInput > div > div > input::placeholder,
.stTextArea > div > div > textarea::placeholder {
    color: #888888 !important;
    opacity: 1 !important;
    font-style: italic;
}
/* WebKit browsers (Chrome, Safari, mobile) */
.stTextInput > div > div > input::-webkit-input-placeholder,
.stTextArea > div > div > textarea::-webkit-input-placeholder {
    color: #888888 !important;
    opacity: 1 !important;
}
/* Firefox */
.stTextInput > div > div > input::-moz-placeholder,
.stTextArea > div > div > textarea::-moz-placeholder {
    color: #888888 !important;
    opacity: 1 !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #6aef8a !important;
    box-shadow: 0 0 0 3px rgba(106,239,138,0.2) !important;
    outline: none !important;
}

/* Labels */
.stTextInput label, .stTextArea label,
.stSelectbox label, .stRadio > label,
.stFileUploader label, .stSlider label,
.stMultiSelect label {
    color: #111111 !important;
    font-weight: 700 !important;
    font-size: 13px !important;
    margin-bottom: 4px !important;
}

/* Radio option text */
.stRadio div[role="radiogroup"] label { color: #111111 !important; font-weight: 600 !important; }

/* ─────────────────────────────────────────
   BUTTONS
───────────────────────────────────────── */
.stButton > button {
    border-radius: 12px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    background: #111111 !important;
    color: #ffffff !important;
    border: none !important;
    transition: all 0.2s !important;
    padding: 10px 20px !important;
    width: 100% !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(0,0,0,0.2) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* Download button */
.stDownloadButton > button {
    border-radius: 12px !important;
    font-weight: 700 !important;
    background: #6aef8a !important;
    color: #111111 !important;
    border: none !important;
}

/* ─────────────────────────────────────────
   MULTISELECT
───────────────────────────────────────── */
.stMultiSelect > div > div {
    border-radius: 12px !important;
    border: 2px solid #cccccc !important;
    background: #ffffff !important;
}
.stMultiSelect span { color: #111111 !important; }

/* ─────────────────────────────────────────
   SLIDER
───────────────────────────────────────── */
.stSlider > div { color: #111111 !important; }
.stSlider [data-testid="stTickBar"] { color: #666666 !important; }

/* ─────────────────────────────────────────
   FILE UPLOADER
───────────────────────────────────────── */
[data-testid="stFileUploader"] {
    border-radius: 14px !important;
    border: 2px dashed #bbbbbb !important;
    background: #ffffff !important;
    padding: 16px !important;
}
[data-testid="stFileUploader"] p,
[data-testid="stFileUploader"] span {
    color: #444444 !important;
    font-size: 13px !important;
}

/* ─────────────────────────────────────────
   EXPANDER
───────────────────────────────────────── */
.streamlit-expanderHeader {
    background: #f5f5f5 !important;
    border-radius: 12px !important;
    color: #111111 !important;
    font-weight: 700 !important;
}
.streamlit-expanderContent {
    background: #fafafa !important;
    border-radius: 0 0 12px 12px !important;
}

/* ─────────────────────────────────────────
   CARDS
───────────────────────────────────────── */
.card {
    background: #ffffff;
    border-radius: 20px;
    padding: 20px;
    margin-bottom: 14px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06);
}
@media (min-width: 768px) {
    .card { padding: 24px; }
}
.card-dark  { background: #111111; border-radius: 20px; padding: 20px; margin-bottom: 14px; }
.card-green { background: #6aef8a; border-radius: 20px; padding: 20px; margin-bottom: 14px; }
.card-purple{ background: #c4b5fd; border-radius: 20px; padding: 20px; margin-bottom: 14px; }
@media (min-width: 768px) {
    .card-dark, .card-green, .card-purple { padding: 24px; }
}

/* ─────────────────────────────────────────
   SECTION LABELS
───────────────────────────────────────── */
.sl      { font-size:11px; font-weight:700; letter-spacing:2px; text-transform:uppercase; color:#555555; margin-bottom:12px; }
.sl-dark { font-size:11px; font-weight:700; letter-spacing:2px; text-transform:uppercase; color:#999999; margin-bottom:12px; }
.sl-green{ font-size:11px; font-weight:700; letter-spacing:2px; text-transform:uppercase; color:#1a5c2a; margin-bottom:12px; }
.sl-purple{font-size:11px; font-weight:700; letter-spacing:2px; text-transform:uppercase; color:#3d1f8a; margin-bottom:12px; }

/* ─────────────────────────────────────────
   NAV BAR
───────────────────────────────────────── */
.nav-bar {
    background: #111111;
    border-radius: 16px;
    padding: 14px 18px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20px;
    flex-wrap: wrap;
    gap: 8px;
}
@media (min-width: 768px) {
    .nav-bar { border-radius: 20px; padding: 16px 28px; margin-bottom: 28px; }
}
.nav-title { color: #ffffff; font-size: 17px; font-weight: 700; }
@media (min-width: 768px) { .nav-title { font-size: 20px; } }
.nav-badge { background: #6aef8a; color: #111111; border-radius: 20px; padding: 5px 13px; font-size: 12px; font-weight: 700; }
.nav-badge-purple { background: #c4b5fd; color: #111111; border-radius: 20px; padding: 5px 13px; font-size: 12px; font-weight: 700; }

/* ─────────────────────────────────────────
   SKILL TAGS
───────────────────────────────────────── */
.skill-tag { display:inline-block; background:#111111; color:#6aef8a; border-radius:20px; padding:4px 12px; font-size:12px; font-weight:700; margin:3px; font-family:'Space Mono',monospace; }
.chip-green { display:inline-block; background:#d1fae5; color:#065f46; border-radius:20px; padding:3px 11px; font-size:11px; font-weight:700; margin:2px; }
.chip-red   { display:inline-block; background:#fee2e2; color:#991b1b; border-radius:20px; padding:3px 11px; font-size:11px; font-weight:700; margin:2px; }
.chip-dark  { display:inline-block; background:#111111; color:#c4b5fd; border-radius:20px; padding:3px 11px; font-size:11px; font-weight:700; margin:2px; font-family:'Space Mono',monospace; }

/* ─────────────────────────────────────────
   PROGRESS BARS
───────────────────────────────────────── */
.prog-wrap  { margin-bottom: 14px; }
.prog-label { display:flex; justify-content:space-between; font-size:13px; font-weight:700; color:#111111; margin-bottom:6px; }
.prog-track { background:#e5e5e5; border-radius:20px; height:10px; }
.prog-fill  { border-radius:20px; height:10px; }

/* ─────────────────────────────────────────
   ITEM ROWS (experience/project list)
───────────────────────────────────────── */
.item-row { background:#f5f5f5; border-radius:12px; padding:12px 16px; margin-bottom:8px; font-size:13px; color:#111111; font-weight:600; }
.item-sub { color:#444444; font-size:12px; font-weight:500; margin-top:2px; }

/* ─────────────────────────────────────────
   SUGGESTION ITEMS
───────────────────────────────────────── */
.sug-item { background:#f5f5f5; border-radius:12px; padding:13px 16px; margin-bottom:8px; border-left:3px solid #6aef8a; font-size:13px; color:#111111; font-weight:500; line-height:1.5; }

/* ─────────────────────────────────────────
   INFO ROWS (dark card)
───────────────────────────────────────── */
.info-row   { display:flex; justify-content:space-between; padding:10px 0; border-bottom:1px solid #2a2a2a; font-size:13px; flex-wrap:wrap; gap:4px; }
.info-label { color:#aaaaaa; font-weight:500; }
.info-value { color:#ffffff; font-weight:700; }

/* ─────────────────────────────────────────
   JOB CARDS
───────────────────────────────────────── */
.job-card { background:#ffffff; border-radius:16px; padding:18px; margin-bottom:4px; border:2px solid #eeeeee; position:relative; }
.job-card.saved { border-color:#6aef8a; background:#f4fff7; }
.job-role { font-size:15px; font-weight:700; color:#111111; padding-right:70px; }
.job-sub  { font-size:12px; color:#444444; margin-top:3px; font-weight:500; }
.match-badge { position:absolute; top:16px; right:16px; border-radius:20px; padding:3px 11px; font-size:12px; font-weight:700; font-family:'Space Mono',monospace; }
.badge-high   { background:#6aef8a; color:#111111; }
.badge-medium { background:#fef08a; color:#111111; }
.badge-low    { background:#fee2e2; color:#991b1b; }

/* ─────────────────────────────────────────
   LEARN ITEMS
───────────────────────────────────────── */
.learn-item { background:#f5f5f5; border-radius:12px; padding:13px 16px; margin-bottom:8px; }
.learn-title  { font-size:14px; font-weight:700; color:#111111; }
.learn-reason { font-size:12px; color:#444444; margin-top:3px; line-height:1.5; }

/* ─────────────────────────────────────────
   MOBILE — column stacking
───────────────────────────────────────── */
@media (max-width: 640px) {
    /* Make Streamlit columns stack on small screens */
    [data-testid="stHorizontalBlock"] {
        flex-direction: column !important;
    }
    [data-testid="stHorizontalBlock"] > div {
        width: 100% !important;
        min-width: 100% !important;
        flex: 1 1 100% !important;
    }
    .nav-title { font-size: 15px; }
    .hero-title { font-size: 30px !important; }
    .hero-subtitle { font-size: 14px !important; }
    .hero-stats { flex-wrap: wrap !important; gap: 20px !important; }
    .module-card { min-height: auto !important; }
}
</style>
"""
