import requests
from utils.job_utils import generate_job_info

job_api_url = "https://www.104.com.tw/jobs/search/api/jobs?area=6001001000%2C6001002000&excludeJobKeyword=%E4%B8%BB%E4%BB%BB%2C%E9%AB%98%E7%B4%9A%2CLead%2CManager%2CSenior%2C%E8%B3%87%E6%B7%B1%2C%E4%B8%BB%E7%AE%A1&jobcat=2007001015%2C2007001017&jobsource=joblist_search&mode=s&page=2&pagesize=100&scmin=40000&scneg=1&scstrict=1&sctp=M&searchJobs=1"


class JobService:

    def __init__(self):
        self.url = job_api_url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Referer": "https://www.104.com.tw/"
        }

    def get_jobs(self):
        page_index = 1
        all_data = []

        response = requests.get(
            f"{self.url}&page={page_index}", headers=self.headers)
        data = response.json()

        job_list = data.get("data", [])
        pagination = data.get("metadata", {}).get("pagination", {})

        total_pages = pagination.get("lastPage", 0)
        total_items = pagination.get("total", 0)

        while page_index <= total_pages:
            response = requests.get(
                f"{self.url}&page={page_index}", headers=self.headers)
            data = response.json()

            job_list = data.get("data", [])
            if not job_list:
                break

            page_jobs = []

            for job in job_list:
                job_info = generate_job_info(job)
                if not job_info:
                    continue

                page_jobs.append(job_info)

            all_data.extend(page_jobs)

            page_index += 1

        return all_data, total_items, total_pages

    def get_metadata(self, data):
        pagination = data.get("metadata", {}).get("pagination", {})
        return {
            "total": pagination.get("total", 0),
            "totalPages": pagination.get("lastPage", 0),
        }
