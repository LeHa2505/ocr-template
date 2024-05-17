from PIL import Image
import urllib
import numpy as np
import cv2
import json
import os
import fitz
def download_pdf_from_url(url):
    try:
        # Open the URL and read the PDF file
        pdf_response = urllib.request.urlopen(url)
        pdf_document = fitz.open(stream=pdf_response.read(), filetype="pdf")
        return pdf_document
    except Exception as e:
        print(f"Error downloading PDF: {e}")
        return None

def convert_pdf_to_image(pdf_document, page_number=0):
    try:
        # Select the desired page from the PDF
        pdf_file = fitz.open(stream=pdf_document, filetype="pdf")
        pdf_page = pdf_file[page_number]
        
        # Get the size of the PDF page in pixels using the 'rect' attribute
        # rect = pdf_page.rect
        # width, height = int(rect.width), int(rect.height)
        
        # # Convert the PDF page to an image using Pillow (PIL)
        # pil_image = Image.frombytes("RGB", (width, height), pdf_page.get_pixmap().samples)
        pixmap = pdf_page.get_pixmap()
        pil_image = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
        # Convert Pillow image to OpenCV image
        img = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        
        return img
    except Exception as e:
        print(f"Error converting PDF to image: {e}")
        return None

def load_template_and_config(doc_type):
    try:
        if doc_type == "invoice":
            label = 'invoice'
            template_folder = f'app/templates/invoices'
            config_folder = f'app/classified/invoices'

            # Load template image
            template_image_path = os.path.join(template_folder, label + '.png')
            template_image = cv2.imread(template_image_path)

            # Load config from JSON file
            config_file_path = os.path.join(config_folder, label + '.json')
            with open(config_file_path, 'r') as config_file:
                config_data = json.load(config_file)

            return template_image, config_data

        # Handle other doc_types if needed
        if doc_type == "bill_of_exchange":
            label = 'exchange'
            template_folder = f'app/templates/bill_of_exchange'
            config_folder = f'app/classified/bill_of_exchange'

            # Load template image
            template_image_path = os.path.join(template_folder, label + '.jpg')
            template_image = cv2.imread(template_image_path)

            # Load config from JSON file
            config_file_path = os.path.join(config_folder, label + '.json')
            with open(config_file_path, 'r') as config_file:
                config_data = json.load(config_file)

            return template_image, config_data

    except Exception as e:
        print(f"Error loading template and config: {e}")
        return None, None