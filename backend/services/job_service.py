import requests
from utils.text_utils import clean_text
from services.filter_service import FilterService
from utils.job_utils import generate_job_info

filter_service = FilterService()


class JobService:
    def __init__(self):
        self.url = "https://www.104.com.tw/jobs/search/api/jobs?area=6001001000%2C6001002000&jobcat=2007001015%2C2007001017&jobsource=joblist_search&mode=s&order=15&pagesize=100&scmin=40000&scneg=1&scstrict=1&sctp=M&searchJobs=1"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Referer": "https://www.104.com.tw/"
        }

    def get_jobs(self):
        page_index = 1
        all_data = []
        filtered_out_jobs = []
        filtered_out_items = 0

        response = requests.get(
            f"{self.url}&page={page_index}", headers=self.headers)
        data = response.json()

        job_list = data.get("data", [])
        pagination = data.get("metadata", {}).get("pagination", {})

        total_pages = pagination.get("lastPage", 0)
        total_items = pagination.get("total", 0)

        if not job_list:
            return all_data, filtered_out_jobs, total_items, total_pages

        while page_index <= total_pages:
            response = requests.get(
                f"{self.url}&page={page_index}", headers=self.headers)
            data = response.json()

            job_list = data.get("data", [])
            if not job_list:
                break

            page_jobs = []
            page_filtered_out_jobs = []

            for job in job_list:
                job_info = generate_job_info(job)
                if not job_info:
                    continue

                if filter_service.filter_by_job_name(job_info["Job Name"]):
                    page_filtered_out_jobs.append(job_info)
                    filtered_out_items += 1
                    continue

                page_jobs.append(job_info)

            all_data.extend(page_jobs)
            filtered_out_jobs.extend(page_filtered_out_jobs)

            page_index += 1

        total_items -= filtered_out_items
        return all_data, filtered_out_jobs, total_items, total_pages

    def get_metadata(self, data, filtered_out_items):
        pagination = data.get("metadata", {}).get("pagination", {})
        return {
            "total": pagination.get("total", 0),
            "totalPages": pagination.get("lastPage", 0),
            "filtered_out": filtered_out_items
        }
