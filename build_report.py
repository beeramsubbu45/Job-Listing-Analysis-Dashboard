from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / 'report' / 'project_report.pdf'
DF = pd.read_csv(ROOT/'data'/'processed_jobs.csv')
CHART = ROOT/'outputs'/'charts'

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='CoverTitle', parent=styles['Title'], alignment=TA_CENTER, fontSize=25, leading=30, spaceAfter=20))
styles.add(ParagraphStyle(name='Sub', parent=styles['Normal'], alignment=TA_CENTER, fontSize=13, leading=18))
styles.add(ParagraphStyle(name='H', parent=styles['Heading1'], fontSize=18, leading=22, spaceBefore=8, spaceAfter=10))
styles.add(ParagraphStyle(name='H2x', parent=styles['Heading2'], fontSize=13, leading=16, spaceBefore=6, spaceAfter=6))
styles.add(ParagraphStyle(name='Bodyx', parent=styles['BodyText'], fontSize=9.5, leading=14, spaceAfter=7))
styles.add(ParagraphStyle(name='Smallx', parent=styles['BodyText'], fontSize=8, leading=11))

def img(name, width=6.6*inch):
    p=CHART/name
    if p.exists():
        return Image(str(p), width=width, height=width*0.58)
    return Spacer(1, 0.1*inch)

story=[]
story += [Spacer(1,1.4*inch), Paragraph('JOB LISTINGS ANALYTICS DASHBOARD', styles['CoverTitle']), Paragraph('Using Python, Web Scraping, Data Analytics & Streamlit', styles['Sub']), Spacer(1,0.4*inch), Paragraph('Portfolio-Level Project Report', styles['Sub']), Spacer(1,0.8*inch), Paragraph('Prepared from the supplied project brief', styles['Sub']), PageBreak()]

story += [Paragraph('1. Project Overview', styles['H']), Paragraph('This project develops an end-to-end Job Listings Analytics Dashboard. The workflow follows the supplied brief: collect job data through web scraping, clean and preprocess it, engineer analytical features, perform statistical analysis and exploratory data analysis, visualize the findings, and publish the results through an interactive Streamlit dashboard.', styles['Bodyx']), Paragraph('The recommended source in the brief is the Real Python Fake Jobs practice site. The site is a static learning resource designed for web-scraping practice, so its listings are suitable for demonstrating the pipeline but should not be presented as real employment vacancies.', styles['Bodyx']), Paragraph('The implementation includes Python functions, a JobScraper class, exception handling, Requests, BeautifulSoup, NumPy, Pandas, Matplotlib, Seaborn, scikit-learn and Streamlit.', styles['Bodyx']), PageBreak()]

story += [Paragraph('2. Objectives', styles['H']), Paragraph('• Understand a complete data-analytics workflow.<br/>• Collect job information using Requests and BeautifulSoup.<br/>• Store extracted records in a Pandas DataFrame and CSV.<br/>• Handle missing values and duplicates.<br/>• Convert data types and standardize text.<br/>• Create new analytical features.<br/>• Demonstrate label encoding and one-hot encoding.<br/>• Perform univariate, bivariate and multivariate EDA.<br/>• Build an interactive Streamlit dashboard with filters, statistics, charts, business insights and download functionality.', styles['Bodyx']), Paragraph('The project brief also expects source code, raw/cleaned/processed datasets, a working dashboard, a project report, screenshots and a demonstration of scraping, cleaning, feature engineering, EDA, dashboard functionality and insights.', styles['Bodyx']), PageBreak()]

story += [Paragraph('3. Data Collection', styles['H']), Paragraph('The scraper requests the source page, locates the ResultsContainer, iterates through job cards, extracts title, company, location, posting date and application URL, and optionally visits the application/detail page to collect the job description. A custom ScrapingError and try/except handling make network failures explicit.', styles['Bodyx']), Paragraph('Source: https://realpython.github.io/fake-jobs/ . The source contains job cards with titles, companies, locations and application links; the individual job pages also expose descriptions. The supplied brief specifically recommends this website.', styles['Bodyx']), Paragraph(f'The bundled demonstration dataset contains {len(DF)} records, satisfying the brief requirement of at least 100 records.', styles['Bodyx']), PageBreak()]

story += [Paragraph('4. Dataset Information', styles['H']), Paragraph('Required core columns are job title, company name, location, job description/category and application link. Additional enriched columns include salary, experience level, job type/work mode and analytical features.', styles['Bodyx'])]
summary = [['Metric','Value'],['Records',str(len(DF))],['Columns',str(len(DF.columns))],['Companies',str(DF.company_name.nunique())],['Categories',str(DF.job_category.nunique())],['Average minimum salary',f"${DF.salary_min.mean():,.0f}"],['Most common category',DF.job_category.mode().iloc[0]],['Most common work mode',DF.work_mode.mode().iloc[0]]]
t=Table(summary,colWidths=[2.7*inch,2.7*inch]); t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.lightgrey),('GRID',(0,0),(-1,-1),0.4,colors.grey),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('PADDING',(0,0),(-1,-1),6)])); story += [t, Spacer(1,0.2*inch), PageBreak()]

