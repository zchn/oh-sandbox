import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from urllib.parse import quote

class JobScraper:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def extract_skills(self, text):
        common_skills = ["python", "java", "javascript", "sql", "aws", "docker",
                        "kubernetes", "react", "node.js", "agile", "scrum"]
        skills = []
        for skill in common_skills:
            if skill.lower() in text.lower():
                skills.append(skill)
        return ", ".join(skills) if skills else "Not specified"

    def scrape_indeed(self, job_title, location="United States"):
        jobs = []
        encoded_title = quote(job_title)
        encoded_location = quote(location)
        url = f"https://www.indeed.com/jobs?q={encoded_title}&l={encoded_location}"

        try:
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')

            job_cards = soup.find_all('div', {'class': ['job_seen_beacon', 'resultContent']})

            for card in job_cards[:10]:
                try:
                    # Find title - handle different class names
                    title_elem = card.find(['h2', 'a'], {'class': ['jobTitle', 'jcs-JobTitle']})
                    if not title_elem:
                        continue
                    title = title_elem.get_text(strip=True)

                    # Find company
                    company_elem = card.find(['span', 'div'], {'class': ['companyName', 'company']})
                    company = company_elem.get_text(strip=True) if company_elem else "Not specified"

                    # Find salary
                    salary_elem = card.find(['div', 'span'], {'class': ['salary-snippet-container', 'salaryText']})
                    salary = salary_elem.get_text(strip=True) if salary_elem else "Not specified"

                    # Get job description/snippet
                    description_elem = card.find(['div', 'span'], {'class': ['job-snippet', 'summary']})
                    description = description_elem.get_text(strip=True) if description_elem else ""

                    # Extract skills from description
                    skills = self.extract_skills(description)

                    jobs.append({
                        "title": title,
                        "company": company,
                        "salary": salary,
                        "skills": skills
                    })

                except Exception as e:
                    print(f"Error processing job card: {str(e)}")
                    continue

        except Exception as e:
            print(f"Error scraping Indeed: {str(e)}")

        return pd.DataFrame(jobs)

    def scrape_jobs(self, job_title, location="United States"):
        # For now, we'll just use Indeed as LinkedIn requires authentication
        jobs = self.scrape_indeed(job_title, location)
        return jobs

if __name__ == "__main__":
    scraper = JobScraper()
    jobs = scraper.scrape_jobs("Software Engineer")
    print("\nJob Postings:")
    print(jobs.to_string(index=False))

if __name__ == "__main__":
    scraper = JobScraper()
    jobs = scraper.scrape_jobs("Software Engineer")
    print("\nJob Postings:")
    print(jobs.to_string(index=False))
