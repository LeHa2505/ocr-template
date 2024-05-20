# this is our 'controller.py' file
from sanic import response
from sanic import Blueprint
from sanic.request import Request
from app.services.align_images import align_images
from app.services.image_process import download_pdf_from_url, convert_pdf_to_image, load_template_and_config
from app.services.text_process import cleanup_text
from app.services.ocr_form import ocr_image, visualize_ocr
from numpy import asarray
import pytesseract
import numpy as np
import cv2
import json
import os
import imutils
from ExtractTable import ExtractTable
import json

# extract table api key
api_key = 'a2LhQLQecTvdGrXtbwvsxv6Sft9nL9q9LNNYiSGP'
et_sess = ExtractTable(api_key)

my_bp = Blueprint('my_blueprint')

@my_bp.route('/my_bp')
def my_bp_func(request):
	return response.text('My First Blueprint')

@my_bp.route('/ocr_document', methods=['POST'])
async def ocr_document(request: Request):
	try:
		# custom_config = "-c page_separator=''"
		data = request.json
		doc_type = data.get('doc_type')
		image_url = data.get('image_url')
		# print("1")
		template, config_data = load_template_and_config(doc_type)
		# print("2")
		if template is not None and config_data is not None:
			pdf_document = download_pdf_from_url(image_url)
			image = convert_pdf_to_image(pdf_document, page_number=0)
			aligned = align_images(image, template)
			# print("22222")
			results = ocr_image(aligned, template, OCR_Locations=config_data)
			# print("5")
			visualize_ocr(results, image, aligned)

		# call extract table api
		# table_data = et_sess.process_file(filepath=image_url, pages="all", output_format="json")
		table_data = {}
		# Return the OCR results
		# Tạo dictionary mới
		new_results = {}
		# Lặp qua mỗi cặp key-value trong dictionary cũ
		for key, value in results.items():
			new_results[key] = value[0].strip()
		
		return response.json({"results": {"table": table_data, **new_results}})
	except Exception as e:
		return response.json({"success": False, "error": str(e)})