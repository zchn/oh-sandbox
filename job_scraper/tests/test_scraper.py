import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from job_scraper import LinkedInJobScraper

class TestLinkedInJobScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = LinkedInJobScraper("dummy_token")

    def test_init_without_token(self):
        with patch('os.getenv', return_value=None):
            with self.assertRaises(ValueError):
                LinkedInJobScraper()

    @patch('requests.get')
    def test_search_jobs_success(self, mock_get):
        # Mock the job search response
        mock_search_response = MagicMock()
        mock_search_response.json.return_value = {
            "elements": [
                {"entityUrn": "job1"},
                {"entityUrn": "job2"}
            ]
        }

        # Mock the job details responses
        mock_details_response = MagicMock()
        mock_details_response.json.return_value = {
            "title": "Software Engineer",
            "salaryRange": {
                "min": 100000,
                "max": 150000,
                "currency": "USD"
            },
            "skills": ["Python", "JavaScript"]
        }

        mock_get.side_effect = [
            mock_search_response,
            mock_details_response,
            mock_details_response
        ]

        df = self.scraper.search_jobs("python developer")

        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 2)
        self.assertEqual(list(df.columns), ["title", "salary_range", "required_skills"])

    @patch('requests.get')
    def test_search_jobs_api_error(self, mock_get):
        mock_get.side_effect = Exception("API Error")

        df = self.scraper.search_jobs("python developer")

        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(df.empty)
        self.assertEqual(list(df.columns), ["title", "salary_range", "required_skills"])

    def test_format_salary_range(self):
        test_cases = [
            (
                {"min": 100000, "max": 150000, "currency": "USD"},
                "USD 100,000 - 150,000"
            ),
            (
                {"min": 100000, "currency": "USD"},
                "USD 100,000+"
            ),
            (
                {"max": 150000, "currency": "USD"},
                "Up to USD 150,000"
            ),
            (
                {},
                "Not specified"
            )
        ]

        for salary_data, expected in test_cases:
            result = self.scraper._format_salary_range(salary_data)
            self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
