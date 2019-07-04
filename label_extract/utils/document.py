import os
import PyPDF2
from bs4 import BeautifulSoup
import subprocess
import re
from docx import Document as Docx
from utils.extract_utils import MAPPINGS, format_labels
from utils.text import Text
from io import BytesIO
from langdetect import detect



class Document:
    """
    Doc containing all paragraphs from .doc, .docx, .pdf
    """
    def __init__(self, filepath, filename=None):
        self.paragraphs = []
        self.from_any(filepath)
        self.name = filename


    def from_any(self, filepath):
        base = os.path.basename(filepath)
        extension = os.path.splitext(base)[1].lower()
        if extension == '.doc':
            self.from_word(filepath)
        elif extension == '.pdf':
            self.from_pdf(filepath)
        elif extension == '.html':
            self.from_html(filepath)
        elif extension == '.txt':
            self.from_txt(filepath)
        else:
            print(f"File with extension {extension} not read.")


    def from_word(self, file):
        try:
            # Docx
            paragraphs = Docx(file).paragraphs
            for paragraphs in paragraphs:
                self.paragraphs.append(Text(paragraphs))
        except:
            try:
                # Doc
                extracted_string = subprocess.check_output(['antiword', '-t', file])
                # Decode and split by paragraphs
                extracted_list = extracted_string.decode('utf-8').split('\n\n')
                for paragraph in extracted_list:
                    self.paragraphs.append(Text(paragraph))
            except:
                # If Antiword does not work, convert to txt
                subprocess.run(['textutil', '-convert', 'txt', file])
                file = file.replace('.doc', '.txt')
                with open(file, 'r') as f:
                    data = f.readlines()
                    for paragraph in data:
                        self.paragraphs.append(Text(paragraph))

    def from_pdf(self, file):
        try:
            with open(file, 'rb') as fi:
                pdfReader = PyPDF2.PdfFileReader(BytesIO(fi.read()))
                for i in range(pdfReader.numPages):
                    extracted_string = pdfReader.getPage(i).extractText()
                    extracted_list = extracted_string.split('\n\n')
                    for line in extracted_list:
                        self.paragraphs.append(Text(line))
        except:
            pass

    def from_html(self, file):
        with open(file, 'rb') as f:
            soup = BeautifulSoup(f, 'html.parser')
            # Strip out any code from the text
            for script in soup(["script", "style"]):
                script.decompose()
            for paragraph in soup.stripped_strings:
                try:
                    if detect(paragraph) == 'en':
                        self.paragraphs.append(Text(paragraph))
                except:
                    pass

    def from_txt(self, file):
        with open(file, 'r') as f:
            data = f.readlines()
            for paragraph in data:
                self.paragraphs.append(Text(paragraph))


def extract_labels(doc, p=None):
    labelled = {}
    unlabelled = {}

    for paragraph in doc.paragraphs:
        text = paragraph.text
        # To avoid extracting Millennium Goals
        if 'millennium' not in text.lower() or ' mdg ' not in text.lower():
            patterns = [
                MAPPINGS['g'] + r"\W*\s+(,?\s*\b\d{1,2}\b[and\s\b\d{1,2}\b]*)",
                MAPPINGS['t'] + r"(\s+\d+\.[\d+a-d])",
                MAPPINGS['i'] + r"(\s+\d+\.[\d+a-d]\.\d+)"
            ]
            labelled_text = False
            for pattern in patterns:
                goals = re.findall(pattern, text, re.I)
                for type_, numbers in goals:
                    labels = format_labels(type_, numbers)
                    if labels:
                        if text not in labelled:
                            labelled[text] = {
                                'cats': labels
                            }
                        labelled[text]['cats'].extend(labels)
                        labelled[text]['cats'] = list(set(labelled[text]['cats']))
                        labelled_text = True
            if labelled_text == False:
                unlabelled[text] = None
    if p:
        p.put((labelled, unlabelled))
    else:
        return labelled, unlabelled