# Job Listings Analytics Dashboard

Complete portfolio project based on the supplied project brief: **Job Listings Analytics Dashboard using Python, Web Scraping & Streamlit**.

## Project goals
- Collect job listings with `requests` and `BeautifulSoup`.
- Clean and preprocess the data with Pandas.
- Handle missing values and duplicate records.
- Create features such as salary category, experience level, job category, work mode, title length and description length.
- Demonstrate label encoding and one-hot encoding.
- Perform statistical analysis and EDA.
- Build visualizations with Matplotlib and Seaborn.
- Build an interactive Streamlit dashboard with filters, KPIs, charts, business insights and CSV download.

## Data source
The supplied brief recommends the Real Python Fake Jobs site: https://realpython.github.io/fake-jobs/ . It is a static practice site designed for web-scraping exercises. The included `src/scraper.py` collects job title, company, location, description, date and application URL from that site.

The bundled CSVs contain a ready-to-run demonstration dataset with 100+ records so the dashboard works immediately. Run the scraper when you have internet access to refresh the raw dataset.

## Folder structure
```
Job_Listings_Analytics_Project/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   ├── raw_jobs.csv
│   ├── cleaned_jobs.csv
│   └── processed_jobs.csv
├── src/
│   ├── scraper.py
│   ├── data_cleaning.py
│   ├── feature_engineering.py
│   └── eda.py
├── outputs/
│   └── charts/*.png
├── report/
│   └── project_report.pdf
└── assets/
    └── README.txt
```

## Installation
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
pip install -r requirements.txt
```

## Run the complete pipeline
```bash
python src/scraper.py
python src/data_cleaning.py
python src/feature_engineering.py
python src/eda.py
streamlit run app.py
```

If you only want to use the included ready-made dataset, skip the scraper and run:
```bash
python src/data_cleaning.py
python src/feature_engineering.py
python src/eda.py
streamlit run app.py
```

## Dashboard pages
1. Home
2. Dataset Viewer
3. Summary Statistics
4. Filtering & Search
5. Interactive Charts
6. Business Insights
7. Download Processed Dataset

## Important note
The source website is a **fake/static job board for learning**, not a live employment database. Do not represent its records as real vacancies. The project uses it because the supplied brief specifically recommends it.
