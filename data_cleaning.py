"""Clean and standardize the raw job-listings dataset."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
RAW = DATA_DIR / "raw_jobs.csv"
CLEAN = DATA_DIR / "cleaned_jobs.csv"

RENAME_MAP = {
    "Job Title": "job_title", "Company Name": "company_name", "Location": "location",
    "Job Description": "job_description", "Posted Date": "posted_date", "Apply Link": "apply_link",
}


def clean_data(path=RAW):
    df = pd.read_csv(path)
    df = df.rename(columns={c: RENAME_MAP.get(c, c) for c in df.columns})
    required = ["job_title", "company_name", "location", "job_description", "posted_date", "apply_link"]
    for col in required:
        if col not in df.columns:
            df[col] = ""

    for col in ["job_title", "company_name", "location", "job_description", "apply_link"]:
        df[col] = df[col].fillna("").astype(str).str.strip()

    # Remove exact duplicates and fill missing text with an explicit value.
    df = df.drop_duplicates().reset_index(drop=True)
    df["job_title"] = df["job_title"].replace("", "Unknown Job")
    df["company_name"] = df["company_name"].replace("", "Unknown Company")
    df["location"] = df["location"].replace("", "Unknown Location")
    df["job_description"] = df["job_description"].replace("", "No description available")
    df["posted_date"] = pd.to_datetime(df["posted_date"], errors="coerce")
    df["posted_date"] = df["posted_date"].fillna(pd.Timestamp("2021-04-08"))

    # Location normalization.
    df["location"] = df["location"].str.replace(r"\s+", " ", regex=True)
    df["city"] = df["location"].str.rsplit(",", n=1).str[0].str.strip()
    df["region"] = df["location"].str.rsplit(",", n=1).str[-1].str.strip()

    df.to_csv(CLEAN, index=False)
    return df


if __name__ == "__main__":
    cleaned = clean_data()
    print(cleaned.info())
    print(f"Saved {len(cleaned)} cleaned records -> {CLEAN}")
