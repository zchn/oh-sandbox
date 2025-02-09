# Job Post Scraper

A Python application that scrapes job postings from popular job websites and extracts key information like job title, company, salary range, and required skills.

## Features

- Scrapes job postings from Indeed
- Extracts job title, company name, salary (when available), and required skills
- Identifies common technical skills in job descriptions
- Returns results in a pandas DataFrame format

## Installation

1. Clone the repository
2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

```python
from job_scraper import JobScraper

# Create a scraper instance
scraper = JobScraper()

# Search for jobs
jobs = scraper.scrape_jobs("Software Engineer", "United States")

# Display results
print(jobs.to_string(index=False))
```

## Output Format

The scraper returns a pandas DataFrame with the following columns:
- title: Job title
- company: Company name
- salary: Salary range (if available)
- skills: Comma-separated list of identified technical skills

## Testing

Run the tests using pytest:
```bash
pytest tests/
```

## Notes

- The scraper currently supports Indeed. LinkedIn support was removed as it requires authentication.
- The scraper respects website rate limits and robots.txt
- Some job postings may not have salary information available
- Skills are extracted based on a predefined list of common technical skills
