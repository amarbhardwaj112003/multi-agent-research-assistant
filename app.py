import streamlit as st
import time
from agents import build_search_agent, build_reader_agent, writer_chain, critic_chain

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NEXUS · Research Engine",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────
# GLOBAL DESIGN SYSTEM
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Oxanium:wght@300;400;500;600;700;800&family=IBM+Plex+Mono:wght@300;400;500;600&family=DM+Sans:wght@300;400;500&display=swap');

/* ── RESET & ROOT ── */
:root {
    --bg-void:       #04070f;
    --bg-base:       #07101d;
    --bg-surface:    #0c1828;
    --bg-elevated:   #101f30;
    --bg-overlay:    rgba(16,31,48,0.75);

    --cyan:          #00d4ff;
    --cyan-dim:      #007a99;
    --cyan-glow:     rgba(0,212,255,0.18);
    --cyan-subtle:   rgba(0,212,255,0.07);

    --amber:         #f0a500;
    --amber-dim:     #7a5200;
    --amber-glow:    rgba(240,165,0,0.18);
    --amber-subtle:  rgba(240,165,0,0.07);

    --red:           #ff4060;
    --red-subtle:    rgba(255,64,96,0.09);
    --green:         #00e5a0;
    --green-subtle:  rgba(0,229,160,0.09);

    --ink-0:         #f0f6ff;
    --ink-1:         #9db8cc;
    --ink-2:         #4d6a80;
    --ink-3:         #263d50;

    --border-hard:   rgba(0,212,255,0.2);
    --border-soft:   rgba(255,255,255,0.06);
    --border-faint:  rgba(255,255,255,0.03);

    --radius-sm:     6px;
    --radius-md:     10px;
    --radius-lg:     16px;

    --font-display:  'Oxanium', sans-serif;
    --font-mono:     'IBM Plex Mono', monospace;
    --font-body:     'DM Sans', sans-serif;

    --shadow-deep:   0 20px 60px rgba(0,0,0,0.6);
    --shadow-card:   0 4px 24px rgba(0,0,0,0.4);
    --shadow-cyan:   0 0 30px rgba(0,212,255,0.12);
    --shadow-amber:  0 0 30px rgba(240,165,0,0.12);
}

.stApp {
    background: #04070f !important;
}

/* Remove header */
header {
    visibility: hidden !important;
    height: 0px !important;
    position: fixed !important;
}

/* Hide Main Header */
header {
    visibility: hidden !important;
    height: 0px !important;
}

/* Hide top right menu (⋮) + Deploy button area */
[data-testid="stToolbar"] {
    display: none !important;
}

/* Hide top decoration line */
[data-testid="stDecoration"] {
    display: none !important;
}

/* Remove top padding caused by header */
div.block-container {
    padding-top: 1rem !important;
}

/* Optional: remove hamburger menu */
#MainMenu {
    visibility: hidden !important;
}

/* Optional: remove footer */
footer {
    visibility: hidden !important;
}

/* Remove deploy top area */
[data-testid="stDecoration"] {
    display: none !important;
}


html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg-void) !important;
    font-family: var(--font-body) !important;
    color: var(--ink-1) !important;
    with: 100% !important;
    height: 100% !important;
}

[data-testid="stSidebar"] {
    background: var(--bg-base) !important;
    border-right: 1px solid var(--border-soft) !important;
}

[data-testid="stSidebar"] * {
    font-family: var(--font-body) !important;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--cyan-dim); border-radius: 99px; }

/* ── HERO ── */
.nx-hero {
    position: relative;
    overflow: hidden;
    background: var(--bg-surface);
    border: 1px solid var(--border-hard);
    border-radius: var(--radius-lg);
    padding: 44px 48px;
    margin-bottom: 28px;
    margin-top: 0rem !important;
    box-shadow: var(--shadow-cyan), var(--shadow-card);
}

.nx-hero::before {
    content: '';
    position: absolute;
    inset: 0;
    background:
        radial-gradient(ellipse 60% 80% at 10% 50%, rgba(0,212,255,0.06) 0%, transparent 60%),
        radial-gradient(ellipse 40% 60% at 90% 20%, rgba(240,165,0,0.05) 0%, transparent 60%);
    pointer-events: none;
}

