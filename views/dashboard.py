import streamlit as st
import plotly.express as px
from db import get_detections, get_counter_history


def dashboard():
    # ================= TITLE =================
    st.markdown(
        """
        <h1 style="text-align:center; font-weight:800;">
            Crowd Monitoring Dashboard
        </h1>
        """,
        unsafe_allow_html=True
    )

    # ================= LOAD DATA =================
    detections = get_detections()
    history = get_counter_history()

    if history.empty:
        st.warning("No data available yet")
        return

    latest = history.iloc[-1]

    # ================= METRICS =================
    col1, col2, col3 = st.columns(3)
    col1.metric("ENTERED", int(latest["entered"]))
    col2.metric("EXITED", int(latest["exited"]))
    col3.metric("INSIDE", int(latest["inside"]))

    st.markdown("---")

    # ================= ROW 1 =================
    row1_col1, row1_col2 = st.columns(2)

    # -------- BAR GRAPH --------
    with row1_col1:
        bar_df = {
            "Type": ["Entered", "Exited", "Inside"],
            "Count": [
                latest["entered"],
                latest["exited"],
                latest["inside"]
            ]
        }

        fig_bar = px.bar(
            bar_df,
            x="Type",
            y="Count",
            color="Type",
            color_discrete_map={
                "Entered": "#2ECC71",
                "Exited": "#E74C3C",
                "Inside": "#3498DB"
            },
            title="<b>Current Crowd Status</b>",
            text_auto=True
        )

        fig_bar.update_layout(
            title_x=0.5,
            font=dict(size=14)
        )

        st.plotly_chart(fig_bar, use_container_width=True)

    # -------- LINE GRAPH --------
    with row1_col2:
        fig_line = px.line(
            history,
            x="timestamp",
            y="inside",
            title="<b>Crowd Growth Trend Over Time</b>",
            markers=True
        )

        fig_line.update_traces(
            line=dict(color="#3498DB", width=3)
        )

        fig_line.update_layout(
            title_x=0.5,
            xaxis_title="Time",
            yaxis_title="People Inside",
            font=dict(size=14)
        )

        st.plotly_chart(fig_line, use_container_width=True)

    st.markdown("---")

    # ================= ROW 2 =================
    row2_col1, row2_col2 = st.columns(2)

    # -------- HEATMAP --------
    with row2_col1:
        if detections.empty:
            st.info("Heatmap will appear once detections are available")
        else:
            fig_heat = px.density_heatmap(
                detections,
                x="x",
                y="y",
                nbinsx=60,
                nbinsy=60,
                color_continuous_scale="Turbo",
                title="<b>People Density & Movement Heatmap</b>"
            )

            fig_heat.update_layout(
                title_x=0.5,
                font=dict(size=14)
            )

            st.plotly_chart(fig_heat, use_container_width=True)

    # -------- FLOW BALANCE --------
    with row2_col2:
        history["flow_balance"] = history["entered"] - history["exited"]

        fig_area = px.area(
            history,
            x="timestamp",
            y="flow_balance",
            title="<b>Net Crowd Flow Balance</b>",
            labels={
                "timestamp": "Time",
                "flow_balance": "Net Flow (+In / −Out)"
            }
        )

        fig_area.update_traces(
            line=dict(color="#9B59B6"),
            fillcolor="rgba(155, 89, 182, 0.4)"
        )

        fig_area.update_layout(
            title_x=0.5,
            xaxis_title="Time",
            yaxis_title="Net People Flow",
            font=dict(size=14)
        )

        st.plotly_chart(fig_area, use_container_width=True)
