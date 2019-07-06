import re

class Text:
    def __init__(self, text):
        self.text = None
        self.clean(text)

    def clean(self, text):
        patterns = [
            (r'^\s?\d+\.[\s\t]?', ''),  # Numbered bullet points at start of paragraph
            (r' ?( ?\W)\1+', r' \1 '),  # Reduce repeated non alphanumeric characters, -------
            (r'\s\s+', ' '),            # Two or more spaces
            (r'\t', ''),                # Tabulations
            (r'\xa0', ' '),             # Non-breaking space \xa0
            (r'(\r\n|\r|\n)', ' '),     # Line breaks
            (r'\•', ''),                # Bullet points
            (r'^\s?\(\w+\)\s*', ''),
            (r'(\|?\s\|)+', ' '),       # Vertical bars,  such as '| |goals | |'
            (r'^\W*', ''),              # Any non-alphanumerical character at the start of string
            (r'Œ', '-')                 # Replace corrupted dash
        ]
        # Run regex twice so that is not affected by order
        for _ in range(2):
            for pattern, substitute in patterns:
                text = re.sub(pattern, substitute, text)
        self.text = text.strip()
