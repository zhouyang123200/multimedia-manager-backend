from http import HTTPStatus
from flask_restful import abort
from marshmallow.exceptions import ValidationError


def mash_load_validate(modelschema, data):
    """
    abort request when validate error occur
    """
    try:
        ret = modelschema.load(data)
    except ValidationError as error:
        abort(HTTPStatus.BAD_REQUEST, message=str(error))
    return ret
