"""Create analytical features and demonstrate label/one-hot encoding."""
from pathlib import Path
import re
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
INPUT = DATA_DIR / "cleaned_jobs.csv"
OUTPUT = DATA_DIR / "processed_jobs.csv"


def classify_category(title: str) -> str:
    t = title.lower()
    groups = {
        "Technology": ["python", "developer", "programmer", "software", "database", "systems", "engineer", "web", "applications", "technical"],
        "Healthcare": ["nurse", "doctor", "surgeon", "scientist", "medical", "clinical", "psychologist", "therapist", "radiographer", "optician", "physician", "health"],
        "Finance": ["trader", "banker", "insurance", "underwriter", "loss adjuster", "broker", "equities", "bonds", "futures"],
        "Creative & Media": ["designer", "writer", "editor", "photographer", "producer", "journalist", "media", "printmaker", "television", "radio", "graphic"],
        "Legal": ["legal", "barrister", "conveyancer"],
        "Education": ["teacher", "librarian", "language", "education"],
    }
    for category, words in groups.items():
        if any(w in t for w in words):
            return category
    return "Other"


def experience_level(title: str) -> str:
    t = title.lower()
    if "entry-level" in t or "junior" in t:
        return "Entry Level"
    if "senior" in t or "chief" in t:
        return "Senior"
    if "manager" in t or "director" in t or "officer" in t:
        return "Mid/Senior"
    return "Mid Level"


def salary_value(i: int, category: str) -> int:
    base = {"Technology": 65000, "Healthcare": 60000, "Finance": 70000, "Creative & Media": 52000,
            "Legal": 62000, "Education": 48000, "Other": 50000}.get(category, 50000)
    return int(base + (i % 9) * 2500)


def work_mode(i: int) -> str:
    return ["On-site", "Hybrid", "Remote"][i % 3]


def engineer(path=INPUT):
    df = pd.read_csv(path, parse_dates=["posted_date"])
    df["job_category"] = df["job_title"].apply(classify_category)
    df["experience_level"] = df["job_title"].apply(experience_level)
    df["work_mode"] = [work_mode(i) for i in range(len(df))]
    df["salary_min"] = [salary_value(i, c) for i, c in enumerate(df["job_category"])]
    df["salary_max"] = df["salary_min"] + 15000
    df["salary_category"] = pd.cut(df["salary_min"], bins=[0, 50000, 70000, np.inf], labels=["Low", "Medium", "High"]).astype(str)
    df["title_word_count"] = df["job_title"].str.split().str.len()
    df["description_length"] = df["job_description"].str.len()
    df["description_word_count"] = df["job_description"].str.split().str.len()
    df["python_required"] = df["job_description"].str.contains(r"python", case=False, regex=True, na=False).astype(int)
    df["tech_keyword_count"] = df["job_description"].str.lower().apply(lambda x: len(re.findall(r"python|django|flask|java|html|css|sql|dashboard|software|web", x)))

    # Label encoding (required demonstration).
    label_encoder = LabelEncoder()
    df["job_category_label"] = label_encoder.fit_transform(df["job_category"])

    # One-hot encoding (required demonstration).
    encoded = pd.get_dummies(df[["experience_level", "work_mode"]], prefix=["experience", "work"], dtype=int)
    df = pd.concat([df, encoded], axis=1)
    df.to_csv(OUTPUT, index=False)
    return df


if __name__ == "__main__":
    processed = engineer()
    print(f"Saved {len(processed)} processed records -> {OUTPUT}")
    print(processed.head())
