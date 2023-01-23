from marshmallow import ValidationError

def find_field_model(model,field,data,outer_field):
    first = model.query.filter_by(**{field:data}).first()
    if not first:raise ValidationError(f'{outer_field} not exists.',field)
    return True