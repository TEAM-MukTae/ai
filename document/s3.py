import requests
import PyPDF2
from io import BytesIO
from requests.exceptions import HTTPError

def extract_text_from_pdf(url: str):
    
    textList = []
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        with BytesIO(response.content) as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text()
            textList.append(text)
            
    except HTTPError as e:
        print(f"Error occurred while fetching PDF: {e}")
        return ""
    
    return ''.join(textList)