from flask import jsonify
from app.server.instance import app

app =app.app


@app.errorhandler(405) 
@app.errorhandler(404) 
@app.errorhandler(400) 
def error_page(error):
    return jsonify(message='router not found',code=404,error=True),404

@app.errorhandler(500) 
def erro_server(error):
    return jsonify(message='Internal server error',code=500,error=True),500