.nx-hero::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent 0%, var(--cyan) 30%, var(--amber) 70%, transparent 100%);
    opacity: 0.5;
}

.nx-hero-tag {
    font-family: var(--font-mono);
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--cyan);
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.nx-hero-tag::before {
    content: '';
    display: inline-block;
    width: 20px; height: 1px;
    background: var(--cyan);
}

.nx-hero-title {
    font-family: var(--font-display);
    font-size: 3rem;
    font-weight: 800;
    letter-spacing: -0.01em;
    line-height: 1;
    margin: 0 0 14px 0;
    color: var(--ink-0);
}

.nx-hero-title span {
    -webkit-text-fill-color: transparent;
    background: linear-gradient(120deg, var(--cyan) 0%, #7bf5ff 40%, var(--amber) 100%);
    -webkit-background-clip: text;
    background-clip: text;
}

.nx-hero-sub {
    font-size: 0.95rem;
    color: var(--ink-2);
    font-weight: 400;
    line-height: 1.6;
    max-width: 580px;
    margin: 0;
}

.nx-hero-corner {
    position: absolute;
    top: 20px; right: 28px;
    font-family: var(--font-mono);
    font-size: 0.65rem;
    color: var(--ink-3);
    letter-spacing: 0.1em;
}

/* ── CARDS ── */
.nx-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-soft);
    border-radius: var(--radius-md);
    padding: 22px 24px;
    margin-bottom: 16px;
    box-shadow: var(--shadow-card);
    transition: border-color 0.25s ease, box-shadow 0.25s ease, transform 0.25s ease;
    position: relative;
    overflow: hidden;
}

.nx-card:hover {
    border-color: var(--border-hard);
    box-shadow: var(--shadow-cyan), var(--shadow-card);
    transform: translateY(-2px);
}

.nx-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: var(--cyan);
    opacity: 0;
    transition: opacity 0.25s ease;
}

.nx-card:hover::before { opacity: 1; }

/* ── METRIC CARDS ── */
.nx-metric {
    background: var(--bg-surface);
    border: 1px solid var(--border-soft);
    border-radius: var(--radius-md);
    padding: 20px 22px;
    transition: all 0.25s ease;
    position: relative;
    overflow: hidden;
}

.nx-metric::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 2px;
    opacity: 0;
    transition: opacity 0.3s ease;
}

.nx-metric-search::after  { background: var(--cyan); }
.nx-metric-reader::after  { background: var(--green); }
.nx-metric-writer::after  { background: var(--amber); }
.nx-metric-total::after   { background: var(--red); }

.nx-metric:hover::after { opacity: 1; }

.nx-metric-label {
    font-family: var(--font-mono);
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 6px;
}

.nx-metric-value {
    font-family: var(--font-display);
    font-size: 2.6rem;
    font-weight: 700;
    line-height: 1;
    letter-spacing: -0.02em;
    margin-bottom: 4px;
}

.nx-metric-unit {
    font-family: var(--font-mono);
    font-size: 0.75rem;
    color: var(--ink-2);
    font-weight: 400;
}

/* ── BADGE ── */
.nx-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 3px 10px 3px 8px;
    border-radius: 4px;
    font-family: var(--font-mono);
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

.nx-badge-cyan   { background: var(--cyan-subtle); color: var(--cyan); border: 1px solid rgba(0,212,255,0.2); }
.nx-badge-green  { background: var(--green-subtle); color: var(--green); border: 1px solid rgba(0,229,160,0.2); }
.nx-badge-amber  { background: var(--amber-subtle); color: var(--amber); border: 1px solid rgba(240,165,0,0.2); }
.nx-badge-red    { background: var(--red-subtle); color: var(--red); border: 1px solid rgba(255,64,96,0.2); }

.nx-badge::before {
    content: '';
    display: inline-block;
    width: 5px; height: 5px;
    border-radius: 50%;
    background: currentColor;
}

