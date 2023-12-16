# this is our 'controller.py' file
from sanic import response
from sanic import Blueprint
from sanic.request import Request
from app.services.align_images import align_images
from numpy import asarray
import pytesseract
import numpy as np
import cv2
import json
import os
import imutils


def cleanup_text(text):
    return "".join([c if ord(c) < 128 else "" for c in text]).strip()

my_bp = Blueprint('my_blueprint')

import requests
from io import BytesIO
from PIL import Image
import urllib

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

@my_bp.route('/my_bp')
def my_bp_func(request):
	return response.text('My First Blueprint')

# @my_bp.route('/ocr/<string:doc_type>/<string:doc_format>', methods={'GET'})
# def ocr_document(doc_type, doc_fomat) 
	
# 	return jsonify(response_data)

@my_bp.route('/ocr_document', methods=['POST'])
async def ocr_document(request: Request):
	try:
		data = request.json
		doc_type = data.get('type')
		image_url = data.get('image_url')

		# Load template image based on doc_type from your database
		# and load config from config.json
		# ...
		template, config_data = load_template_and_config(doc_type)

		if template is not None and config_data is not None:
			image = download_image_from_url(image_url)
			print("img: ", image)
			# if image:
			# Tiếp tục xử lý ảnh
			# ...
			print("[Info] aligning images...")
			aligned = align_images(image, template)

			print("[Info] OCR'ing document...")
			parsingResults = []
			OCR_Locations = config_data
			for loc in OCR_Locations:
				bbox = loc["bbox"]
				(x, y, w, h) = bbox
				# roi = aligned[y:y+h, x:x+w]
				roi = aligned[y: h, x: w]

				rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
				text = pytesseract.image_to_string(rgb)
				
				for line in text.split("\n"):
					if len(line) == 0:
						continue

					lower = line.lower()
					count = sum([lower.count(x) for x in loc["filter_keywords"]])

					# if count == 0:
					parsingResults.append((loc, line))

			results = {}

			for (loc, line) in parsingResults:
				print("loc:", loc)
				r = results.get(loc['id'], None)

				if r is None:
					results[loc['id']] = (line, loc)
				
				else:
					(existingText, loc) = r
					text = "{}\n{}".format(existingText, line)

					results[loc["id"]] = (text, loc)

			for (locID, result) in results.items():
				(text, loc) = result

				print(loc["id"])
				print("=" * len(loc["id"]))
				print("{}\n\n".format(text))

				(x, y, w, h) = loc["bbox"]
				clean = cleanup_text(text)

				cv2.rectangle(aligned, (x, y), (x+w, y+h), (0, 255, 0), 2)

				for (i, line) in enumerate(clean.split("\n")):
					startY = y + (i * 70) + 40
					cv2.putText(aligned, line, (x, startY), cv2.FONT_HERSHEY_SIMPLEX, 1.8, (0, 0, 255), 5)

			cv2.imwrite("input.jpg", imutils.resize(image))
			cv2.imwrite("Output.jpg", imutils.resize(aligned))
			print("[Info] aligned image saved as new.jpg")
			# cv2.imshow("Input", imutils.resize(image))
			# cv2.imshow("Output", imutils.resize(aligned))
			cv2.waitKey(0)
			return response.text('Done')

			# Perform OCR
			# ...

		# Return the OCR results
		return response.json({"success": True, "results": ocr_results})
	except Exception as e:
		return response.json({"success": False, "error": str(e)})
