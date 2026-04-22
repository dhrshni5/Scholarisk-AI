import streamlit as st
import pickle
import numpy as np

# Load model
model = pickle.load(open("model.pkl", "rb"))

st.set_page_config(page_title="Scholarisk", page_icon="🎓", layout="wide")

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 2.8rem;
        max-width: 1150px;
    }
    
    .section-card {
        background: color-mix(in srgb, var(--background-color) 92%, var(--text-color) 8%);
        border: 1px solid color-mix(in srgb, var(--text-color) 16%, transparent);
        border-radius: 16px;
        padding: 1rem 1rem 0.7rem 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 8px 20px color-mix(in srgb, var(--text-color) 10%, transparent);
    }

    [data-testid="stSidebar"] {
        border-right: 1px solid rgba(120, 120, 120, 0.22);
    }

    [data-testid="stMetric"] {
        background: color-mix(in srgb, var(--background-color) 88%, var(--text-color) 12%);
        border: 1px solid color-mix(in srgb, var(--text-color) 20%, transparent);
        border-radius: 14px;
        padding: 0.85rem 1rem;
        box-shadow: 0 4px 14px color-mix(in srgb, var(--text-color) 14%, transparent);
    }

    [data-testid="stMetricLabel"] {
        font-weight: 600;
    }

    [data-testid="stMetricValue"] {
        color: var(--text-color);
    }

    [data-testid="stProgressBar"] {
        margin-top: 0.45rem;
    }

    h1, h2, h3 {
        letter-spacing: 0.2px;
    }
    
    h1 {
        font-weight: 800;
    }
    
    h2, h3 {
        font-weight: 700;
    }

    p, li {
        line-height: 1.45;
    }

    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
        border: 1px solid rgba(120, 120, 120, 0.25);
        padding: 0.55rem 0.9rem;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 16px color-mix(in srgb, var(--text-color) 12%, transparent);
    }

    [data-testid="stAlert"] {
        border-radius: 12px;
        border: 1px solid color-mix(in srgb, var(--text-color) 18%, transparent);
    }

    /* Slightly cleaner spacing in sidebar controls */
    [data-testid="stSidebar"] [data-testid="stSlider"] {
        padding-top: 0.2rem;
        padding-bottom: 0.35rem;
    }

    [data-testid="stSidebar"] .stCaption {
        opacity: 0.85;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🎓 Scholarisk")
st.caption("AI-powered Student Risk Intelligence System")
st.divider()

with st.sidebar:
    st.header("📥 Input Parameters")
    st.caption("Tune inputs for your personalized risk analysis.")
    st.caption("Sleep Hours - Hours of sleep per day")
    sleep = st.slider("Sleep Hours", 0, 10, 5)
    st.caption("Study Hours - Focused academic study time")
    study = st.slider("Study Hours", 0, 10, 5)
    st.caption("Screen Time - Non-stop screen exposure in hours")
    screen = st.slider("Screen Time (hrs)", 0, 10, 5)
    st.caption("Stress Level - Daily stress intensity")
    stress = st.slider("Stress Level (1-10)", 1, 10, 5)
    st.caption("Breaks per Day - Recovery breaks taken")
    breaks = st.slider("Breaks per Day", 0, 10, 3)
    st.caption("Motivation Level - Current drive to perform")
    motivation = st.slider("Motivation Level (1-10)", 1, 10, 5)
    analyze = st.button("Analyze My Life", use_container_width=True)

if not analyze:
    st.info("👈 Adjust your parameters and click Analyze")
else:

    # ML Prediction
    input_data = np.array([[sleep, study, screen, stress, breaks, motivation]])
    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]
    # Risk Score Calculation
    risk_score = (
    (10 - sleep) * 2 +
    stress * 2 +
    screen +
    (10 - motivation) * 2 +
    (10 - study)
    )

    risk_score = min(100, risk_score)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    with st.container():
        st.subheader("📊 Overall Risk Score")
        score_col, status_col = st.columns([1, 1])
        with score_col:
            st.metric("Risk Score", f"{risk_score}/100")
            st.progress(risk_score / 100)
        with status_col:
            if risk_score > 70:
                st.error("🔴 High Risk Zone")
            elif risk_score > 40:
                st.warning("🟡 Medium Risk Zone")
            else:
                st.success("🟢 Low Risk Zone")
    st.markdown("</div>", unsafe_allow_html=True)

    st.divider()

    left_col, right_col = st.columns(2)

    with left_col:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        with st.container():
            st.write("### 🔥 Burnout Result")
            if prediction == 1:
                st.error(f"⚠️ High Burnout Risk ({round(probability*100)}%)")
            else:
                st.success(f"✅ Low Burnout Risk ({round((1-probability)*100)}%)")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        with st.container():
            st.write("### 🧠 Why this result?")
            reasons = []

            if sleep < 5:
                reasons.append("Low sleep reduces recovery")

            if stress > 7:
                reasons.append("High stress increases burnout risk")

            if screen > 6:
                reasons.append("Excess screen time reduces focus")

            if motivation < 4:
                reasons.append("Low motivation affects consistency")

            if study < 3:
                reasons.append("Insufficient study time impacts performance")
            if reasons:
                for r in reasons:
                    st.write(f"- {r}")
            else:
                st.write("- No major risk signals detected from the selected inputs.")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        with st.container():
            st.write("### 🧬 Student Type")
            if stress > 7 and sleep < 5:
                st.write("🔥 The Overloaded Achiever")
            elif motivation < 4 and study < 3:
                st.write("😴 The Unmotivated Drifter")
            elif study > 6 and stress < 5:
                st.write("🎯 The Focused Performer")
            elif screen > 7:
                st.write("📱 The Distracted Explorer")
            else:
                st.write("Balanced student")
        st.markdown("</div>", unsafe_allow_html=True)

    with right_col:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        with st.container():
            st.write("### 🚨 Top Risk Factors")
            risks = []

            if sleep < 5:
                risks.append("Low Sleep")
            if screen > 6:
                risks.append("High Screen Time")
            if stress > 7:
                risks.append("High Stress")
            if motivation < 4:
                risks.append("Low Motivation")

            for r in risks[:2]:
                st.write(f"- **{r}**")
            if not risks:
                st.write("- No top risk factors detected.")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        with st.container():
            st.write("### 🎯 Priority Action")
            if sleep < 6:
                st.write("- Increase sleep to at least 7 hours")

            if screen > 5:
                st.write("- Reduce screen time by 20–30%")

            if stress > 6:
                st.write("- Practice relaxation (walk, music, meditation)")

            if motivation < 5:
                st.write("- Break tasks into smaller goals")

            if study < 4:
                st.write("- Follow structured study plan (Pomodoro)")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        with st.container():
            st.write("### 🔮 Future Insight")
            if risk_score > 70:
                st.error("⚠️ If this pattern continues, high chance of burnout within weeks")
            elif risk_score > 40:
                st.warning("⚠️ You may face performance drop if habits don’t improve")
            else:
                st.success("✅ You are on a sustainable path")
        st.markdown("</div>", unsafe_allow_html=True)

    st.divider()

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    with st.container():
        st.write("### ⚠️ Rule-based Risks")
        has_rule_risk = False

        if sleep < 5:
            st.warning("⚠️ Low Sleep Detected → Can cause fatigue")
            has_rule_risk = True

        if motivation < 4:
            st.warning("⚠️ Low Motivation → Productivity issue")
            has_rule_risk = True

        if study < 3:
            st.warning("⚠️ Low Study Time → Academic risk")
            has_rule_risk = True

        if screen > 6:
            st.warning("⚠️ High Screen Time → Distraction risk")
            has_rule_risk = True

        if stress > 7:
            st.warning("⚠️ High Stress → Mental overload")
            has_rule_risk = True

        if not has_rule_risk:
            st.success("✅ No immediate rule-based risk flags at current levels.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    with st.container():
        st.write("### 📅 Daily Recovery Plan")
        plan = []

        if sleep < 6:
            plan.append("🛌 Sleep at least 7–8 hours")

        if study < 4:
            plan.append("📚 Study in 25-min focused sessions (Pomodoro)")

        if screen > 6:
            plan.append("📵 Reduce screen time by 2 hours")

        if stress > 6:
            plan.append("🧘 Take 15 mins break (walk/meditation)")

        if motivation < 5:
            plan.append("🎯 Set 3 small achievable goals today")

        if plan:
            for p in plan:
                st.write(f"- {p}")
        else:
            st.write("✅ Maintain your current routine!")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    with st.container():
        st.write("### ⚖️ Current vs Ideal")
        current_col, ideal_col = st.columns(2)
        with current_col:
            st.write("**Your Current State:**")
            st.write(f"- Sleep: {sleep} hrs")
            st.write(f"- Study: {study} hrs")
            st.write(f"- Stress: {stress}/10")
        with ideal_col:
            st.write("**Ideal Recommended State:**")
            st.write("- Sleep: 7–8 hrs")
            st.write("- Study: 5–6 hrs")
            st.write("- Stress: below 5")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    with st.container():
        st.write("### 🔄 Improvement Simulation")
        st.write("### 💡 Recommendations")
        made_reco = False

        if sleep < 6:
            st.write("- Increase sleep to at least 7 hours")
            made_reco = True

        if screen > 5:
            st.write("- Reduce screen time by 20–30%")
            made_reco = True

        if stress > 6:
            st.write("- Practice relaxation (walk, music, meditation)")
            made_reco = True

        if motivation < 5:
            st.write("- Break tasks into smaller goals")
            made_reco = True

        if study < 4:
            st.write("- Follow structured study plan (Pomodoro)")
            made_reco = True

        if not made_reco:
            st.write("✅ Maintain your current routine!")
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)