story += [Paragraph('5. Data Cleaning & Preprocessing', styles['H']), Paragraph('The cleaning module standardizes column names, creates missing columns when necessary, trims text, fills missing text values, removes duplicate records, converts the posting date to a datetime type, and separates location into city and region. Missing job descriptions are replaced with an explicit placeholder so downstream analysis remains stable.', styles['Bodyx']), Paragraph('The pipeline saves cleaned_jobs.csv for the next phase. This directly addresses the brief requirements for missing-value handling, duplicate removal and data-type conversion.', styles['Bodyx']), PageBreak()]

story += [Paragraph('6. Feature Engineering', styles['H']), Paragraph('The feature-engineering module creates job category, experience level, work mode, salary minimum and maximum, salary category, title word count, description length, description word count, Python keyword flag and technical keyword count.', styles['Bodyx']), Paragraph('Label encoding is demonstrated through scikit-learn LabelEncoder for job category. One-hot encoding is demonstrated with Pandas get_dummies for experience level and work mode. The result is stored as processed_jobs.csv.', styles['Bodyx']), PageBreak()]

story += [Paragraph('7. Exploratory Data Analysis', styles['H']), Paragraph('The EDA stage includes the analysis types requested in the brief: histogram, count plot, bar plot, box plot, violin plot, scatter plot, crosstab/heatmap, pair plot and correlation analysis. Every visualization is intended to be accompanied by an observation in the final presentation or viva.', styles['Bodyx']), img('01_salary_histogram.png'), Paragraph('Figure 1. Salary distribution.', styles['Smallx']), PageBreak()]

story += [Paragraph('8. EDA Visualizations', styles['H']), img('02_category_countplot.png'), Paragraph('Figure 2. Job category distribution.', styles['Smallx']), img('03_avg_salary_category.png'), Paragraph('Figure 3. Average minimum salary by category.', styles['Smallx']), PageBreak()]

story += [Paragraph('9. Distribution & Relationship Analysis', styles['H']), img('04_salary_boxplot.png'), Paragraph('Figure 4. Salary spread by category.', styles['Smallx']), img('05_workmode_violin.png'), Paragraph('Figure 5. Salary distribution by work mode.', styles['Smallx']), PageBreak()]

story += [Paragraph('10. Multivariate Analysis', styles['H']), img('06_description_salary_scatter.png'), Paragraph('Figure 6. Description length versus minimum salary.', styles['Smallx']), img('07_category_workmode_heatmap.png'), Paragraph('Figure 7. Job category and work-mode crosstab.', styles['Smallx']), PageBreak()]

story += [Paragraph('11. Correlation & Pair Analysis', styles['H']), img('08_pairplot.png'), Paragraph('Figure 8. Pair plot of selected numerical features.', styles['Smallx']), img('09_correlation_heatmap.png'), Paragraph('Figure 9. Correlation heatmap.', styles['Smallx']), PageBreak()]

story += [Paragraph('12. Streamlit Dashboard', styles['H']), Paragraph('The dashboard is implemented in app.py and contains Home, Dataset Viewer, Summary Statistics, Filtering & Search, Interactive Charts, Business Insights and Download pages. Sidebar controls allow users to filter by category, work mode and experience level, search text, and minimum salary. The dashboard displays KPIs for total jobs, companies, categories and average minimum salary.', styles['Bodyx']), Paragraph('The dashboard also provides CSV download functionality so users can export the processed dataset. To run it, use: streamlit run app.py', styles['Bodyx']), PageBreak()]

story += [Paragraph('13. Business Insights', styles['H']), Paragraph('The dashboard calculates decision-oriented observations from the processed dataset: the largest job category, most common work mode, category with the highest average minimum salary and the share of descriptions containing the Python keyword. These metrics demonstrate how an analytical dashboard can convert raw records into understandable business observations.', styles['Bodyx']), Paragraph('Because the source is a synthetic learning site, these observations describe the demonstration dataset only and should not be interpreted as real labor-market statistics.', styles['Bodyx']), PageBreak()]

story += [Paragraph('14. Challenges & Solutions', styles['H']), Paragraph('Challenge: websites can change HTML structure. Solution: isolate scraping selectors in scraper.py and use exception handling.<br/><br/>Challenge: missing and duplicated records. Solution: explicit fill, type conversion and drop_duplicates steps.<br/><br/>Challenge: categorical variables cannot always be used directly in numerical analysis. Solution: label encoding and one-hot encoding.<br/><br/>Challenge: users need more than static charts. Solution: Streamlit filters, KPIs, interactive charts and download controls.<br/><br/>Challenge: the bundled project must run even before a fresh scrape. Solution: provide ready-made raw, cleaned and processed CSVs while keeping scraper.py available for refresh.', styles['Bodyx']), PageBreak()]

story += [Paragraph('15. Conclusion', styles['H']), Paragraph('The completed project demonstrates an end-to-end Python analytics workflow from web scraping to an interactive dashboard. It covers the required programming, data collection, cleaning, feature engineering, statistical analysis, visualization and dashboard stages described in the supplied brief. The project can be extended with multiple sources, pagination handling, advanced search, additional dashboard filters and report export.', styles['Bodyx']), Paragraph('Recommended viva explanation: “I collected job listings with Requests and BeautifulSoup, cleaned and standardized them with Pandas, engineered analytical features including salary and job category, performed EDA using Matplotlib and Seaborn, and deployed the results through Streamlit with filters, KPIs, charts, insights and CSV download.”', styles['Bodyx'])]

doc=SimpleDocTemplate(str(PDF),pagesize=A4,rightMargin=45,leftMargin=45,topMargin=45,bottomMargin=45)
doc.build(story)
print(PDF)
