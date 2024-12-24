import re
import json
from utils.text_utils import clean_text


class FilterService:
    def __init__(self):
        with open('./data/filter_keywords.json', 'r', encoding='utf-8') as f:
            self.filter_keywords = json.load(f)

        self.job_name_filter_keywords = self.filter_keywords.get(
            "job_name", [])

    def filter_by_job_name(self, job_name):
        job_name = clean_text(job_name)
        for keyword in self.job_name_filter_keywords:
            if re.search(re.escape(keyword), job_name, re.IGNORECASE):
                return True
        return False
