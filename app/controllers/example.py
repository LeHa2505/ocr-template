from sanic import Blueprint
from sanic.response import json

example = Blueprint('example', url_prefix='/example')


@example.route('/')
async def bp_root(request):
    return json({'example': 'blueprint'})
