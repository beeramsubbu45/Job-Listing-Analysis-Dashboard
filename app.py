"""Streamlit dashboard for the Job Listings Analytics project."""
from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "processed_jobs.csv"

st.set_page_config(page_title="Job Listings Analytics", page_icon="💼", layout="wide")

@st.cache_data

def load_data():
    if not DATA.exists():
        return pd.DataFrame()
    return pd.read_csv(DATA, parse_dates=["posted_date"])


df = load_data()

st.sidebar.title("💼 Job Analytics")
page = st.sidebar.radio("Navigate", ["Home", "Dataset Viewer", "Summary Statistics", "Filtering & Search", "Interactive Charts", "Business Insights", "Download"])

if df.empty:
    st.error("Processed dataset not found. Run: python src/data_cleaning.py and python src/feature_engineering.py")
    st.stop()

if page == "Home":
    st.title("💼 Job Listings Analytics Dashboard")
    st.write("Interactive analysis of a scraped job-listings dataset using Python, Pandas, Matplotlib, Seaborn and Streamlit.")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Jobs", f"{len(df):,}")
    c2.metric("Companies", f"{df['company_name'].nunique():,}")
    c3.metric("Categories", f"{df['job_category'].nunique():,}")
    c4.metric("Avg. Min Salary", f"${df['salary_min'].mean():,.0f}")
    st.subheader("Project Workflow")
    st.markdown("**Scraping → Cleaning → Feature Engineering → Statistical Analysis → EDA → Streamlit Dashboard → Business Insights**")
    st.info("The bundled data is a learning/demo dataset based on the static Fake Python practice site. Run the scraper to refresh it from the source.")

elif page == "Dataset Viewer":
    st.title("Dataset Viewer")
    st.dataframe(df, use_container_width=True, height=600)
    st.write(f"Rows: **{len(df)}** | Columns: **{len(df.columns)}**")

elif page == "Summary Statistics":
    st.title("Summary Statistics")
    st.subheader("Head")
    st.dataframe(df.head(10), use_container_width=True)
    st.subheader("Descriptive Statistics")
    st.dataframe(df.describe(include="all").transpose(), use_container_width=True)
    st.subheader("Value Counts")
    col = st.selectbox("Choose a categorical column", ["job_category", "experience_level", "work_mode", "salary_category", "region"])
    st.dataframe(df[col].value_counts().rename("count"), use_container_width=True)

elif page == "Filtering & Search":
    st.title("Filtering & Search")
    categories = st.multiselect("Job Category", sorted(df.job_category.unique()), default=sorted(df.job_category.unique()))
    modes = st.multiselect("Work Mode", sorted(df.work_mode.unique()), default=sorted(df.work_mode.unique()))
    experiences = st.multiselect("Experience Level", sorted(df.experience_level.unique()), default=sorted(df.experience_level.unique()))
    keyword = st.text_input("Search title/company/description")
    min_salary = st.slider("Minimum salary", int(df.salary_min.min()), int(df.salary_min.max()), int(df.salary_min.min()), step=1000)
    filtered = df[df.job_category.isin(categories) & df.work_mode.isin(modes) & df.experience_level.isin(experiences) & (df.salary_min >= min_salary)].copy()
    if keyword:
        mask = filtered.astype(str).apply(lambda s: s.str.contains(keyword, case=False, na=False)).any(axis=1)
        filtered = filtered[mask]
    st.metric("Matching Jobs", len(filtered))
    st.dataframe(filtered, use_container_width=True, height=550)

elif page == "Interactive Charts":
    st.title("Interactive Charts")
    chart = st.selectbox("Chart", ["Jobs by Category", "Average Salary by Category", "Jobs by Work Mode", "Salary Distribution", "Experience Distribution", "Category × Work Mode"])
    if chart == "Jobs by Category":
        st.bar_chart(df.job_category.value_counts())
    elif chart == "Average Salary by Category":
        s = df.groupby("job_category")["salary_min"].mean().sort_values(ascending=False)
        st.bar_chart(s)
    elif chart == "Jobs by Work Mode":
        st.bar_chart(df.work_mode.value_counts())
    elif chart == "Salary Distribution":
        st.line_chart(df.salary_min.sort_values().reset_index(drop=True))
    elif chart == "Experience Distribution":
        st.bar_chart(df.experience_level.value_counts())
    else:
        pivot = pd.crosstab(df.job_category, df.work_mode)
        st.dataframe(pivot, use_container_width=True)
        st.bar_chart(pivot)

elif page == "Business Insights":
    st.title("Business Insights")
    top_category = df.job_category.value_counts().idxmax()
    top_mode = df.work_mode.value_counts().idxmax()
    highest_paid = df.groupby("job_category")["salary_min"].mean().idxmax()
    python_share = df["python_required"].mean() * 100
    st.success(f"**{top_category}** is the largest job category in the current dataset.")
    st.info(f"**{top_mode}** is the most common work mode in the current dataset.")
    st.warning(f"**{highest_paid}** has the highest average minimum salary among categories.")
    st.write(f"About **{python_share:.1f}%** of the bundled job descriptions contain the keyword Python.")
    st.subheader("Decision-oriented observations")
    st.markdown("- Recruiters can use category and experience filters to identify concentrated talent demand.\n- Salary comparisons help prioritize high-value roles.\n- Work-mode distributions can support workforce planning.\n- Keyword frequency can indicate technical skill demand.")

elif page == "Download":
    st.title("Download Processed Dataset")
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download processed_jobs.csv", csv, "processed_jobs.csv", "text/csv")
    st.download_button("⬇️ Download filtered CSV", df.to_csv(index=False).encode("utf-8"), "job_listings_export.csv", "text/csv")
