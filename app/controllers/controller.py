# this is our 'controller.py' file
from sanic import response
from sanic import Blueprint

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
        data = request.json
        doc_type = data.get('type')
        image_url = data.get('image_url')

        # Load template image based on doc_type from your database
        # and load config from config.json
        # ...

        # Download the image from the given URL
        # ...

        # Perform OCR
        # ...

        # Return the OCR results
        return response.json({"success": True, "results": ocr_results})
    except Exception as e:
        return response.json({"success": False, "error": str(e)})

