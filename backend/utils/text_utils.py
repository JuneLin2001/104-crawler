import re


def clean_text(text):
    if isinstance(text, str):
        text = re.sub(r'[\s\n\r]+', ' ', text)
        return re.sub(r'[^\x20-\x7E\u4e00-\u9fa5]', '', text)
    return text
