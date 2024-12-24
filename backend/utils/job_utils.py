from utils.text_utils import clean_text
from services.keyword_service import KeywordService

keyword_service = KeywordService()


def generate_job_info(job):
    job_name = clean_text(job.get("jobName", ""))

    if not job_name:
        return None

    job_info = {
        "Appear Date": clean_text(job.get("appearDate", "")),
        "Company Name": clean_text(job.get("custName", "")),
        "Job Name": job_name,
        "Description": clean_text(job.get("description", "")),
        "Job Address": clean_text(job.get("jobAddrNoDesc", "")),
        "Job Link": clean_text(job.get("link", {}).get("job", "")),
        "Labels": keyword_service.extract_labels(job.get("description", "")),
        "isFiltered": False
    }

    return job_info
