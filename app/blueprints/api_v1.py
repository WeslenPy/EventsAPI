from flask import Blueprint


# @v1
v1 = Blueprint(
    name = 'api_v1', 
    import_name = __name__, 
    url_prefix='/api/v1/'
)