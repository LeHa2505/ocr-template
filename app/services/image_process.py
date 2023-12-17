import requests
from io import BytesIO
from PIL import Image
import urllib
import numpy as np
import cv2
import json
import os
import imutils

def download_image_from_url(url):
	try:
		url_response = urllib.request.urlopen(url)
		img_array = np.array(bytearray(url_response.read()), dtype=np.uint8)
		img = cv2.imdecode(img_array, -1)
		return img
	except Exception as e:
		print(f"Error downloading image from URL: {e}")
		return None

def load_template_and_config(doc_type):
	try:
		if doc_type == 1:
			label = 'invoice_1'
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

	except Exception as e:
		print(f"Error loading template and config: {e}")
		return None, None