/* ── PIPELINE TRACKER ── */
.nx-pipeline {
    display: flex;
    align-items: center;
    gap: 0;
    padding: 24px 28px;
    background: var(--bg-surface);
    border: 1px solid var(--border-soft);
    border-radius: var(--radius-md);
    margin: 20px 0 28px 0;
    position: relative;
    overflow: hidden;
}

.nx-pipeline::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border-hard), transparent);
}

.nx-step {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    position: relative;
    z-index: 2;
}

.nx-step:not(:last-child)::after {
    content: '';
    position: absolute;
    top: 19px;
    left: 50%;
    width: 100%;
    height: 1px;
    background: var(--ink-3);
    transition: background 0.4s ease;
    z-index: 1;
}

.nx-step.done:not(:last-child)::after {
    background: var(--cyan);
    box-shadow: 0 0 8px var(--cyan-glow);
}

.nx-node {
    width: 38px; height: 38px;
    border-radius: 50%;
    border: 2px solid var(--ink-3);
    background: var(--bg-base);
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: var(--font-display);
    font-size: 0.8rem;
    font-weight: 700;
    color: var(--ink-2);
    transition: all 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
    position: relative;
    z-index: 2;
}

.nx-step.active .nx-node {
    border-color: var(--cyan);
    color: var(--cyan);
    background: var(--cyan-subtle);
    box-shadow: 0 0 0 5px var(--cyan-glow), 0 0 20px rgba(0,212,255,0.3);
    animation: nx-pulse 1.8s ease infinite;
}

.nx-step.done .nx-node {
    border-color: var(--green);
    background: rgba(0,229,160,0.12);
    color: var(--green);
    box-shadow: 0 0 12px rgba(0,229,160,0.25);
}

@keyframes nx-pulse {
    0%, 100% { box-shadow: 0 0 0 5px var(--cyan-glow), 0 0 20px rgba(0,212,255,0.3); }
    50%       { box-shadow: 0 0 0 9px rgba(0,212,255,0.06), 0 0 30px rgba(0,212,255,0.5); }
}

.nx-step-label {
    font-family: var(--font-mono);
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--ink-3);
    margin-top: 8px;
    transition: color 0.3s ease;
}

.nx-step.active .nx-step-label { color: var(--cyan); }
.nx-step.done   .nx-step-label { color: var(--green); }

/* ── TERMINAL ── */
.nx-terminal {
    background: var(--bg-void);
    border: 1px solid var(--border-soft);
    border-radius: var(--radius-md);
    padding: 18px 20px;
    font-family: var(--font-mono);
    font-size: 0.78rem;
    line-height: 1.9;
    color: var(--green);
    max-height: 240px;
    overflow-y: auto;
    position: relative;
}

.nx-terminal-bar {
    display: flex;
    align-items: center;
    gap: 6px;
    margin-bottom: 14px;
    padding-bottom: 12px;
    border-bottom: 1px solid var(--border-faint);
}

.nx-dot { width: 8px; height: 8px; border-radius: 50%; }
.nx-dot-r { background: #ff5f57; }
.nx-dot-y { background: #febc2e; }
.nx-dot-g { background: #28c840; }

.nx-term-title {
    font-family: var(--font-mono);
    font-size: 0.65rem;
    color: var(--ink-3);
    letter-spacing: 0.1em;
    margin-left: auto;
}

.nx-log-entry { display: flex; gap: 12px; }
.nx-log-time { color: var(--ink-3); flex-shrink: 0; }
.nx-log-agent { color: var(--cyan); flex-shrink: 0; }
.nx-log-msg { color: #64d982; }

/* ── REPORT VIEWER ── */
.nx-report {
    background: var(--bg-base);
    border: 1px solid var(--border-soft);
    border-radius: var(--radius-md);
    padding: 32px 36px;
}

.nx-report h1, .nx-report h2, .nx-report h3 {
    font-family: var(--font-display) !important;
    color: var(--ink-0) !important;
    letter-spacing: -0.01em;
}

.nx-report h2::before {
    content: '// ';
    color: var(--cyan);
    font-family: var(--font-mono);
    font-size: 0.85em;
}

/* ── SIDEBAR OVERRIDES ── */
.nx-sidebar-logo {
    font-family: var(--font-display);
    font-size: 1.3rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    color: var(--ink-0);
    padding: 8px 0 4px 0;
    display: flex;
    align-items: center;
    gap: 10px;
}

.nx-sidebar-logo span { color: var(--cyan); }

.nx-sidebar-section {
    font-family: var(--font-mono);
    font-size: 0.62rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--ink-3);
    padding: 6px 0 8px 0;
    border-bottom: 1px solid var(--border-faint);
    margin-bottom: 12px;
    z-index: 999
}

/* ── EMPTY STATE ── */
.nx-empty {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 72px 40px;
    background: var(--bg-surface);
    border: 1px dashed var(--border-soft);
    border-radius: var(--radius-lg);
    margin-top: 16px;
    text-align: center;
}

.nx-empty-icon {
    font-size: 2.4rem;
    margin-bottom: 16px;
    opacity: 0.35;
}

.nx-empty-title {
    font-family: var(--font-display);
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--ink-2);
    margin-bottom: 8px;
    letter-spacing: 0.02em;
}

.nx-empty-body {
    font-size: 0.85rem;
    color: var(--ink-3);
    line-height: 1.6;
    max-width: 380px;
}

/* ── DIVIDER ── */
.nx-rule {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border-soft) 30%, var(--border-soft) 70%, transparent);
    margin: 24px 0;
    border: none;
}

