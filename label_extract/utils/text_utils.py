import re

class Text:
    def __init__(self, text):
        self.text = None
        self.clean(text)

    def clean(self, text):
        patterns = [
            (r'^\s?\d+\.[\s\t]?', ''),  # Numbered bullet points at start of paragraph
            (r' \--+', ' '),            # Extra long dashes ------
            (r' +', ' '),               # Extra spaces
            (r'\t', ''),                # Tabulations
            (r'\xa0', ' '),             # Non-breaking space \xa0
            (r'(\r\n|\r|\n)', ' '),     # Line breaks. Check this one as there might be some paragraphs that need to be separated
            (r'\•', ''),                 # Bullet points
            (r'^\s?\(\w+\)\s*', '')
        ]
        for pattern, substitute in patterns:
            text = re.sub(pattern, substitute, text)
        self.text = text
