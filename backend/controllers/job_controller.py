from flask import Blueprint, Response
from services.job_service import JobService
from services.keyword_service import KeywordService
from services.filter_service import FilterService
from utils.text_utils import clean_text
import requests
import json

job_controller = Blueprint("job_controller", __name__)
job_service = JobService()
keyword_service = KeywordService()
filter_service = FilterService()


@job_controller.route("/api/jobs")
def get_jobs():
    def generate_jobs():
        all_data = []
        filtered_out_jobs = []
        page_index = 1
        total_pages = 0
        total_items = 0
        filtered_out_items = 0

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
            page_filtered_out_jobs = []

            for job in job_list:
                job_name = clean_text(job.get("jobName", ""))
                if not job_name:
                    print("警告：jobName 為空，跳過此條目")
                    continue

                if filter_service.filter_by_job_name(job_name):
                    filtered_out_items += 1
                    page_filtered_out_jobs.append({
                        "Job Name": job_name,
                        "Description": clean_text(job.get("description", "")),
                        "Job Address": clean_text(job.get("jobAddrNoDesc", "")),
                        "Job Link": clean_text(job.get("link", {}).get("job", ""))
                    })
                    continue

                job_info = {
                    "Appear Date": clean_text(job.get("appearDate", "")),
                    "Company Name": clean_text(job.get("custName", "")),
                    "Job Name": job_name,
                    "Description": clean_text(job.get("description", "")),
                    "Job Address": clean_text(job.get("jobAddrNoDesc", "")),
                    "Job Link": clean_text(job.get("link", {}).get("job", "")),
                    "Labels": keyword_service.extract_labels(job.get("description", ""))
                }
                page_jobs.append(job_info)

            all_data.extend(page_jobs)
            filtered_out_jobs.extend(page_filtered_out_jobs)

            yield f"data: {json.dumps({'jobs': page_jobs})}\n\n"
            yield f"data: {json.dumps({'filtered_out_jobs': page_filtered_out_jobs})}\n\n"

            page_jobs.clear()
            page_filtered_out_jobs.clear()

            if page_index >= total_pages:
                break

            page_index += 1

        total_items -= filtered_out_items
        metadata['total'] = total_items
        metadata['filtered_out'] = filtered_out_items

        yield f"data: {json.dumps({'metadata': metadata})}\n\n"
        print(f"已過濾的工作數量: {len(filtered_out_jobs)}")

    return Response(generate_jobs(), content_type='text/event-stream')