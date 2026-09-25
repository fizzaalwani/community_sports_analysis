from pathlib import Path
from datetime import date
from dateutil.relativedelta import relativedelta

import pandas as pd
from sqlalchemy import create_engine
from jinja2 import Environment, FileSystemLoader



# DATABASE
engine = create_engine(
    "mysql+pymysql://root:fizza@localhost/SportsComplexDW"
)



# DATE RANGE FOR MONTHLY REPORT
def get_month_dates(year, month):

    # First day of selected month
    month_start = date(year, month, 1)

    # First day of next month
    month_end = month_start + relativedelta(months=1)

    # First day of previous month
    previous_start = month_start - relativedelta(months=1)

    return month_start, month_end, previous_start



# RUN MONTHLY SQL QUERIES
def run_queries(year, month):

    # Get dates for selected month
    month_start, month_end, previous_start = get_month_dates(
        year,
        month
    )

    # This dictionary will contain every SQL result
    results = {}

    # Main SQL folder
    sql_root = Path("sql")

    # Loop through folders :
    for section_folder in sql_root.iterdir():

        # Ignore files; only process folders
        if not section_folder.is_dir():
            continue

        section = section_folder.name

        # Create dictionary for this section
        results[section] = {}

        # Find every .sql file inside the folder
        for sql_file in section_folder.glob("*.sql"):

            # Example:
            # kpis.sql -> kpis

            query_name = sql_file.stem

            # Read SQL file
            query = sql_file.read_text(
                encoding="utf-8"
            )

            # Replace placeholders in SQL
            query = query.format(
                year=year,
                month=month,
                month_start=month_start,
                month_end=month_end,
                previous_start=previous_start
            )

            # Execute SQL
            df = pd.read_sql(
                query,
                engine
            )

            # Store result
            results[section][query_name] = df

    return results



# RUN ANNUAL SQL QUERIES
def run_annual_queries(year):

    results = {}

    # SQL folder specifically for annual queries
    sql_root = Path("sql/annual")

    # If annual folder doesn't exist,
    # return an empty dictionary
    if not sql_root.exists():
        return results

    # Find every annual SQL query
    for sql_file in sql_root.glob("*.sql"):

        query_name = sql_file.stem

        # Read SQL
        query = sql_file.read_text(
            encoding="utf-8"
        )

        # Give SQL the selected year
        query = query.format(
            year=year
        )

        # Execute SQL
        df = pd.read_sql(
            query,
            engine
        )

        # Store result
        results[query_name] = df

    return results


