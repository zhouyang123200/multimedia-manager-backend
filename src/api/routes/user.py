from http import HTTPStatus
from flask import Blueprint, request, current_app, url_for
from flask_restful import Api, Resource
from flask_mail import Message
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_optional,
    jwt_required,
    get_raw_jwt
    )
from api.models import User, UserSchema
from api.utils.request_validate import mash_load_validate
from api.utils.passwd import check_password, verify_token, generate_token

user_route = Blueprint('user_route', __name__)
user_api = Api(user_route)

black_list = set()

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
        token = generate_token(user.email, salt='activate')
        subject = 'Please confirm your registration'
        link = url_for('user_route.useractivateresource', token=token, _external=True)
        text = 'Hi, Thanks for using SmileCook! Please confirm your registration by clicking on the link: {}'.format(link)
        msg = Message(subject, sender='zhouyang123200@sina.com', recipients=[user.email], body=text)
        current_app.mail.send(msg)
        current_app.logger.info('user %s send activate email successfully', user.username)
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


class RevokeResourse(Resource):

    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        black_list.add(jti)
        return {'message': 'Successfully logged out'}, HTTPStatus.OK


class UserActivateResource(Resource):

    def get(self, token):
        email = verify_token(token, salt='activate')
        if not email:
            return {'message': 'Invalid token or token expired'}, HTTPStatus.BAD_REQUEST
        user = User.query.filter_by(email=email).first()
        if not user:
            return {'message': 'User not found'}, HTTPStatus.NOT_FOUND
        if user.is_activate:
            return {'message': 'The user account is already activated'}, HTTPStatus.BAD_REQUEST
        user.is_activate = True
        user.save()
        return {}, HTTPStatus.NO_CONTENT



class MailResource(Resource):

    def post(self):
        data = request.get_json()
        message = data['message']
        msg = Message('hello', sender='zhouyang123200@sina.com', recipients=['zhouyang123200@hotmail.com'])
        msg.body = message
        current_app.logger.info('start send mail')
        current_app.mail.send(msg)


user_api.add_resource(UserList, '/api/users')
user_api.add_resource(TokenResource, '/api/token')
user_api.add_resource(RevokeResourse, '/api/revoke')
user_api.add_resource(MailResource, '/api/testmail')
user_api.add_resource(UserActivateResource, '/api/users/activate/<regex("[a-zA-Z.0-9-_]+"):token>')

