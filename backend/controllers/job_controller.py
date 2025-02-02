from flask import Blueprint, Response
from services.job_service import JobService
from utils.text_utils import clean_text
from utils.job_utils import generate_job_info
import requests
import json

job_controller = Blueprint("job_controller", __name__)
job_service = JobService()


@job_controller.route("/api/jobs")
def get_jobs():
    def generate_jobs():
        all_data = []
        page_index = 1
        total_pages = 0
        total_items = 0

        response = requests.get(f"{job_service.url}&page={
                                page_index}", headers=job_service.headers)
        data = response.json()
        job_list = data.get("data", [])
        pagination = data.get("metadata", {}).get("pagination", {})

        if pagination:
            total_pages = pagination.get("lastPage", 0)
            total_items = pagination.get("total", 0)

        print(f"正在發送請求，total_pages: {total_pages}, total_items: {total_items}")

        metadata = {
            "lastPage": total_pages,
            "total": total_items
        }
        yield f"data: {json.dumps({'metadata': metadata})}\n\n"

        while True:
            page_url = f"{job_service.url}&page={page_index}"
            response = requests.get(page_url, headers=job_service.headers)
            data = response.json()
            job_list = data.get("data", [])

            if not job_list:
                print("沒有更多資料，抓取結束。")
                break

            yield f"data: {json.dumps({'page_count': page_index, 'total_pages': total_pages})}\n\n"

            page_jobs = []

            for job in job_list:
                job_info = generate_job_info(job)

                job_name = clean_text(job.get("jobName", ""))
                if not job_name:
                    print("警告：jobName 為空，跳過此條目")
                    continue

                page_jobs.append(job_info)

            all_data.extend(page_jobs)

            yield f"data: {json.dumps({'job_results': page_jobs})}\n\n"

            page_jobs.clear()

            if page_index >= total_pages:
                break

            page_index += 1

        metadata['total'] = total_items

        yield f"data: {json.dumps({'metadata': metadata})}\n\n"

    return Response(generate_jobs(), content_type='text/event-stream')
