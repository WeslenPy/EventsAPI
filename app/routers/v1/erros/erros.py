from flask import jsonify
from app.server.instance import app

jwt = app.jwt
app =app.app


@app.errorhandler(405) 
@app.errorhandler(404) 
# @app.errorhandler(400) 
def error_page(error):
    return jsonify(message='router not found',status=404,success=False),404

@app.errorhandler(500) 
def erro_server(error):
    return jsonify(message='Internal server error',status=500,success=False),500

# @jwt.expired_token_loader
# def expired_token(jwt_header, jwt_payload):
#     print('caiu aqui')
#     return{"code":401, "error":"not authorized"}, 401


