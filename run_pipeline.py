"""Run the non-interactive data pipeline in sequence."""
from src.scraper import scrape_jobs, URL
from src.data_cleaning import clean_data
from src.feature_engineering import engineer
from src.eda import run_eda

if __name__ == '__main__':
    print('1/4 Scraping...')
    try:
        df = scrape_jobs(URL, fetch_details=True)
        df.to_csv('data/raw_jobs.csv', index=False)
        print(f'   Scraped {len(df)} records.')
    except Exception as exc:
        print(f'   Scraping skipped/failed: {exc}')
        print('   Keeping the bundled demonstration raw dataset.')
    print('2/4 Cleaning...')
    clean_data()
    print('3/4 Feature engineering...')
    engineer()
    print('4/4 EDA...')
    run_eda()
    print('Pipeline complete. Start dashboard with: streamlit run app.py')
