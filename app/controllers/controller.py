# this is our 'controller.py' file
from sanic import response
from sanic import Blueprint

my_bp = Blueprint('my_blueprint')

@my_bp.route('/my_bp')
def my_bp_func(request):
	return response.text('My First Blueprint')

@my_bp.route('/ocr/<string:doc_type>/<string:doc_format>', methods={'GET'})
def ocr_document(doc_type, doc_fomat) 

	return jsonify(response_data)

