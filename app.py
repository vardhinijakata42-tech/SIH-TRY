
import streamlit as st
from PIL import Image
from gate1_metadata import analyze_metadata
from gate2_ocr import analyze_ocr
from gate3_face import biometric_demo

st.set_page_config(
    page_title="DETECT-X | Secure Verification",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
.stApp {
    background:
      radial-gradient(circle at 10% 5%, rgba(91,52,190,.24), transparent 28%),
      radial-gradient(circle at 90% 15%, rgba(0,255,210,.12), transparent 26%),
      #060811;
    color: #f4f7ff;
}
.block-container {max-width: 1250px; padding: 2rem 2.5rem 4rem;}
.hero {
    border: 1px solid #5fffe0; border-radius: 20px; padding: 26px 30px;
    background: linear-gradient(125deg, rgba(36,26,76,.95), rgba(10,20,43,.96));
    box-shadow: 0 0 35px rgba(95,255,224,.16), inset 0 0 30px rgba(155,70,255,.08);
}
.hero h1 {margin:0; font-size:34px; letter-spacing:1px;}
.terminal {font-family:monospace; color:#63ffd9; margin-top:9px;}
.card {
    border:1px solid rgba(122,91,255,.72); border-radius:16px; padding:20px;
    background:rgba(17,18,40,.78); box-shadow:0 0 22px rgba(118,74,255,.10);
}
.gate {
    border:1px solid rgba(94,255,224,.35); border-left:4px solid #63ffd9;
    border-radius:12px; padding:16px 18px; margin:10px 0;
    background:rgba(13,20,36,.88);
}
.gate h4 {margin:0 0 4px 0;}
.muted {color:#9aa6c5; font-size:13px;}
.status {float:right; font-family:monospace; font-weight:800; color:#63ffd9;}
div.stButton > button {
    width:100%; border:1px solid #63ffd9; border-radius:10px;
    background:linear-gradient(90deg,#14233a,#29184d); color:white; font-weight:700;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <h1>🛡️ DETECT-X: PROTOCOL TERMINAL</h1>
  <div class="terminal">// ACTIVE PIPELINE // GATES 1–5 SECURE VERIFICATION SUITE</div>
</div>
""", unsafe_allow_html=True)

st.write("")
c1, c2, c3 = st.columns([1, 1.2, 1])
with c1:
    registry = st.selectbox("TARGET REGISTRY", [
        "Aadhaar • Demo Registry",
        "Passport • Demo Registry",
        "Visa • Demo Registry",
        "Student ID • Demo Registry"
    ])
with c2:
    uploaded = st.file_uploader("VERIFICATION MEDIA", type=["png","jpg","jpeg"])
with c3:
    st.metric("PIPELINE", "GATES 1–5")
    st.caption("Demo / non-sensitive sample only")

if not uploaded:
    st.markdown("""
    <div class="card" style="text-align:center;margin-top:25px;padding:55px;">
      <h2>◈ SYSTEM STANDBY</h2>
      <p class="muted">Upload a non-sensitive sample image to initialize the verification pipeline.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

image = Image.open(uploaded).convert("RGB")

st.markdown("### ◈ VERIFICATION PIPELINE")
p = st.progress(0, text="INITIALIZING SECURE PIPELINE...")
p.progress(20, text="GATE 1 // METADATA & PIXEL ANALYSIS")
gate1 = analyze_metadata(image)
p.progress(45, text="GATE 2 // OCR & TEXT VALIDATION")
ocr_text = st.text_area("OCR INPUT • DEMO", placeholder="Paste OCR output here if you want to test a format rule.")
gate2 = analyze_ocr(ocr_text)
p.progress(70, text="GATE 3 // BIOMETRIC INTEGRATION")
selfie = st.file_uploader("SELFIE • OPTIONAL DEMO", type=["png","jpg","jpeg"], key="selfie")
gate3 = biometric_demo(selfie)
p.progress(90, text="GATE 4 // LAYOUT CONSISTENCY")
gate4 = {"status": "READY", "detail": "Layout engine placeholder ready for template rules."}
p.progress(100, text="GATE 5 // RISK SYNTHESIS COMPLETE")

a, b = st.columns([1, 1])
with a:
    st.markdown('<div class="card"><h3>◈ SOURCE MEDIA</h3>', unsafe_allow_html=True)
    st.image(image, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
with b:
    st.markdown('<div class="card"><h3>◈ GATE MATRIX</h3>', unsafe_allow_html=True)
    gates = [
        ("01", "METADATA & TEXTURAL ANALYSIS", gate1["status"], gate1["detail"]),
        ("02", "OCR & TEXT VALIDATION", gate2["status"], gate2["detail"]),
        ("03", "IDENTITY BIOMETRICS", gate3["status"], gate3["detail"]),
        ("04", "LAYOUT CONSISTENCY", gate4["status"], gate4["detail"]),
        ("05", "RISK SYNTHESIS", "COMPLETE", "Signals aggregated for review routing."),
    ]
    for num, title, status, detail in gates:
        st.markdown(f"""
        <div class="gate">
          <h4>GATE {num} // {title} <span class="status">{status}</span></h4>
          <div class="muted">{detail}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

signals = 0
signals += gate1.get("review", False)
signals += gate2.get("review", False)
signals += gate3.get("review", False)

st.markdown("### ◈ RISK SYNTHESIS")
if signals >= 2:
    st.error("🔴 HIGH REVIEW SIGNAL • MANUAL VERIFICATION RECOMMENDED")
elif signals == 1:
    st.warning("🟡 MEDIUM REVIEW SIGNAL • SECONDARY CHECK RECOMMENDED")
else:
    st.success("🟢 LOW REVIEW SIGNAL • NO STRONG PROTOTYPE FLAGS")

with st.expander("TECHNICAL TRACE"):
    st.json({
        "registry": registry,
        "gate_1": gate1,
        "gate_2": gate2,
        "gate_3": gate3,
        "gate_4": gate4,
    })

st.caption("DEMO ONLY • Heuristic signals and placeholders. Do not upload real Aadhaar/passport data. This prototype does not authenticate identity or prove fraud.")
