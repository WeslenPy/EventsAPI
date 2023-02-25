from marshmallow import ValidationError

def find_field_model(model,data,outer_field):
    first = model.query.filter_by(**data).first()
    if not first:raise ValidationError(f'{outer_field} not exists.',outer_field)
    return first


# def compair_field_model(model,)