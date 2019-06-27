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
    def __init__(self, filepath, filename):
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
        #print(filepath)

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
        except Exception as e:
            print(e)

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

    def extract_labels(self, normalize):
        labelled_data = {}
        unlabelled_data = {}

        for paragraph in self.paragraphs:
            text = paragraph.text
            # To avoid extracting Millennium Goals
            if 'millennium' not in text.lower():
                patterns = [
                    MAPPINGS['g'] + r"\W*\s+(,?\s*\b\d{1,2}\b[and\s\b\d{1,2}\b]*)",
                    MAPPINGS['t'] + r"(\s+\d+\.[\d+a-d])",
                    MAPPINGS['i'] + r"(\s+\d+\.[\d+a-d]\.\d+)"
                ]
                for pattern in patterns:
                    goals = re.findall(pattern, text, re.I)

                    for type_, numbers in goals:
                        labels = format_labels(type_, numbers, normalize)
                        if labels:
                            if text not in labelled_data:
                                labelled_data[text] = {
                                    'cats': labels,
                                    'doc_id': self.name
                                }
                            labelled_data[text]['cats'].extend(labels)
                            labelled_data[text]['cats'] = list(set(labelled_data[text]['cats']))
                        else:
                            unlabelled_data[text] = None
            else:
                unlabelled_data[text] = None
        return labelled_data, unlabelled_data

        # If we only find one goal label in the document and the document is not about millenium goals
        # It should include also Sustainable Development Goal, or SDG
        # if len(labelled_data) == 1 and not millenium_text:
        # print("document with online one label. Also check it Millenium goals are added.")
        # print(labelled_data)
        # labelled_data[text]['cats'].extend(all_labels)
        # labelled_data[text]['cats'] = list(set(labelled_data[text]['cats']))