/* ── STREAMLIT COMPONENT OVERRIDES ── */
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, var(--cyan) 0%, #00a8cc 100%) !important;
    color: var(--bg-void) !important;
    font-family: var(--font-display) !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    padding: 10px 20px !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 20px rgba(0,212,255,0.25) !important;
}

[data-testid="stButton"] > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 30px rgba(0,212,255,0.4) !important;
}

[data-testid="stButton"][data-type="secondary"] > button {
    background: transparent !important;
    color: var(--ink-1) !important;
    border: 1px solid var(--border-soft) !important;
    box-shadow: none !important;
}

[data-testid="stButton"][data-type="secondary"] > button:hover {
    border-color: var(--border-hard) !important;
    color: var(--ink-0) !important;
    box-shadow: none !important;
}

[data-testid="stTextInput"] > div > div > input {
    background: var(--bg-surface) !important;
    border: 1px solid var(--border-soft) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--ink-0) !important;
    font-family: var(--font-mono) !important;
    font-size: 0.9rem !important;
    padding: 12px 14px !important;
}

[data-testid="stTextInput"] > div > div > input:focus {
    border-color: var(--border-hard) !important;
    box-shadow: 0 0 0 3px var(--cyan-glow) !important;
}

[data-testid="stTextInput"] > label {
    font-family: var(--font-mono) !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: var(--ink-2) !important;
}

[data-testid="stTextArea"] > div > textarea {
    background: var(--bg-void) !important;
    border: 1px solid var(--border-soft) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--ink-1) !important;
    font-family: var(--font-mono) !important;
    font-size: 0.82rem !important;
}

[data-testid="stTabs"] [role="tablist"] {
    border-bottom: 1px solid var(--border-soft) !important;
    gap: 4px !important;
}

[data-testid="stTabs"] button[role="tab"] {
    font-family: var(--font-mono) !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: var(--ink-2) !important;
    border-radius: var(--radius-sm) var(--radius-sm) 0 0 !important;
    padding: 8px 16px !important;
}

[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    color: var(--cyan) !important;
    border-bottom: 2px solid var(--cyan) !important;
}

[data-testid="stSelectbox"] > div > div,
[data-testid="stSlider"] > div,
[data-testid="stRadio"] > div {
    font-family: var(--font-body) !important;
    font-size: 0.9rem !important;
}

[data-testid="stMarkdownContainer"] p {
    color: var(--ink-1) !important;
    font-family: var(--font-body) !important;
}

[data-testid="stInfo"] {
    background: var(--cyan-subtle) !important;
    border: 1px solid rgba(0,212,255,0.15) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--ink-1) !important;
}

/* Tab status containers */
[data-testid="stStatusWidget"] {
    background: var(--bg-surface) !important;
    border: 1px solid var(--border-soft) !important;
    border-radius: var(--radius-sm) !important;
}

