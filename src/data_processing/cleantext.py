import pandas as pd
import re
def clean_text(text):
        if not isinstance(text, str):
            return text

        emoji_pattern = re.compile(
            "[" 
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags
            "\U00002700-\U000027BF"  # dingbats
            "\U0001F900-\U0001F9FF"  # supplemental symbols
            "\U00002600-\U000026FF"  # misc symbols
            "]+", 
            flags=re.UNICODE
        )
        text = emoji_pattern.sub(r"", text)

        text = re.sub(r"[^\w\s.,!?؟]", "", text)  
        text = re.sub(r"\s+", " ", text).strip()   

        return text