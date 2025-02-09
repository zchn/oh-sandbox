import os
import requests
import pandas as pd
from typing import List, Dict, Optional
from dotenv import load_dotenv

class LinkedInJobScraper:
    def __init__(self, access_token: Optional[str] = None):
        load_dotenv()
        self.access_token = access_token or os.getenv('LINKEDIN_ACCESS_TOKEN')
        if not self.access_token:
            raise ValueError("LinkedIn access token is required")

        self.base_url = "https://api.linkedin.com/v2"
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

    def search_jobs(self, keywords: str, location: str = None, limit: int = 10) -> pd.DataFrame:
        """
        Search for jobs on LinkedIn using their Jobs Search API

        Args:
            keywords: Search keywords
            location: Location to search in
            limit: Maximum number of results to return

        Returns:
            DataFrame containing job listings with title, salary range, and required skills
        """
        endpoint = f"{self.base_url}/jobSearch"
        params = {
            "keywords": keywords,
            "location": location,
            "count": min(limit, 50)  # LinkedIn API limit
        }

        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            jobs_data = response.json()

            jobs_list = []
            for job in jobs_data.get("elements", []):
                job_details = self._get_job_details(job["entityUrn"])
                if job_details:
                    jobs_list.append(job_details)

            if not jobs_list:
                return pd.DataFrame(columns=["title", "salary_range", "required_skills"])

            return pd.DataFrame(jobs_list)

        except Exception as e:
            print(f"Error fetching jobs: {e}")
            return pd.DataFrame(columns=["title", "salary_range", "required_skills"])

    def _get_job_details(self, job_id: str) -> Optional[Dict]:
        """
        Get detailed information about a specific job posting

        Args:
            job_id: LinkedIn job ID

        Returns:
            Dictionary containing job details or None if request fails
        """
        endpoint = f"{self.base_url}/jobs/{job_id}"

        try:
            response = requests.get(endpoint, headers=self.headers)
            response.raise_for_status()
            job_data = response.json()

            return {
                "title": job_data.get("title", ""),
                "salary_range": self._format_salary_range(job_data.get("salaryRange", {})),
                "required_skills": job_data.get("skills", [])
            }

        except requests.exceptions.RequestException:
            return None

    @staticmethod
    def _format_salary_range(salary_data: Dict) -> str:
        """Format salary range into a readable string"""
        if not salary_data:
            return "Not specified"

        min_salary = salary_data.get("min", "")
        max_salary = salary_data.get("max", "")
        currency = salary_data.get("currency", "USD")

        if min_salary and max_salary:
            return f"{currency} {min_salary:,} - {max_salary:,}"
        elif min_salary:
            return f"{currency} {min_salary:,}+"
        elif max_salary:
            return f"Up to {currency} {max_salary:,}"
        return "Not specified"
