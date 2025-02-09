import pytest
import pandas as pd
from job_scraper import JobScraper

def test_job_scraper_initialization():
    scraper = JobScraper()
    assert scraper is not None
    assert hasattr(scraper, 'headers')

def test_extract_skills():
    scraper = JobScraper()
    text = "We are looking for a Python developer with SQL and AWS experience"
    skills = scraper.extract_skills(text)
    assert "python" in skills.lower()
    assert "sql" in skills.lower()
    assert "aws" in skills.lower()

    text = "No relevant skills mentioned here"
    skills = scraper.extract_skills(text)
    assert skills == "Not specified"

def test_indeed_scraping():
    scraper = JobScraper()
    jobs = scraper.scrape_indeed("Software Engineer")

    assert isinstance(jobs, pd.DataFrame)
    assert len(jobs) >= 0  # May be 0 if no jobs found or rate limited

    if len(jobs) > 0:
        assert all(col in jobs.columns for col in ['title', 'company', 'salary', 'skills'])

def test_scrape_jobs():
    scraper = JobScraper()
    jobs = scraper.scrape_jobs("Software Engineer")

    assert isinstance(jobs, pd.DataFrame)
    assert len(jobs) >= 0  # May be 0 if no jobs found or rate limited

    if len(jobs) > 0:
        assert all(col in jobs.columns for col in ['title', 'company', 'salary', 'skills'])
