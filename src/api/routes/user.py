"""
user and authentication apis
"""
import os
import shutil
import pathlib
from http import HTTPStatus
from flask import Blueprint, request, current_app, url_for
from flask_restful import Api, Resource
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_optional,
    jwt_required,
    get_raw_jwt
    )
from api.models import User, UserSchema, AvatarSchema
from api.utils.request_validate import mash_load_validate
from api.utils.passwd import check_password, verify_token, generate_token
from api.utils.tasks import send_mail

user_route = Blueprint('user_route', __name__)
user_api = Api(user_route)

black_list = set()

class UserItem(Resource):
    """
    user info get api
    """

    @jwt_optional
    def get(self, username:str):
        """
        get user info by username
        """
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
    """
    user list get api
    """

    user_schema = UserSchema()

    def post(self):
        """
        user sign in api and send email
        """

        data = request.get_json()
        user = mash_load_validate(self.user_schema, data)
        ret = UserSchema(exclude=('created_at', 'updated_at', 'is_activate')).dump(user.save())
        token = generate_token(user.email, salt='activate')
        subject = 'Please confirm your registration'
        link = url_for('user_route.useractivateresource', token=token, _external=True)
        text = 'Hi, Thanks for using multimedia manager! Please confirm your registration\
             by clicking on the link: {}'.format(link)
        send_mail.delay(subject=subject, sender='zhouyang123200@sina.com', recipients=[user.email],
         text=text)
        # current_app.logger.info('user %s send activate email successfully', user.username)
        return ret, HTTPStatus.CREATED


class TokenResource(Resource):
    """
    jwt token generate api
    """

    def post(self):
        """
        create token
        """

        data = request.get_json()
        user_find_by_name = User.get_by_username(data.get('username'))
        if not user_find_by_name or not \
        check_password(data.get('passwd'), user_find_by_name.passwd):
            return {'message': 'username or password is incorrect'}, HTTPStatus.UNAUTHORIZED
        if not user_find_by_name.is_activate:
            return {'message': 'the user is not activate'}, HTTPStatus.BAD_REQUEST
        current_app.logger.info('user %s login', user_find_by_name.username)
        return {'access_token': create_access_token(identity=user_find_by_name.id, fresh=True)}


class RevokeResource(Resource):
    """
    logout api
    """

    @jwt_required
    def post(self):
        """
        disable jwt token
        """

        jti = get_raw_jwt()['jti']
        black_list.add(jti)
        return {'message': 'Successfully logged out'}, HTTPStatus.OK


class UserActivateResource(Resource):
    """
    user activate api using mail
    """

    def get(self, token):
        """
        activate user by the token from mail
        """

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


class UserAvatarResource(Resource):
    """
    user avatar api
    """

    avatar_schema = AvatarSchema()
    user_schema = UserSchema()

    def put(self):
        """
        modify user avatar api
        """
        raw_data = request.get_json()
        data = mash_load_validate(self.avatar_schema, raw_data)
        user = User.query.filter_by(id=get_jwt_identity())
        self.save_image(data['file_name'], data['image_name'], user.username)
        user.avatar_image = data['image_name']
        user.save()
        ret = self.user_schema.dump(user)

        return ret, HTTPStatus.OK

    @staticmethod
    def save_image(file_name:str, image_name:str, username:str):
        """
        rename file name and save it to user's specified path
        """
        upload_path = current_app.config['UPLOAD_FOLDER']
        storage_path = current_app.config['FILE_STORAGE_PATH']
        storage_dir = os.path.join(storage_path, 'users', username)
        source_path = os.path.join(upload_path, file_name)
        obj_path = os.path.join(storage_dir, image_name)
        pathlib.Path(storage_dir).mkdir(parents=True, exist_ok=True)
        shutil.move(source_path, obj_path)


user_api.add_resource(UserList, '/api/users')
user_api.add_resource(TokenResource, '/api/token')
user_api.add_resource(RevokeResource, '/api/revoke')
user_api.add_resource(UserActivateResource, '/api/users/activate/<regex("[a-zA-Z.0-9-_]+"):token>')
