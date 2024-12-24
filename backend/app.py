from flask import Flask, Response
from flask_cors import CORS
import requests
import json
import re

app = Flask(__name__)

CORS(app)

with open('./data/keywords.json', 'r', encoding='utf-8') as f:
    keywords = json.load(f)

with open('./data/filter_keywords.json', 'r', encoding='utf-8') as f:
    filter_keywords = json.load(f)

job_name_filter_keywords = filter_keywords.get("job_name", [])

url = "https://www.104.com.tw/jobs/search/api/jobs?area=6001001000%2C6001002000&jobcat=2007001015%2C2007001017&jobsource=joblist_search&mode=s&order=15&pagesize=100&scmin=40000&scneg=1&scstrict=1&sctp=M&searchJobs=1"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Referer": "https://www.104.com.tw/"
}


def clean_text(text):
    if isinstance(text, str):
        text = re.sub(r'[\s\n\r]+', ' ', text)
        return re.sub(r'[^\x20-\x7E\u4e00-\u9fa5]', '', text)
    return text


def extract_labels(description):
    labels = set()
    description = clean_text(description)

    for keyword, label in keywords.items():
        if re.search(r'\b' + re.escape(keyword) + r'\b', description, re.IGNORECASE):
            labels.add(label)

    return list(labels)


def filter_by_job_name(job_name):
    """ 根據關鍵字過濾工作名稱 """
    job_name = clean_text(job_name)
    for keyword in job_name_filter_keywords:
        if re.search(re.escape(keyword), job_name, re.IGNORECASE):
            print(f"匹配到關鍵字: {keyword}，過濾: {job_name}")
            return True
    return False


@app.route("/api/jobs")
def get_jobs():
    def generate_jobs():
        all_data = []
        filtered_out_jobs = []
        page_index = 1
        total_pages = 0
        total_items = 0
        filtered_out_items = 0

        response = requests.get(f"{url}&page={page_index}", headers=headers)
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
            page_url = f"{url}&page={page_index}"
            response = requests.get(page_url, headers=headers)
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

                if filter_by_job_name(job_name):
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
                    "Labels": extract_labels(job.get("description", ""))
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


if __name__ == "__main__":
    app.run(debug=True)