def generate_report_text(results, report_month):


    # EXECUTIVE
    kpis = results["executive"]["kpis"].iloc[0]
    growth = results["executive"]["monthly_growth"].iloc[0]

    total_members = int(kpis["total_members"])
    active_members = int(kpis["active_members"])
    new_members = int(kpis["new_members"])

    august_visits = int(growth["august_visits"] or 0)
    july_visits = int(growth["july_visits"] or 0)

    visit_growth = float(growth["visit_growth_percentage"] or 0)

    august_revenue = float(growth["august_revenue"] or 0)
    july_revenue = float(growth["july_revenue"] or 0)

    revenue_growth = float(growth["revenue_growth_percentage"] or 0)



    # EXECUTIVE SUMMARY
    if visit_growth > 0:
        activity_direction = "increased"
    elif visit_growth < 0:
        activity_direction = "declined"
    else:
        activity_direction = "remained stable"

    if revenue_growth > 0:
        revenue_direction = "increased"
    elif revenue_growth < 0:
        revenue_direction = "declined"
    else:
        revenue_direction = "remained stable"


    executive_summary = (
        f"At the end of {report_month}, the sports complex had "
        f"{total_members:,} registered members, including "
        f"{active_members:,} active members. During the month, "
        f"{new_members:,} new members joined the facility."
    )

    activity_summary = (
        f"Member activity {activity_direction} by "
        f"{abs(visit_growth):.2f}% compared with the previous month, "
        f"with {august_visits:,} visits recorded in {report_month} "
        f"compared with {july_visits:,} visits in the previous month."
    )

    revenue_summary = (
        f"Revenue {revenue_direction} by "
        f"{abs(revenue_growth):.2f}% compared with the previous month, "
        f"generating PKR {august_revenue:,.0f} during the reporting period."
    )


    # -----------------------------------
    # MEMBERSHIP
    # -----------------------------------
    renewal = results["memberships"]["renewal"].iloc[0]

    renewal_rate = float(renewal["renewal_rate"] or 0)
    expiring = int(renewal["memberships_expiring"])

    membership_summary = (
        f"The complex currently has {active_members:,} active members "
        f"out of {total_members:,} registered members. "
        f"{new_members:,} new members joined during the reporting period."
    )

    renewal_summary = (
        f"{expiring:,} memberships were identified as expiring during "
        f"the reporting period. The recorded renewal rate was "
        f"{renewal_rate:.1f}%."
    )


    # -----------------------------------
    # ENGAGEMENT
    # -----------------------------------

    engagement_levels = results["engagement"]["engagement_level"]
    visitor_types = results["engagement"]["by_visitor_type"]

    regular = engagement_levels[
        engagement_levels["engagement_level"] == "Regular"
    ]

    regular_percentage = (
        float(regular.iloc[0]["percentage"])
        if not regular.empty
        else 0
    )

    engagement_summary = (
        f"The largest engagement group was Regular members, representing "
        f"{regular_percentage:.2f}% of the members included in the "
        f"engagement analysis."
    )


    # -----------------------------------
    # FACILITIES
    # -----------------------------------

    facility_usage = results["facility"]["visits"]

    if not facility_usage.empty:

        top_facility = facility_usage.iloc[0]

        facility_summary = (
            f"{top_facility['facility_name'].title()} was the most-used "
            f"facility during the reporting period, recording "
            f"{int(top_facility['total_visits'] or 0):,} visits and accounting for "
            f"{float(top_facility['percentage_of_total_visits'] or 0):.2f}% "
            f"of total facility visits."
        )

    else:

        facility_summary = (
            "No facility usage data was available for the reporting period."
        )


    # -----------------------------------
    # PEAK USAGE
    # -----------------------------------

    # busiest_day = results["engagement"]["busiest_day_of_month"].iloc[0]

    busiest_day_df = results["engagement"]["busiest_day_of_month"]

    print("========== BUSIEST DAY DEBUG ==========")
    print(busiest_day_df)
    print("Rows:", len(busiest_day_df))
    print("Columns:", busiest_day_df.columns.tolist())
    print("=======================================")

    if not busiest_day_df.empty:
        busiest_day = busiest_day_df.iloc[0]
    else:
        busiest_day = None

    print("FACILITY RESULTS:", results["facility"].keys())

    # busiest_hour = results["facility"]["busiest_hour"].iloc[0]
    busiest_hour_df = results["facility"]["busiest_hour"]

    if not busiest_hour_df.empty:
        busiest_hour = busiest_hour_df.iloc[0]
    else:
        busiest_hour = None

    peak_usage_summary = (
        f"The busiest day was {busiest_day['day_name']}, "
        f"{busiest_day['full_date']}, with "
        f"{int(busiest_day['total_visits']):,} visits. "
        f"Across the entire reporting period, the highest activity hour was "
        f"{int(busiest_hour['hour_of_day'])}:00, recording "
        f"{int(busiest_hour['total_visits']):,} visits."
    )


    utilization_df = results['facility']['utilization']

    utilization_lines = []

    if not utilization_df.empty:
        for _, row in utilization_df.iterrows():
            facility_name = row["facility_name"].title()
            utilization = float(row["utilization"] or 0)

            utilization_lines.append( 
                f"{facility_name}: {utilization:.2f}% utilization"
                )
        facility_utilization_summary = (
        "Facility utilization during the reporting period was as follows: "
        + "; ".join(utilization_lines)
        + "."
    )
    else:
        facility_utilization_summary = (
            "No facility utilization data was available for the reporting period."
        )



    # -----------------------------------
    # WEEKDAY / WEEKEND
    # -----------------------------------

    week_type = results["engagement"]["by_week_type"]

    weekday = week_type[
        week_type["period_type"] == "Weekday"
    ].iloc[0]

    weekend = week_type[
        week_type["period_type"] == "Weekend"
    ].iloc[0]

    usage_pattern_summary = (
        f"Weekdays generated {int(weekday['total_visits']):,} visits "
        f"from {int(weekday['unique_members']):,} unique members, "
        f"while weekends generated {int(weekend['total_visits']):,} visits "
        f"from {int(weekend['unique_members']):,} unique members."
    )



    # REVENUE
    membership_revenue = results["revenue"]["membership_revenue"]

    top_revenue_type = membership_revenue.iloc[
        membership_revenue["revenue"].argmax()
    ]

    revenue_detail = (
        f"The {top_revenue_type['membership_type']} membership category "
        f"generated the highest revenue during the reporting period, "
        f"contributing PKR {float(top_revenue_type['revenue']):,.0f} "
        f"across {int(top_revenue_type['payment_transactions']):,} "
        f"transactions."
    )


    # INACTIVE MEMBERS
    inactive_members = results["engagement"]["inactive_members"]

    inactive_count = len(inactive_members)

    if inactive_count == 0:
        inactive_summary = (
            "No inactive members were identified during the reporting period "
            "based on the available visit activity data."
        )
    else:
        inactive_summary = (
            f"{inactive_count:,} inactive members were identified as requiring "
            f"attention based on the available visit activity data. "
            f"These members may be candidates for targeted engagement or "
            f"follow-up."
        )


    # RECOMMENDATIONS
    recommendations = []

    if revenue_growth < 0:
        recommendations.append(
            f"Review the decline in monthly revenue of "
            f"{abs(revenue_growth):.2f}% and examine membership-level "
            f"payment patterns for possible causes."
        )

    if renewal_rate == 0 and expiring > 0:
        recommendations.append(
            f"Prioritize follow-up with the {expiring:,} memberships "
            f"identified as expiring, as no renewals were recorded "
            f"in the current dataset."
        )

    if inactive_count > 0:
        recommendations.append(
            f"Consider a targeted re-engagement campaign for the "
            f"{inactive_count:,} members identified with limited recent "
            f"attendance."
        )

    if weekend["total_visits"] < weekday["total_visits"]:
        recommendations.append(
            "Weekday activity was higher than weekend activity. "
            "Management could evaluate whether additional weekday "
            "programming or promotions could further support utilization."
        )

    recommendations.append(
        f"Monitor the busiest usage period around "
        f"{int(busiest_hour['hour_of_day'])}:00 to ensure facility "
        f"capacity and staffing are aligned with demand."
    )

    print("____________________________________________")
    print(results['facility']['utilization'])


    return {
        "executive_summary": executive_summary,
        "activity_summary": activity_summary,
        "revenue_summary": revenue_summary,

        "membership_summary": membership_summary,
        "renewal_summary": renewal_summary,

        "engagement_summary": engagement_summary,

        "facility_summary": facility_summary,
         "facility_utilization_summary": facility_utilization_summary,

        "peak_usage_summary": peak_usage_summary,
        "usage_pattern_summary": usage_pattern_summary,

        "revenue_detail": revenue_detail,

        "inactive_summary": inactive_summary,

        "recommendations": recommendations,
    }