/* Download button */
[data-testid="stDownloadButton"] > button {
    background: var(--amber-subtle) !important;
    color: var(--amber) !important;
    border: 1px solid rgba(240,165,0,0.25) !important;
    font-family: var(--font-mono) !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.08em !important;
    border-radius: var(--radius-sm) !important;
    box-shadow: none !important;
}

[data-testid="stDownloadButton"] > button:hover {
    background: rgba(240,165,0,0.14) !important;
    box-shadow: 0 4px 16px var(--amber-glow) !important;
    transform: translateY(-1px) !important;
}

/* Checkbox */
[data-testid="stCheckbox"] label {
    font-family: var(--font-mono) !important;
    font-size: 0.8rem !important;
    color: var(--ink-1) !important;
}

/* Success message */
[data-testid="stAlert"] {
    background: var(--green-subtle) !important;
    border: 1px solid rgba(0,229,160,0.2) !important;
    border-radius: var(--radius-sm) !important;
}

/* Sidebar title text */
[data-testid="stSidebar"] h3 {
    font-family: var(--font-mono) !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    color: var(--ink-2) !important;
}

</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────
if "state" not in st.session_state:
    st.session_state.state = {
        "search_results": "",
        "reader_results": "",
        "report": "",
        "feedback": "",
        "logs": []
    }
if "is_researching" not in st.session_state:
    st.session_state.is_researching = False
if "execution_times" not in st.session_state:
    st.session_state.execution_times = {}
if "pipeline_step" not in st.session_state:
    st.session_state.pipeline_step = 0


# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────
def log_agent_activity(agent_name, message):
    timestamp = time.strftime("%H:%M:%S")
    st.session_state.state["logs"].append(f"[{timestamp}] [{agent_name}] {message}")


