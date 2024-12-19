from flask import Flask, Response
from flask_cors import CORS
import requests
import json
import re

app = Flask(__name__)

# 啟用 CORS 支援
CORS(app)

url = "https://www.104.com.tw/jobs/search/api/jobs?area=6001001000%2C6001002000&jobcat=2007001015%2C2007001017&jobsource=joblist_search&mode=s&order=15&pagesize=20&scmin=40000&scneg=1&scstrict=1&sctp=M&searchJobs=1"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Referer": "https://www.104.com.tw/"
}


def clean_text(text):
    if isinstance(text, str):
        return re.sub(r'[^\x20-\x7E\u4e00-\u9fa5]', '', text)
    return text


@app.route("/api/jobs", methods=["GET"])
def get_jobs():
    def generate_jobs():
        # 存儲所有資料的列表
        all_data = []
        page_index = 1
        total_pages = 0  # 記錄已抓取的頁數

        while True:
            print(f"正在發送請求，PageIndex: {page_index}")

            # 動態生成每一頁的 URL
            page_url = f"{url}&page={page_index}"

            # 發送 GET 請求
            response = requests.get(page_url, headers=headers)

            # 假設返回的 JSON 資料中有職位列表
            data = response.json()  # 假設返回的是 JSON 格式資料
            job_list = data.get("data", [])  # 假設 JSON 裡的資料在 "data" 欄位

            # 如果沒有資料，則停止抓取
            if not job_list:
                print("沒有更多資料，抓取結束。")
                break

            # 增加已抓取的頁數
            total_pages += 1

            # 發送頁數資料給前端
            yield f"data: {json.dumps({'page_count': total_pages})}\n\n"

            # 遍歷每一個職位，將其資訊加入 all_data
            for job in job_list:
                job_info = {
                    "Appear Date": clean_text(job.get("appearDate", "")),
                    "Company Name": clean_text(job.get("custName", "")),
                    "Job Name": clean_text(job.get("jobName", "")),
                    "Description": clean_text(job.get("description", "")),
                    "Job Address": clean_text(job.get("jobAddrNoDesc", "")),
                    "Job Link": clean_text(job.get("link", {}).get("job", "")),
                }
                all_data.append(job_info)

            # 如果工作列表數量小於20，說明已經是最後一頁
            if len(job_list) < 20:
                print("已經抓取到最後一頁。")
                break

            page_index += 1  # 增加頁數繼續抓取下一頁

        # 返回抓取到的所有資料
        yield f"data: {json.dumps({'jobs': all_data})}\n\n"

    # 使用 Flask 的 Response 回傳 SSE 流式數據
    return Response(generate_jobs(), content_type='text/event-stream')


if __name__ == "__main__":
    app.run(debug=True)
