import re
import json
from utils.text_utils import clean_text


class KeywordService:
    def __init__(self):
        with open('./data/keywords.json', 'r', encoding='utf-8') as f:
            self.keywords = json.load(f)

    def extract_labels(self, description):
        labels = set()
        description = clean_text(description)

        for keyword, label in self.keywords.items():
            if re.search(r'\b' + re.escape(keyword) + r'\b', description, re.IGNORECASE):
                labels.add(label)

        return list(labels)
