from flask import Flask, Response
from flask_cors import CORS
import requests
import json
import re

app = Flask(__name__)

CORS(app)

url = "https://www.104.com.tw/jobs/search/api/jobs?area=6001001000%2C6001002000&jobcat=2007001015%2C2007001017&jobsource=joblist_search&mode=s&order=15&pagesize=100&scmin=40000&scneg=1&scstrict=1&sctp=M&searchJobs=1"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Referer": "https://www.104.com.tw/"
}

keywords = {
    "JavaScript": "javascript",
    "React": "react",
    "Vue": "vue",
    "Python": "python",
    "Node.js": "nodejs",
    "TypeScript": "typescript",
    "Tailwindcss": "tailwindcss",
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


@app.route("/api/jobs", methods=["GET"])
def get_jobs():
    def generate_jobs():
        all_data = []
        page_index = 1
        total_pages = 0
        total_items = 0

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

            for job in job_list:
                job_info = {
                    "Appear Date": clean_text(job.get("appearDate", "")),
                    "Company Name": clean_text(job.get("custName", "")),
                    "Job Name": clean_text(job.get("jobName", "")),
                    "Description": clean_text(job.get("description", "")),
                    "Job Address": clean_text(job.get("jobAddrNoDesc", "")),
                    "Job Link": clean_text(job.get("link", {}).get("job", "")),
                    "Labels": extract_labels(job.get("description", ""))

                }
                all_data.append(job_info)

            if page_index >= total_pages:
                break

            page_index += 1

        yield f"data: {json.dumps({'jobs': all_data})}\n\n"

    return Response(generate_jobs(), content_type='text/event-stream')


if __name__ == "__main__":
    app.run(debug=True)
