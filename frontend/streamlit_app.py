import sys
import hashlib
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

import streamlit as st

from app.chains.sql_chain import sql_chain
from app.database.schema_loader import get_schema
from app.database.query_executor import execute_query
from app.database.database_manager import get_databases

from app.services.sql_validator import validate_sql
from app.services.chart_selector import detect_chart_type
from app.services.insight_generator import generate_insights

from frontend.components.charts import create_chart


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Natural Language SQL Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Natural Language SQL Analytics")

st.caption(
    "Ask questions in plain English and get SQL, results, visualizations, and AI insights."
)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("Database Selection")

try:

    databases = get_databases()

    selected_db = st.sidebar.selectbox(
        "Choose Database",
        databases
    )

    st.sidebar.success(
        f"Connected to: {selected_db}"
    )

except Exception as e:

    st.sidebar.error(
        f"Database Error: {str(e)}"
    )

    st.stop()

# --------------------------------------------------
# USER QUESTION
# --------------------------------------------------

question = st.text_input(
    "Ask a question",
    placeholder="Example: Show revenue by customer region"
)

# --------------------------------------------------
# GENERATE BUTTON
# --------------------------------------------------

if st.button("Generate", type="primary"):

    if not question.strip():

        st.warning(
            "Please enter a question."
        )

        st.stop()

    try:

        # ------------------------------------------
        # LOAD SCHEMA
        # ------------------------------------------

        with st.spinner("Loading schema..."):

            schema = get_schema(
                selected_db
            )

        # ------------------------------------------
        # GENERATE SQL
        # ------------------------------------------

        with st.spinner("Generating SQL..."):

            sql = sql_chain.invoke(
                {
                    "question": question,
                    "schema": schema
                }
            )

        # ------------------------------------------
        # SHOW SQL
        # ------------------------------------------

        st.subheader("Generated SQL")

        st.code(
            sql,
            language="sql"
        )

        # ------------------------------------------
        # SCHEMA ERROR
        # ------------------------------------------

        if sql.strip() == "SCHEMA_ERROR":

            st.error(
                "The selected database schema does not contain enough information to answer this question."
            )

            st.stop()

        # ------------------------------------------
        # VALIDATE SQL
        # ------------------------------------------

        valid, message = validate_sql(sql)

        if not valid:

            st.error(
                f"SQL Validation Failed: {message}"
            )

            st.stop()

        # ------------------------------------------
        # EXECUTE QUERY
        # ------------------------------------------

        with st.spinner("Executing query..."):

            df = execute_query(
                sql,
                selected_db
            )

        # ------------------------------------------
        # RESULTS
        # ------------------------------------------

        st.subheader("Results")

        if df.empty:

            st.info(
                "No records found."
            )

            st.stop()

        st.dataframe(
            df,
            use_container_width=True
        )

        # ------------------------------------------
        # CHART + INSIGHTS
        # ------------------------------------------

        col1, col2 = st.columns([2, 1])

        # -----------------------------
        # VISUALIZATION
        # -----------------------------

        with col1:

            chart_info = detect_chart_type(df)

            if chart_info:

                chart = create_chart(
                    df,
                    chart_info
                )

                st.subheader("Visualization")

                chart_key = hashlib.md5(
                    f"{selected_db}_{sql}".encode()
                ).hexdigest()

                st.plotly_chart(
                    chart,
                    use_container_width=True,
                    key=f"plot_{chart_key}"
                )

            else:

                st.info(
                    "No suitable visualization available."
                )

        # -----------------------------
        # AI INSIGHTS
        # -----------------------------

        with col2:

            st.subheader("AI Insights")

            with st.spinner(
                "Generating insights..."
            ):

                insights = generate_insights(
                    question,
                    df
                )

            st.markdown(
                insights
            )

        # ------------------------------------------
        # DOWNLOAD CSV
        # ------------------------------------------

        csv = df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="📥 Download Results CSV",
            data=csv,
            file_name="query_results.csv",
            mime="text/csv"
        )

    except Exception as e:

        st.error(
            f"Error: {str(e)}"
        )