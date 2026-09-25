import streamlit as st
from datetime import date

from report import generate_report


# PAGE CONFIG
st.set_page_config(
    page_title="Sports Complex Reports",
    page_icon="",
    layout="wide"
)



# GLOBAL STYLES
st.markdown(
    """
    <style>
        :root {
            --bg: #EEF0F4;
            --surface: #F9FAFB;
            --text-primary: #1F2937;
            --text-secondary: #6B7280;
            --border: #E5E7EB;
            --primary: #2563EB;
            --primary-hover: #1D4ED8;
        }

        html, body, [class*="css"] {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI",
                         Roboto, Helvetica, Arial, sans-serif;
        }

        .stApp {
            background-color: var(--bg);
        }

        /* ---------------- SIDEBAR ---------------- */
        section[data-testid="stSidebar"] {
            background-color: var(--surface);
            border-right: 1px solid var(--border);
        }
        section[data-testid="stSidebar"] > div {
            padding: 1.5rem 1.25rem;
        }

        .sidebar-brand {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 1.05rem;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 1.75rem;
        }
        .sidebar-brand .dot {
            width: 10px;
            height: 10px;
            border-radius: 3px;
            background-color: var(--primary);
            display: inline-block;
        }

        .sidebar-eyebrow {
            font-size: 0.7rem;
            font-weight: 600;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .sidebar-heading {
            font-size: 1.05rem;
            font-weight: 600;
            color: var(--text-primary);
            margin: 0.15rem 0 0.25rem 0;
        }
        .sidebar-subtext {
            font-size: 0.82rem;
            color: var(--text-secondary);
            margin-bottom: 1.25rem;
            line-height: 1.35;
        }

        .section-label {
            font-size: 0.75rem;
            font-weight: 600;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.04em;
            margin: 1rem 0 0.4rem 0;
        }

        .period-box {
            border-top: 1px solid var(--border);
            margin-top: 1.1rem;
            padding-top: 0.9rem;
        }
        .period-box .label {
            font-size: 0.75rem;
            color: var(--text-secondary);
            margin-bottom: 0.15rem;
        }
        .period-box .value {
            font-size: 1rem;
            font-weight: 600;
            color: var(--text-primary);
        }

        /* ---------------- MAIN AREA ---------------- */
        .block-container {
            padding-top: 2.5rem;
            padding-bottom: 3rem;
        }

        .report-heading {
            margin-bottom: 1rem;
        }
        .report-heading .eyebrow {
            font-size: 0.78rem;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.04em;
            margin-bottom: 0.25rem;
        }
        .report-heading .title {
            font-size: 1.3rem;
            font-weight: 600;
            color: var(--text-primary);
        }

        .status-line {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.88rem;
            color: #15803D;
            font-weight: 500;
            margin: 0.5rem 0 1.25rem 0;
        }

        .report-frame {
            background-color: var(--surface);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 0.5rem;
            box-shadow: 0 1px 2px rgba(16, 24, 40, 0.03);
            margin-bottom: 1.25rem;
        }

        .empty-state {
            background-color: var(--surface);
            border: 1px dashed var(--border);
            border-radius: 10px;
            padding: 3rem 1.5rem;
            text-align: center;
            color: var(--text-secondary);
        }
        .empty-state .title {
            font-size: 1.05rem;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 0.35rem;
        }

        /* Buttons */
        .stButton > button {
            border-radius: 8px;
            font-weight: 500;
            padding: 0.55rem 1.1rem;
            border: 1px solid var(--border);
        }
        .stButton > button[kind="primary"] {
            background-color: var(--primary);
            border: 1px solid var(--primary);
            color: #fff;
            width: 100%;
        }
        .stButton > button[kind="primary"]:hover {
            background-color: var(--primary-hover);
            border: 1px solid var(--primary-hover);
        }

        .stDownloadButton > button {
            background-color: var(--surface);
            border: 1px solid var(--border);
            border-radius: 8px;
            color: var(--text-primary);
            font-weight: 500;
        }
        .stDownloadButton > button:hover {
            border-color: var(--primary);
            color: var(--primary);
        }

        /* Force light theme on inputs regardless of user's Streamlit theme */
        div[data-baseweb="select"] > div {
            border-radius: 8px !important;
            border-color: var(--border) !important;
            background-color: var(--surface) !important;
            color: var(--text-primary) !important;
        }
        div[data-baseweb="select"] span,
        div[data-baseweb="select"] div {
            color: var(--text-primary) !important;
        }
        /* Dropdown menu that pops out (rendered in a portal) */
        ul[data-testid="stSelectboxVirtualDropdown"] {
            background-color: var(--surface) !important;
        }
        ul[data-testid="stSelectboxVirtualDropdown"] li {
            color: var(--text-primary) !important;
        }

        div[role="radiogroup"] {
            gap: 0.5rem;
        }
        div[role="radiogroup"] label,
        div[role="radiogroup"] label p,
        div[role="radiogroup"] label span {
            color: var(--text-primary) !important;
            opacity: 1 !important;
        }

        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] p {
            color: var(--text-primary) !important;
        }

        #MainMenu, header, footer {
            visibility: hidden;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# SIDEBAR — REPORT CONFIGURATION
with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-brand">
            <span class="dot"></span> QuantaSights
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="sidebar-eyebrow">Reports</div>
        <div class="sidebar-heading">Generate Business Report</div>
        <div class="sidebar-subtext">
            Select the time period and get your detailed business report.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="section-label">Report Type</div>', unsafe_allow_html=True)
    report_type = st.radio(
        "Report type",
        ["Monthly Report", "Annual Report"],
        label_visibility="collapsed"
    )

    if report_type == "Monthly Report":

        st.markdown('<div class="section-label">Year</div>', unsafe_allow_html=True)
        year = st.selectbox(
            "Year",
            range(2026, 2027),
            label_visibility="collapsed"
        )

        st.markdown('<div class="section-label">Month</div>', unsafe_allow_html=True)
        month = st.selectbox(
            "Month",
            range(1, 13),
            format_func=lambda x: date(2000, x, 1).strftime("%B"),
            label_visibility="collapsed"
        )

        month_name = date(year, month, 1).strftime("%B")
        period_label = f"{month_name} {year}"
        file_name = f"{year}_{month:02d}_monthly_report.html"

    else:

        st.markdown('<div class="section-label">Year</div>', unsafe_allow_html=True)
        year = st.selectbox(
            "Year",
            range(2025, 2028),
            label_visibility="collapsed"
        )

        period_label = f"{year} Annual Report"
        file_name = f"{year}_annual_report.html"

    st.markdown(
        f"""
        <div class="period-box">
            <div class="label">Report period</div>
            <div class="value">{period_label}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")
    generate_clicked = st.button("Generate Report →", type="primary")


# ============================================================
# MAIN AREA — REPORT PREVIEW
# ============================================================
if generate_clicked:

    if report_type == "Monthly Report":
        with st.spinner("Running SQL queries and generating report..."):
            html = generate_report(
                report_type="monthly",
                year=year,
                month=month
            )
    else:
        with st.spinner("Running SQL queries and generating report..."):
            html = generate_report(
                report_type="annual",
                year=year
            )

    st.markdown(
        f"""
        <div class="report-heading">
            <div class="eyebrow">{period_label}</div>
            <div class="title">Management Report</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="status-line">✓ Generated successfully</div>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="report-frame">', unsafe_allow_html=True)
    st.components.v1.html(
        html,
        height=900,
        scrolling=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.download_button(
        "Download HTML Report",
        data=html,
        file_name=file_name,
        mime="text/html"
    )

else:

    st.markdown(
        """
        <div class="empty-state">
            <div class="title">No report generated yet</div>
            <div>Choose a report type and period in the sidebar, then click "Generate Report".</div>
        </div>
        """,
        unsafe_allow_html=True
    )