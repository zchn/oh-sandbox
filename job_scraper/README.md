# Job Scraper

A Python package for scraping job postings from LinkedIn using their official API.

## Installation

```bash
pip install .
```

## Usage

First, you need to set up your LinkedIn API credentials. You can either:

1. Set the `LINKEDIN_ACCESS_TOKEN` environment variable
2. Create a `.env` file with your LinkedIn API token:
   ```
   LINKEDIN_ACCESS_TOKEN=your_token_here
   ```
3. Pass the token directly to the scraper

Example usage:

```python
from job_scraper import LinkedInJobScraper

# Create a scraper instance
scraper = LinkedInJobScraper()

# Search for jobs
jobs_df = scraper.search_jobs(
    keywords="python developer",
    location="San Francisco",
    limit=10
)

# Display results
print(jobs_df)
```

The results will be returned as a pandas DataFrame with the following columns:
- title: Job title
- salary_range: Formatted salary range
- required_skills: List of required skills

## Testing

Run the tests using:

```bash
python -m unittest discover tests
```
