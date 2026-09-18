import streamlit as st
from datetime import date

from report import generate_report


# ==================================================
# STREAMLIT PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Sports Complex Reports",
    page_icon="📊",
    layout="wide"
)


# ==================================================
# TITLE
# ==================================================

st.title("Sports Complex Business Reports")

st.write(
    "Generate automated monthly and annual management reports."
)


# ==================================================
# REPORT TYPE
# ==================================================

report_type = st.radio(
    "Select Report Type",
    ["Monthly Report", "Annual Report"],
    horizontal=True
)


# ==================================================
# MONTHLY REPORT
# ==================================================

if report_type == "Monthly Report":

    st.subheader("Monthly Report")

    col1, col2 = st.columns(2)


    # -----------------------------
    # MONTH
    # -----------------------------

    with col1:

        month = st.selectbox(
            "Select Month",
            range(1, 13),
            format_func=lambda x:
                date(2000, x, 1).strftime("%B")
        )


    # -----------------------------
    # YEAR
    # -----------------------------

    with col2:

        year = st.selectbox(
            "Select Year",
            range(2025, 2028)
        )


    # Display selected report
    month_name = date(
        year,
        month,
        1
    ).strftime("%B")


    st.info(
        f"Selected report: **{month_name} {year}**"
    )


    # ==================================================
    # GENERATE BUTTON
    # ==================================================

    if st.button(
        "Generate Monthly Report",
        type="primary"
    ):

        with st.spinner(
            "Running SQL queries and generating report..."
        ):

            html = generate_report(
                report_type="monthly",
                year=year,
                month=month
            )


        st.success(
            f"{month_name} {year} report generated!"
        )


        # ==================================================
        # SHOW HTML REPORT
        # ==================================================

        st.components.v1.html(
            html,
            height=900,
            scrolling=True
        )


        # ==================================================
        # DOWNLOAD HTML
        # ==================================================

        st.download_button(
            "Download HTML Report",
            data=html,
            file_name=f"{year}_{month:02d}_monthly_report.html",
            mime="text/html"
        )


# ==================================================
# ANNUAL REPORT
# ==================================================

else:

    st.subheader("Annual Report")


    # -----------------------------
    # YEAR
    # -----------------------------

    year = st.selectbox(
        "Select Year",
        range(2025, 2028)
    )


    st.info(
        f"Selected report: **{year} Annual Report**"
    )


    # ==================================================
    # GENERATE BUTTON
    # ==================================================

    if st.button(
        "Generate Annual Report",
        type="primary"
    ):

        with st.spinner(
            "Running SQL queries and generating report..."
        ):

            html = generate_report(
                report_type="annual",
                year=year
            )


        st.success(
            f"{year} annual report generated!"
        )


        # ==================================================
        # SHOW HTML
        # ==================================================

        st.components.v1.html(
            html,
            height=900,
            scrolling=True
        )


        # ==================================================
        # DOWNLOAD HTML
        # ==================================================

        st.download_button(
            "Download HTML Report",
            data=html,
            file_name=f"{year}_annual_report.html",
            mime="text/html"
        )