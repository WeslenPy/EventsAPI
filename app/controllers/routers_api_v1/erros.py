from flask import jsonify
from app import app

@app.errorhandler(405) 
@app.errorhandler(404) 
# @app.errorhandler(400) 
def error_page(error):
    return jsonify(message='router not found',status=404,success=False),404

@app.errorhandler(500) 
def erro_server(error):
    return jsonify(message='Internal server error',status=500,success=False),500