def generate_report(
    report_type,
    year,
    month=None
):

   
    # MONTHLY REPORT
    if report_type == "monthly":

        # Run all monthly SQL queries
        results = run_queries(
            year,
            month
        )

        # Example:
        # year = 2026
        # month = 8
        # report_month = "August 2026"

        report_month = date(
            year,
            month,
            1
        ).strftime("%B %Y")



        # GENERATE NARRATIVE TEXT
        report_text = generate_report_text(
            results,
            report_month
        )


        # PREPARE DATA FOR JINJA2
        report_data = {

            "report_type": "Monthly",

            "report_month": report_month,

          
            # EXECUTIVE
            "kpis":
                results["executive"]["kpis"].iloc[0],

            "growth":
                results["executive"]["monthly_growth"].iloc[0],


            # ENGAGEMENT
            "engagement_levels":
                results["engagement"]["engagement_level"]
                .to_dict("records"),

            "visitor_types":
                results["engagement"]["by_visitor_type"]
                .to_dict("records"),

            "frequent_members":
                results["engagement"]["frequent_members"]
                .to_dict("records"),

            "inactive_members":
                results["engagement"]["inactive_members"]
                .to_dict("records"),


            # FACILITY
            "facility_usage":
                results["facility"]["visits"]
                .to_dict("records"),

            "facility_comparison":
                results["facility"]["monthly_visit_comparison"]
                .to_dict("records"),

            "gender_facilities":
                results["facility"]["most_used_by_gender"]
                .to_dict("records"),

            "age_facilities":
                results["facility"]["usage_by_age_group"]
                .to_dict("records"),


            # USAGE PATTERNS
            "week_type":
                results["engagement"]["by_week_type"]
                .to_dict("records"),

            "busiest_day": (
                results["engagement"]["busiest_day_of_month"].iloc[0]
                if not results["engagement"]["busiest_day_of_month"].empty
                else None
            ),

            "busiest_hour":
                results["facility"]["busiest_hour"]
                .iloc[0] if not results["facility"]["busiest_hour"].empty
                else None,

            # REVENUE
            "membership_revenue":
                results["revenue"]["membership_revenue"]
                .to_dict("records"),

            "membership_engagement":
                results["memberships"]["avg_visit_per_member"]
                .to_dict("records"),


            # GENERATED NARRATIVE

            **report_text
        }


  
    # ANNUAL REPORT


    elif report_type == "annual":

        results = run_annual_queries(
            year
        )

        report_data = {

            "report_type": "Annual",

            "report_month": str(year),

            "results": results
        }



    # INVALID REPORT TYPE
    else:

        raise ValueError(
            "report_type must be 'monthly' or 'annual'"
        )


    # LOAD JINJA2 TEMPLATE
    env = Environment(
        loader=FileSystemLoader("templates")
    )

    template = env.get_template(
        "monthly_report.html"
    )


    # GENERATE HTML
    print("REPORT DATA KEYS:")
    print(report_data.keys())

    print("KPIS:")
    print(report_data.get("kpis"))

    html = template.render(
        **report_data
    )

    return html

