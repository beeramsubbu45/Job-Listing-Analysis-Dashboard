"""Web scraper for the Real Python Fake Jobs practice site."""
from pathlib import Path
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup

URL = "https://realpython.github.io/fake-jobs/"
ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; JobAnalyticsStudentProject/1.0)"}


class ScrapingError(Exception):
    """Raised when the job source cannot be scraped."""


class JobScraper:
    """Object-oriented wrapper around requests + BeautifulSoup."""

    def __init__(self, url: str = URL):
        self.url = url

    def fetch(self, url: str) -> BeautifulSoup:
        try:
            response = requests.get(url, headers=HEADERS, timeout=20)
            response.raise_for_status()
        except requests.RequestException as exc:
            raise ScrapingError(f"Unable to fetch {url}: {exc}") from exc
        return BeautifulSoup(response.text, "html.parser")

    def scrape_jobs(self, fetch_details: bool = True) -> pd.DataFrame:
        soup = self.fetch(self.url)
        results = soup.find(id="ResultsContainer")
        if results is None:
            raise RuntimeError("Could not find ResultsContainer on the source page.")

        rows = []
        cards = results.find_all("div", class_="card-content")
        for card in cards:
            title_el = card.find("h2", class_="title")
            company_el = card.find("h3", class_="company")
            location_el = card.find("p", class_="location")
            date_el = card.find("time")
            links = card.find_all("a")
            apply_link = links[1].get("href") if len(links) > 1 else ""

            description = ""
            if fetch_details and apply_link:
                try:
                    detail = self.fetch(apply_link)
                    body = detail.find("div", class_="content")
                    if body:
                        description = body.get_text(" ", strip=True)
                    time.sleep(0.05)
                except requests.RequestException:
                    description = ""

            rows.append({
                "job_title": title_el.get_text(strip=True) if title_el else "",
                "company_name": company_el.get_text(strip=True) if company_el else "",
                "location": location_el.get_text(" ", strip=True) if location_el else "",
                "job_description": description,
                "posted_date": date_el.get_text(strip=True) if date_el else "",
                "apply_link": apply_link,
            })

        return pd.DataFrame(rows)


def scrape_jobs(url: str = URL, fetch_details: bool = True) -> pd.DataFrame:
    return JobScraper(url).scrape_jobs(fetch_details=fetch_details)


if __name__ == "__main__":
    df = scrape_jobs()
    out = DATA_DIR / "raw_jobs.csv"
    df.to_csv(out, index=False)
    print(f"Scraped {len(df)} jobs -> {out}")
