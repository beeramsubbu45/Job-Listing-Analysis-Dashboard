"""Generate statistical summaries and EDA visualizations with Matplotlib and Seaborn."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed_jobs.csv"
OUT = ROOT / "outputs" / "charts"
OUT.mkdir(parents=True, exist_ok=True)


def save(fig, name):
    fig.tight_layout()
    fig.savefig(OUT / name, dpi=160, bbox_inches="tight")
    plt.close(fig)


def run_eda():
    sns.set_theme()  # Seaborn styling; charts also use Matplotlib Figure/Axes APIs.
    df = pd.read_csv(DATA)

    # 1. Histogram
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(df["salary_min"], bins=12)
    ax.set_title("Salary Distribution")
    ax.set_xlabel("Minimum Salary")
    save(fig, "01_salary_histogram.png")

    # 2. Count plot — use Seaborn when available; fall back to Matplotlib for older environments.
    fig, ax = plt.subplots(figsize=(8, 5))
    order = df["job_category"].value_counts().index
    try:
        sns.countplot(data=df, y="job_category", order=order, ax=ax)
    except Exception:
        counts = df["job_category"].value_counts().reindex(order)
        ax.barh(counts.index, counts.values)
    ax.set_title("Jobs by Category")
    save(fig, "02_category_countplot.png")

    # 3. Average salary bar chart
    category_salary = df.groupby("job_category", as_index=False)["salary_min"].mean().sort_values("salary_min", ascending=False)
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.barh(category_salary["job_category"], category_salary["salary_min"])
    ax.invert_yaxis()
    ax.set_title("Average Minimum Salary by Category")
    save(fig, "03_avg_salary_category.png")

    # 4. Box plot
    fig, ax = plt.subplots(figsize=(9, 5))
    groups = [g["salary_min"].values for _, g in df.groupby("job_category")]
    labels = list(df.groupby("job_category").groups.keys())
    ax.boxplot(groups, labels=labels)
    ax.set_title("Salary Spread by Category")
    ax.tick_params(axis="x", rotation=35)
    save(fig, "04_salary_boxplot.png")

    # 5. Violin plot
    fig, ax = plt.subplots(figsize=(9, 5))
    groups = [g["salary_min"].values for _, g in df.groupby("work_mode")]
    labels = list(df.groupby("work_mode").groups.keys())
    ax.violinplot(groups, showmeans=True)
    ax.set_xticks(range(1, len(labels) + 1), labels)
    ax.set_title("Salary by Work Mode")
    save(fig, "05_workmode_violin.png")

    # 6. Scatter plot
    fig, ax = plt.subplots(figsize=(8, 5))
    for category, group in df.groupby("job_category"):
        ax.scatter(group["description_word_count"], group["salary_min"], label=category, alpha=0.7)
    ax.set_xlabel("Description Word Count")
    ax.set_ylabel("Minimum Salary")
    ax.set_title("Description Length vs Minimum Salary")
    ax.legend(fontsize=7)
    save(fig, "06_description_salary_scatter.png")

    # 7. Crosstab heatmap (Matplotlib imshow to keep the pipeline portable)
    cross = pd.crosstab(df["job_category"], df["work_mode"])
    fig, ax = plt.subplots(figsize=(8, 5))
    image = ax.imshow(cross.values, aspect="auto")
    ax.set_xticks(range(len(cross.columns)), cross.columns)
    ax.set_yticks(range(len(cross.index)), cross.index)
    for i in range(cross.shape[0]):
        for j in range(cross.shape[1]):
            ax.text(j, i, cross.iloc[i, j], ha="center", va="center")
    ax.set_title("Job Category × Work Mode")
    fig.colorbar(image, ax=ax)
    save(fig, "07_category_workmode_heatmap.png")

    # 8. Pair plot — Seaborn implementation with a Matplotlib fallback.
    pair = df[["salary_min", "title_word_count", "description_word_count", "tech_keyword_count"]]
    try:
        g = sns.pairplot(pair)
        g.fig.suptitle("Multivariate Pair Plot", y=1.02)
        g.savefig(OUT / "08_pairplot.png", dpi=150, bbox_inches="tight")
        plt.close(g.fig)
    except Exception:
        pd.plotting.scatter_matrix(pair, figsize=(9, 9))
        plt.suptitle("Multivariate Pair Plot")
        plt.savefig(OUT / "08_pairplot.png", dpi=150, bbox_inches="tight")
        plt.close("all")

    # 9. Correlation heatmap
    numeric = df.select_dtypes(include="number")
    corr = numeric.corr()
    fig, ax = plt.subplots(figsize=(10, 7))
    image = ax.imshow(corr.values, aspect="auto", vmin=-1, vmax=1)
    ax.set_xticks(range(len(corr.columns)), corr.columns, rotation=80)
    ax.set_yticks(range(len(corr.index)), corr.index)
    ax.set_title("Numeric Feature Correlation")
    fig.colorbar(image, ax=ax)
    save(fig, "09_correlation_heatmap.png")

    df.describe(include="all").transpose().to_csv(ROOT / "outputs" / "statistical_summary.csv")
    print(f"EDA outputs saved to {OUT}")


if __name__ == "__main__":
    run_eda()
