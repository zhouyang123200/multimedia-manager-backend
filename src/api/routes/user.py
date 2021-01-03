from http import HTTPStatus
from flask import Blueprint, request, current_app
from flask_restful import Api, Resource
from api.models import User, UserSchema
from api.utils.request_validate import mash_load_validate

user_route = Blueprint('user_route', __name__)
user_api = Api(user_route)

class UserItem(Resource):

    def get(self, username:str):
        pass


class UserList(Resource):

    user_schema = UserSchema()
    
    def post(self):
        data = request.get_json()
        user = mash_load_validate(self.user_schema, data)
        ret = self.user_schema.dump(user.save())
        return ret, HTTPStatus.CREATED

user_api.add_resource(UserList, '/api/users')

