from marshmallow import ValidationError

def unique(model,data:dict[str]):
    for field in data:
        if model.query.filter_by(**{field:data[field]}).first():
            raise ValidationError(f"{field} is already exists.",field)
    return False