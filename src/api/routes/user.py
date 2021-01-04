from http import HTTPStatus
from flask import Blueprint, request, current_app
from flask_restful import Api, Resource
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_optional
from api.models import User, UserSchema
from api.utils.request_validate import mash_load_validate
from api.utils.passwd import check_password

user_route = Blueprint('user_route', __name__)
user_api = Api(user_route)

class UserItem(Resource):

    @jwt_optional
    def get(self, username:str):
        user = User.get_by_username(username)
        if not user:
            return {'message': 'user do not exist'}, HTTPStatus.BAD_REQUEST
        if user.id == get_jwt_identity():
            ret = UserSchema(
                exclude=('created_at', 'updated_at', 'is_activate')).dump(user)
        else:
            ret = UserSchema(
                exclude=('created_at', 'updated_at', 'is_activate', 'email')).dump(user)
        return ret, HTTPStatus.OK
        


class UserList(Resource):

    user_schema = UserSchema()
    
    def post(self):
        data = request.get_json()
        user = mash_load_validate(self.user_schema, data)
        ret = UserSchema(exclude=('created_at', 'updated_at', 'is_activate')).dump(user.save())
        ret['access_token'] = create_access_token(identity=user.id)
        current_app.logger.info('user %s created successfully', user.username)
        return ret, HTTPStatus.CREATED

class TokenResource(Resource):

    def post(self):
        data = request.get_json()
        user_find_by_name = User.get_by_username(data.get('username'))
        if not user_find_by_name or not \
        check_password(data.get('passwd'), user_find_by_name.passwd):
            return {'message': 'username or password is incorrect'}, HTTPStatus.UNAUTHORIZED
        current_app.logger.info('user %s login', user_find_by_name.username)
        return {'access_token': create_access_token(identity=user_find_by_name.id, fresh=True)}


user_api.add_resource(UserList, '/api/users')
user_api.add_resource(TokenResource, '/api/token')

