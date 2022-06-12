from flask import jsonify
from app import app

@app.errorhandler(405) 
@app.errorhandler(404) 
def error_page(error):
    return jsonify(message='404 not found',status=404),404

@app.errorhandler(500) 
def erro_server(error):
    return jsonify(message='Server error',status=500),500
