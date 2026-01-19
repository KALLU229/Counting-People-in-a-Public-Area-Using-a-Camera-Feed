import streamlit as st
import plotly.express as px
from db import get_detections, get_counter_history


def dashboard():
    # Custom CSS - Clean & Modern LIGHT MODE
    st.markdown("""
    <style>
        /* Light background with subtle gradient */
        .stApp {
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        }

        /* Headers */
        h1, h2, h3 {
            color: #1e40af !important;
            font-family: 'Segoe UI', system-ui, sans-serif;
        }

        /* Metrics */
        [data-testid="stMetricValue"] {
            font-size: 2.6rem !important;
            font-weight: 800;
            color: #1d4ed8;
        }
        [data-testid="stMetricLabel"] {
            font-size: 1.15rem !important;
            color: #475569;
            font-weight: 500;
        }

        /* Subtle divider */
        hr {
            background: linear-gradient(to right, transparent, #cbd5e1, transparent);
            height: 1px;
            border: none;
            margin: 2.4rem 0;
        }

        /* Card style - clean white with soft shadow */
        .card {
            padding: 1.6rem;
            border-radius: 16px;
            background: white;
            border: 1px solid #e2e8f0;
            box-shadow: 0 8px 25px -8px rgba(0,0,0,0.08);
            margin-bottom: 1.8rem;
        }

        /* Better Plotly chart appearance */
        .js-plotly-plot {
            border-radius: 12px !important;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0,0,0,0.06);
        }
    </style>
    """, unsafe_allow_html=True)

    # ================= TITLE =================
    st.markdown("""
        <div style="text-align:center; padding: 2rem 0 1.5rem;">
            <h1 style="margin:0; font-size:3.4rem; font-weight:800; letter-spacing:-0.5px; color:#1e40af;">
                Crowd Monitoring Dashboard
            </h1>
            <p style="color:#64748b; font-size:1.25rem; margin-top:0.6rem; font-weight:400;">
                Real-time People Counting & Space Occupancy Analytics
            </p>
        </div>
    """, unsafe_allow_html=True)

    # ================= LOAD DATA =================
    with st.spinner("Fetching latest crowd data..."):
        detections = get_detections()
        history = get_counter_history()

    if history.empty:
        st.warning("No data recorded yet. Waiting for the first detections...", icon="⏳")
        st.stop()

    latest = history.iloc[-1]

    # ================= METRICS - Card style =================
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.metric("TOTAL ENTERED", f"{int(latest['entered']):,}")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.metric("TOTAL EXITED", f"{int(latest['exited']):,}")
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        inside = int(latest["inside"])
        delta = None
        if len(history) >= 2:
            prev = int(history.iloc[-2]["inside"])
            delta = inside - prev
        st.metric("CURRENTLY INSIDE", f"{inside:,}", delta)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # ================= ROW 1 =================
    r1c1, r1c2 = st.columns([5, 5])

    with r1c1:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        bar_df = {
            "Category": ["Entered", "Exited", "Inside"],
            "Count": [latest["entered"], latest["exited"], latest["inside"]]
        }

        fig_bar = px.bar(
            bar_df,
            x="Category",
            y="Count",
            color="Category",
            color_discrete_map={
                "Entered": "#16a34a",
                "Exited": "#dc2626",
                "Inside": "#2563eb"
            },
            title="<b>Current Crowd Snapshot</b>",
            text_auto=True
        )

        fig_bar.update_traces(textfont_size=14, textposition="auto")
        fig_bar.update_layout(
            title_x=0.5,
            showlegend=False,
            margin=dict(l=20, r=20, t=60, b=30),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(size=13, color="#1e293b")
        )

        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with r1c2:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        fig_line = px.line(
            history,
            x="timestamp",
            y="inside",
            title="<b>Occupancy Trend Over Time</b>",
            markers=True,
            template="plotly_white"
        )

        fig_line.update_traces(
            line=dict(color="#2563eb", width=3.2),
            marker=dict(size=7, color="#2563eb", line=dict(width=1.5, color="white"))
        )

        fig_line.update_layout(
            title_x=0.5,
            xaxis_title="",
            yaxis_title="People Inside",
            margin=dict(l=20, r=20, t=60, b=30),
            hovermode="x unified",
            font=dict(size=13, color="#1e293b")
        )

        st.plotly_chart(fig_line, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # ================= ROW 2 =================
    r2c1, r2c2 = st.columns([5, 5])

    with r2c1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        if detections.empty:
            st.info("Heatmap will appear once person detections are available.", icon="🔍")
        else:
            fig_heat = px.density_heatmap(
                detections,
                x="x",
                y="y",
                nbinsx=60,
                nbinsy=60,
                color_continuous_scale="YlOrRd",
                title="<b>People Density Heatmap</b>",
                template="plotly_white"
            )

            fig_heat.update_layout(
                title_x=0.5,
                margin=dict(l=20, r=20, t=60, b=30),
                font=dict(size=13, color="#1e293b")
            )

            st.plotly_chart(fig_heat, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with r2c2:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        history["flow_balance"] = history["entered"] - history["exited"]

        fig_area = px.area(
            history,
            x="timestamp",
            y="flow_balance",
            title="<b>Net Flow Balance (+In / −Out)</b>",
            template="plotly_white"
        )

        fig_area.update_traces(
            line=dict(color="#7c3aed", width=2.8),
            fillcolor="rgba(124, 58, 237, 0.18)"
        )

        fig_area.update_layout(
            title_x=0.5,
            xaxis_title="",
            yaxis_title="Net Flow",
            margin=dict(l=20, r=20, t=60, b=30),
            hovermode="x unified",
            font=dict(size=13, color="#1e293b")
        )

        st.plotly_chart(fig_area, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)