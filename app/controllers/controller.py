# this is our 'controller.py' file
from sanic import response
from sanic import Blueprint
from sanic.request import Request
from app.services.align_images import align_images
from app.services.image_process import download_image_from_url, load_template_and_config
from app.services.text_process import cleanup_text
from app.services.ocr_form import ocr_image, visualize_ocr
from numpy import asarray
import pytesseract
import numpy as np
import cv2
import json
import os
import imutils


my_bp = Blueprint('my_blueprint')

@my_bp.route('/my_bp')
def my_bp_func(request):
	return response.text('My First Blueprint')

# @my_bp.route('/ocr/<string:doc_type>/<string:doc_format>', methods={'GET'})
# def ocr_document(doc_type, doc_fomat) 
	
# 	return jsonify(response_data)

@my_bp.route('/ocr_document', methods=['POST'])
async def ocr_document(request: Request):
	try:
		# custom_config = "-c page_separator=''"
		data = request.json
		doc_type = data.get('type')
		image_url = data.get('image_url')

		# Load template image based on doc_type from your database
		# and load config from config.json
		# ...
		template, config_data = load_template_and_config(doc_type)

		if template is not None and config_data is not None:
			image = download_image_from_url(image_url)
			aligned = align_images(image, template)
			results = ocr_image(aligned, template, OCR_Locations=config_data)
			visualize_ocr(results, image, aligned)


		# Return the OCR results
		# Tạo dictionary mới
		new_results = {}
		# Lặp qua mỗi cặp key-value trong dictionary cũ
		for key, value in results.items():
			new_results[key] = value[0].strip()
		return response.json({"success": True, "results": new_results})
	except Exception as e:
		return response.json({"success": False, "error": str(e)})