def render_pipeline_tracker(step, placeholder=None):
    stages = [
        ("01", "SEARCH"),
        ("02", "READER"),
        ("03", "WRITER"),
        ("04", "CRITIC"),
    ]
    html = '<div class="nx-pipeline">'
    for i, (num, label) in enumerate(stages, 1):
        if step == i:
            cls = "active"
        elif step > i:
            cls = "done"
            num = "✓"
        else:
            cls = ""
        html += (
            f'<div class="nx-step {cls}">'
            f'<div class="nx-node">{num}</div>'
            f'<div class="nx-step-label">{label}</div>'
            f'</div>'
        )
    html += '</div>'

    if placeholder:
        placeholder.markdown(html, unsafe_allow_html=True)
    else:
        st.markdown(html, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="nx-sidebar-logo">⬡ <span>NEXUS</span> AI</div>
    <div style="font-family: var(--font-mono); font-size:0.65rem; color: var(--ink-3); letter-spacing:0.1em; margin-bottom:24px;">
        MULTI-AGENT RESEARCH ENGINE · v2.0
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="nx-sidebar-section">⚙ Engine Config</div>', unsafe_allow_html=True)

    llm_provider = st.selectbox(
        "LLM Backend",
        ["Groq Cloud (Llama 3)", "Ollama Local (Mistral)", "OpenAI Client"],
        index=0
    )

    max_search_results = st.slider("Search Query Depth", min_value=2, max_value=12, value=6)
    deep_scrape_depth = st.radio(
        "Scrape Density",
        ["Standard Core Article", "High Intensive Parsing"],
        index=0
    )

    st.markdown('<hr class="nx-rule"/>', unsafe_allow_html=True)
    st.markdown('<div class="nx-sidebar-section">⬡ Pipeline</div>', unsafe_allow_html=True)
    st.info("4 autonomous agents orchestrated in sequence: Search → Read → Write → Critique.")

    st.markdown('<hr class="nx-rule"/>', unsafe_allow_html=True)

    if st.button("↺  Reset Environment", use_container_width=True, type="secondary"):
        st.session_state.state = {
            "search_results": "",
            "reader_results": "",
            "report": "",
            "feedback": "",
            "logs": []
        }
        st.session_state.execution_times = {}
        st.session_state.is_researching = False
        st.session_state.pipeline_step = 0
        st.rerun()


# ─────────────────────────────────────────────────────────────
# HERO BANNER
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="nx-hero">
    <div class="nx-hero-tag">Autonomous Intelligence · Multi-Agent Orchestration</div>
    <h1 class="nx-hero-title">NEXUS <span>Research</span> Engine</h1>
    <p class="nx-hero-sub">
        Define a topic. The pipeline deploys four specialized agents — search, scrape, synthesize, and critique —
        delivering a vetted intelligence report automatically.
    </p>
    <div class="nx-hero-corner">SYS_READY · BUILD 2.0.4</div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# INPUT ROW
# ─────────────────────────────────────────────────────────────
default_val = "Traditional RAG vs Agentic RAG" if not st.session_state.state["report"] else ""
topic = st.text_input(
    "TARGET RESEARCH TOPIC",
    placeholder="e.g., Traditional RAG vs Agentic RAG",
    value=default_val
)

start_research = st.button("⬡  Execute Autonomous Pipeline", type="primary", use_container_width=True)


# ─────────────────────────────────────────────────────────────
# PIPELINE EXECUTION
# ─────────────────────────────────────────────────────────────
if start_research and topic:
    st.session_state.is_researching = True
    st.session_state.state["logs"] = []
    start_total_time = time.time()

    visual_container = st.container()

    with visual_container:
        st.markdown("""
        <div style="font-family: var(--font-mono); font-size:0.68rem; letter-spacing:0.15em;
                    text-transform:uppercase; color: var(--cyan); margin: 20px 0 6px 0;">
            ⬡ Active Deployment
        </div>
        """, unsafe_allow_html=True)

        tracker_placeholder = st.empty()

        # ── STAGE 1: SEARCH ──
        st.session_state.pipeline_step = 1
        render_pipeline_tracker(1, tracker_placeholder)
        t0 = time.time()

        with st.status("⬡ Search Agent: Initiating web reconnaissance...", expanded=True) as status:
            log_agent_activity("SEARCH", f"Web recon for: '{topic}'")
            st.write("Generating optimal query parameters and dispatching requests...")

            search_agent = build_search_agent()
            search_results = search_agent.invoke(
                {"messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]}
            )
            raw_content = search_results['messages'][-1].content
            st.session_state.state["search_results"] = raw_content or "No search results retrieved."
            log_agent_activity("SEARCH", "Discovery metadata cached successfully.")
            status.update(label="✓ Search Agent: Complete", state="complete", expanded=False)

        st.session_state.execution_times["Search Agent"] = round(time.time() - t0, 2)

        # ── STAGE 2: READER ──
        st.session_state.pipeline_step = 2
        render_pipeline_tracker(2, tracker_placeholder)
        t0 = time.time()

        with st.status("⬡ Reader Agent: Parsing source documents...", expanded=True) as status:
            log_agent_activity("READER", "Evaluating high-yield index sources...")
            st.write("Resolving HTML to structured markdown, extracting tables and body content...")

            reader_agent = build_reader_agent()
            reader_results = reader_agent.invoke(
                {
                    "messages": [("user",
                        f"Based on the following search result about '{topic}', "
                        f"pick the most relevant URL and scrape it for deeper content.\n\n"
                        f"Search Result:\n{st.session_state.state['search_results'][:800]}"
                    )]
                }
            )
            raw_reader = reader_results['messages'][-1].content
            st.session_state.state["reader_results"] = raw_reader or "No scraping content extracted."
            log_agent_activity("READER", "Markdown extraction of source documents complete.")
            status.update(label="✓ Reader Agent: Complete", state="complete", expanded=False)

        st.session_state.execution_times["Reader Agent"] = round(time.time() - t0, 2)

        # ── STAGE 3: WRITER ──
        st.session_state.pipeline_step = 3
        render_pipeline_tracker(3, tracker_placeholder)
        t0 = time.time()

        with st.status("⬡ Writer Chain: Synthesizing intelligence report...", expanded=True) as status:
            log_agent_activity("WRITER", "Constructing research synthesis matrix...")
            st.write("Integrating reader output with search cache and formatting final report...")

            research_combined = (
                f"SEARCH RESULTS:\n{st.session_state.state['search_results']}\n\n"
                f"DETAILED SCRAPED CONTENT:\n{st.session_state.state['reader_results']}"
            )
            writer_result = writer_chain.invoke({"topic": topic, "research": research_combined})
            st.session_state.state["report"] = writer_result or "Error generating report."
            log_agent_activity("WRITER", "First draft compiled and formatted.")
            status.update(label="✓ Writer Chain: Complete", state="complete", expanded=False)

        st.session_state.execution_times["Writer Chain"] = round(time.time() - t0, 2)

        # ── STAGE 4: CRITIC ──
        st.session_state.pipeline_step = 4
        render_pipeline_tracker(4, tracker_placeholder)
        t0 = time.time()

        with st.status("⬡ Critic Chain: Running quality audit...", expanded=True) as status:
            log_agent_activity("CRITIC", "Validating citations, structure, and clarity...")
            st.write("Auditing structural alignment, factual consistency, and editorial quality...")

            feedback_result = critic_chain.invoke({"report": st.session_state.state['report']})
            st.session_state.state["feedback"] = feedback_result or "No feedback received."
            log_agent_activity("CRITIC", "Audit complete. Review finalized.")
            status.update(label="✓ Critic Chain: Complete", state="complete", expanded=False)

        st.session_state.execution_times["Critic Chain"] = round(time.time() - t0, 2)

    st.session_state.execution_times["Total Duration"] = round(time.time() - start_total_time, 2)
    st.session_state.pipeline_step = 5
    st.session_state.is_researching = False

    render_pipeline_tracker(5, tracker_placeholder)
    st.success("⬡ Pipeline execution complete. Results mapped below.")


# ─────────────────────────────────────────────────────────────
# RESULTS DASHBOARD
# ─────────────────────────────────────────────────────────────
if st.session_state.state["report"]:

    # ── TELEMETRY ROW ──
    st.markdown("""
    <div style="font-family: var(--font-mono); font-size:0.68rem; letter-spacing:0.15em;
                text-transform:uppercase; color: var(--ink-2); margin: 28px 0 10px 0;">
        ⬡ Engine Telemetry
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="nx-metric nx-metric-search">
            <div class="nx-metric-label" style="color:var(--cyan);">
                <span class="nx-badge nx-badge-cyan">Search</span>
            </div>
            <div class="nx-metric-value" style="color:var(--cyan);">{st.session_state.execution_times.get('Search Agent','—')}</div>
            <div class="nx-metric-unit">seconds · web recon</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="nx-metric nx-metric-reader">
            <div class="nx-metric-label">
                <span class="nx-badge nx-badge-green">Reader</span>
            </div>
            <div class="nx-metric-value" style="color:var(--green);">{st.session_state.execution_times.get('Reader Agent','—')}</div>
            <div class="nx-metric-unit">seconds · html parse</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="nx-metric nx-metric-writer">
            <div class="nx-metric-label">
                <span class="nx-badge nx-badge-amber">Writer</span>
            </div>
            <div class="nx-metric-value" style="color:var(--amber);">{st.session_state.execution_times.get('Writer Chain','—')}</div>
            <div class="nx-metric-unit">seconds · synthesis</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="nx-metric nx-metric-total">
            <div class="nx-metric-label">
                <span class="nx-badge nx-badge-red">Total</span>
            </div>
            <div class="nx-metric-value" style="color:var(--red);">{st.session_state.execution_times.get('Total Duration','—')}</div>
            <div class="nx-metric-unit">seconds · full loop</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<hr class="nx-rule"/>', unsafe_allow_html=True)

    # ── TABS ──
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "  REPORT  ",
        "  AUDIT  ",
        "  SEARCH CACHE  ",
        "  SCRAPE DATA  ",
        "  EVENT LOG  ",
    ])

    with tab1:
        st.markdown("""
        <div style="font-family:var(--font-mono); font-size:0.68rem; letter-spacing:0.12em;
                    text-transform:uppercase; color:var(--ink-2); margin-bottom:16px;">
            ⬡ Compiled Intelligence Report
        </div>
        """, unsafe_allow_html=True)

        enable_editor = st.checkbox("⬡ Enable Manual Document Editor")
        if enable_editor:
            corrected_input = st.text_area(
                "LIVE EDITOR", st.session_state.state["report"], height=560
            )
            if corrected_input != st.session_state.state["report"]:
                st.session_state.state["report"] = corrected_input
                st.toast("Document updated.")
        else:
            st.markdown('<div class="nx-report">', unsafe_allow_html=True)
            st.markdown(st.session_state.state["report"])
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<hr class="nx-rule"/>', unsafe_allow_html=True)

        doc_topic = topic if topic else "nexus_research"
        st.download_button(
            label="⬡  Download as Markdown",
            data=st.session_state.state["report"],
            file_name=f"{doc_topic.lower().replace(' ', '_')}_report.md",
            mime="text/markdown",
            use_container_width=True
        )

    with tab2:
        st.markdown("""
        <div style="font-family:var(--font-mono); font-size:0.68rem; letter-spacing:0.12em;
                    text-transform:uppercase; color:var(--ink-2); margin-bottom:16px;">
            ⬡ Editorial Critique & Action Items
        </div>
        """, unsafe_allow_html=True)
        st.markdown(
            '<div class="nx-card" style="border-left: 3px solid var(--red); padding-left:22px;">',
            unsafe_allow_html=True
        )
        st.markdown(st.session_state.state["feedback"])
        st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown("""
        <div style="font-family:var(--font-mono); font-size:0.68rem; letter-spacing:0.12em;
                    text-transform:uppercase; color:var(--ink-2); margin-bottom:16px;">
            ⬡ Discoveries Cached by Search Agent
        </div>
        """, unsafe_allow_html=True)
        st.text_area("SEARCH BUFFER", value=st.session_state.state["search_results"], height=450, disabled=True)

    with tab4:
        st.markdown("""
        <div style="font-family:var(--font-mono); font-size:0.68rem; letter-spacing:0.12em;
                    text-transform:uppercase; color:var(--ink-2); margin-bottom:16px;">
            ⬡ HTML Extraction by Reader Agent
        </div>
        """, unsafe_allow_html=True)
        st.text_area("SCRAPE BUFFER", value=st.session_state.state["reader_results"], height=450, disabled=True)

    with tab5:
        st.markdown("""
        <div style="font-family:var(--font-mono); font-size:0.68rem; letter-spacing:0.12em;
                    text-transform:uppercase; color:var(--ink-2); margin-bottom:16px;">
            ⬡ Kernel Event Stream
        </div>
        """, unsafe_allow_html=True)

        bar_html = (
            '<div class="nx-terminal">'
            '<div class="nx-terminal-bar">'
            '<span class="nx-dot nx-dot-r"></span>'
            '<span class="nx-dot nx-dot-y"></span>'
            '<span class="nx-dot nx-dot-g"></span>'
            '<span class="nx-term-title">nexus-kernel · event log</span>'
            '</div>'
        )
        for entry in st.session_state.state["logs"]:
            # Parse: [HH:MM:SS] [AGENT] message
            parts = entry.split("] ", 2)
            ts = parts[0].replace("[", "") if len(parts) > 0 else ""
            ag = parts[1].replace("[", "") if len(parts) > 1 else ""
            msg = parts[2] if len(parts) > 2 else entry
            bar_html += (
                f'<div class="nx-log-entry">'
                f'<span class="nx-log-time">{ts}</span>'
                f'<span class="nx-log-agent">[{ag}]</span>'
                f'<span class="nx-log-msg">{msg}</span>'
                f'</div>'
            )
        bar_html += '</div>'
        st.markdown(bar_html, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# EMPTY STATE
# ─────────────────────────────────────────────────────────────
elif not start_research and not st.session_state.state["report"]:
    st.markdown("""
    <div class="nx-empty">
        <div class="nx-empty-icon">⬡</div>
        <div class="nx-empty-title">System Standby</div>
        <div class="nx-empty-body">
            Define a research topic in the field above and click
            <strong style="color:var(--cyan);">Execute Autonomous Pipeline</strong>
            to engage all four agents.
        </div>
    </div>
    """, unsafe_allow_html=True)