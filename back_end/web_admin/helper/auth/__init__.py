#  @Project FCloudConsole
#  @Homepage https://fsmartstore.com
#  @Copyright (c) 2018 Fujinet Systems JSC. All Rights Reserved.
#  @License All resources of the source code are owned by 'Fujinet Systems JSC'.
#  Intentionally infringing, stealing, exchanging, or trading in all of the
#  resources below without our consent, is a violation of intellectual property
#  rights. So, if you accidentally receive this source code, please send an email
#  to rd-support@fujinet.net, so we can find the best solution for this problem.
import base64
import datetime
import os

import jwt
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from rest_framework_jwt.settings import api_settings

from config.django_settings import STATIC_DIR
from db_accessor.models import User, UserToken, XrefAvatarUser, Profile
from static_serving import StaticServing
from utils.constants import *
from utils.result import Result

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class Authen:
    """
    Supports functions related to user authentication such as login, logout, check credentials,...
    """

    @classmethod
    def parse_request_user_data(cls, request):
        """
        Check user authentication data is exist in request
        :param request: the data that the user submitted the request
        :return: User information contain token and user_id if it contains the request otherwise None
        """

        if (
                KEY_REQUEST_AUTHENTICATION in request.META
                and DEFAULT_WHITE_SPACE_VALUE in request.META[KEY_REQUEST_AUTHENTICATION]
        ):
            authentication_content = str.split(request.META[KEY_REQUEST_AUTHENTICATION])

            return {
                KEY_USER_ID: authentication_content[0],
                KEY_USER_TOKEN: authentication_content[1]
            }

        else:
            return None

    @classmethod
    def parse_login_user_data(cls, request):
        """
        Parse user login information from request
        :param request: the data that the user submitted the request
        :return: a dict containing username and password information if it exists, otherwise None
        """

        if KEY_USER_NAME in request.data and KEY_USER_PASSWORD in request.data:
            return {
                KEY_USER_NAME: request.data[KEY_USER_NAME],
                KEY_USER_PASSWORD: request.data[KEY_USER_PASSWORD],
            }
        else:
            return None

    @classmethod
    def parse_create_user_data(cls, request):
        """
        Parse creation user information from request
        :param request: the data that the user submitted the request
        :return: a dict containing username, password, password_confirm, fullname
        information if it exists, otherwise None
        """

        if (KEY_USER_NAME in request.data and KEY_USER_PASSWORD in request.data and
                KEY_USER_PASSWORD_CONFIRM in request.data and KEY_USER_FIRSTNAME in request.data and
                KEY_USER_EMAIL in request.data and KEY_USER_LASTNAME in request.data):
            return {
                KEY_USER_NAME: request.data[KEY_USER_NAME],
                KEY_USER_EMAIL: request.data[KEY_USER_EMAIL],
                KEY_USER_PASSWORD: request.data[KEY_USER_PASSWORD],
                KEY_USER_PASSWORD_CONFIRM: request.data[KEY_USER_PASSWORD_CONFIRM],
                KEY_USER_FIRSTNAME: request.data[KEY_USER_FIRSTNAME],
                KEY_USER_LASTNAME: request.data[KEY_USER_LASTNAME],
            }
        else:
            return None

    @classmethod
    def create(cls, request):
        # Get user information

        user = cls.parse_create_user_data(request)

        if user:
            result_check_username = User.objects.filter(username=user[KEY_USER_NAME]).values()
            result_check_email = User.objects.filter(email=user[KEY_USER_EMAIL]).values()
            # Check username is existed
            if not result_check_username.exists():
                # Check email is existed
                if not result_check_email.exists():
                    # Create new user
                    result_create_user = User.objects.create(
                        username=user[KEY_USER_NAME],
                        email=user[KEY_USER_EMAIL],
                        password=cls.generate_password(user[KEY_USER_PASSWORD]),
                        full_name=user[KEY_USER_FIRSTNAME] + user[KEY_USER_LASTNAME],
                        role=DEFAULT_ADMIN_ROLE
                    )
                    # Check create user
                    if result_create_user:

                        # Retrive user after create
                        new_user_query_set = User.objects.filter(username=user[KEY_USER_NAME]).values()
                        new_user = list(new_user_query_set)[0]
                        # Create new token
                        # Check update new token for user
                        result = {
                            KEY_USER_ID: new_user.get(KEY_USER_ID),
                        }
                        profile_user = Profile.objects.create(
                            first_name=user[KEY_USER_FIRSTNAME],
                            last_name=user[KEY_USER_LASTNAME],
                            user_id=User.objects.get(user_id=new_user.get(KEY_USER_ID))
                        )
                        if not profile_user:
                            return Result.failed(
                                message='Fail to create profile!',
                            )
                        return Result.success(
                            message='New user registration success!',
                            data=result
                        )

                    else:
                        return Result.failed(
                            message='There was an error in creating new user!'
                        )
                else:
                    return Result.failed(
                        message='Email exists',
                    )
            else:
                return Result.failed(
                    message='Username exists!',
                )
        else:
            return Result.failed(
                message='User information not contained in the request!'
            )

    @classmethod
    def login(cls, request):
        # Get user login data
        user_login_data = cls.parse_login_user_data(request)

        if user_login_data:
            user_information = cls.parse_request_user_data(request)
            if user_information:
                user_data_queryset = User.objects.filter(username=user_login_data.get(KEY_USER_NAME)).values()
                user_data = list(user_data_queryset)[0]

                # Check sessions are still available
                token_available = UserToken.objects.filter(
                    user_id=user_data.get(KEY_USER_ID),
                    token=user_information[KEY_USER_TOKEN]
                ).values().order_by('-created_at')
                if token_available.exists():
                    status_token_available = list(token_available)[0][KEY_TOKEN_STATUS]
                    if status_token_available is DEFAULT_TOKEN_ACTIVE:
                        return Result.failed(
                            message='Pre-logon sessions are still available! '
                                    'You must log out to perform this feature.'
                        )

            validated_user_name = User.objects.filter(
                username=user_login_data[KEY_USER_NAME]
            ).values()

            if validated_user_name.exists():
                # Get all user detail in database
                user_detail = list(validated_user_name)[0]

                validated_user_password = cls.check_user_password(
                    user_login_data[KEY_USER_PASSWORD],
                    user_detail[KEY_USER_PASSWORD]
                )

                if validated_user_password:

                    # Create payload
                    payload = {
                        KEY_USER_ID: user_detail.get(KEY_USER_ID),
                        KEY_USER_NAME: user_detail.get(KEY_USER_NAME),
                        KEY_USER_EMAIL: user_detail.get(KEY_USER_EMAIL),
                        KEY_USER_FULLNAME: user_detail.get(KEY_USER_FULLNAME),
                        KEY_USER_PASSWORD: user_detail.get(KEY_USER_PASSWORD),
                    }

                    # Get new token
                    token = jwt.encode(payload, SECRET_TOKEN_KEY, algorithm='HS256').decode('utf-8')

                    # Set token expiration
                    token_expiration_date = datetime.datetime.now() + datetime.timedelta(
                        days=DEFAULT_TOKEN_EXPIRATION_DATE)

                    # Create new token for user
                    create_token = UserToken.objects.create(user_id=user_detail[KEY_USER_ID], token=token,
                                                            created_at=datetime.datetime.now(),
                                                            expiration_date=token_expiration_date,
                                                            status=DEFAULT_TOKEN_ACTIVE)

                    if create_token:
                        result = {
                            KEY_USER_ID: user_detail[KEY_USER_ID],
                            KEY_USER_TOKEN: 'Token ' + token,
                            KEY_TOKEN_EXPIRATION_DATE: token_expiration_date
                        }

                        return Result.success(message='Log in the user successfully!',
                                              data=result)
                    else:
                        return Result.failed(
                            message='There was an error updating the database!')

                else:
                    return Result.failed(message='Username or password incorrect!')

            else:
                return Result.failed(message='Username or password incorrect!')

        else:
            return Result.failed(
                message='User information not contained in the request!'
            )

    # Login with no check expiration_date
    @classmethod
    def login_no_check_expiration(cls, request):
        # Get user login data
        user_login_data = cls.parse_login_user_data(request)

        if user_login_data:

            user_information = cls.parse_request_user_data(request)

            if user_information:
                # Check sessions are still available
                user_data_queryset = User.objects.filter(username=user_login_data.get(KEY_USER_NAME)).values()
                user_data = list(user_data_queryset)[0]

                # Check sessions are still available
                token_available = UserToken.objects.filter(
                    user_id=user_data.get(KEY_USER_ID),
                    token=user_information[KEY_USER_TOKEN]
                ).values().order_by('-created_at')

                if token_available.exists():
                    status_token_available = list(token_available)[0][KEY_TOKEN_STATUS]
                    if status_token_available is DEFAULT_TOKEN_ACTIVE:
                        return Result.failed(
                            message='Pre-logon sessions are still available! '
                                    'You must log out to perform this feature.'
                        )

            validated_user_name = User.objects.filter(
                username=user_login_data[KEY_USER_NAME]
            ).values()

            if validated_user_name.exists():
                # Get all user detail in database
                user_detail = list(validated_user_name)[0]

                validated_user_password = cls.check_user_password(
                    user_login_data[KEY_USER_PASSWORD],
                    user_detail[KEY_USER_PASSWORD]
                )

                if validated_user_password:

                    # Create payload
                    payload = {
                        KEY_USER_ID: user_detail.get(KEY_USER_ID),
                        KEY_USER_NAME: user_detail.get(KEY_USER_NAME),
                        KEY_USER_EMAIL: user_detail.get(KEY_USER_EMAIL),
                        KEY_USER_FULLNAME: user_detail.get(KEY_USER_FULLNAME),
                        KEY_USER_PASSWORD: user_detail.get(KEY_USER_PASSWORD),
                    }

                    # Get new token
                    token = jwt.encode(payload, SECRET_TOKEN_KEY, algorithm='HS256').decode('utf-8')
                    # Create new token for user
                    create_token = UserToken.objects.create(user_id=user_detail[KEY_USER_ID], token=token,
                                                            status=DEFAULT_TOKEN_ACTIVE)

                    if create_token:
                        result = {
                            KEY_USER_ID: user_detail[KEY_USER_ID],
                            KEY_USER_TOKEN: token
                        }

                        return Result.success(message='Log in the user successfully!',
                                              data=result)
                    else:
                        return Result.failed(
                            message='There was an error updating the database!')

                else:
                    return Result.failed(message='Username or password incorrect!')

            else:
                return Result.failed(message='Username or password incorrect!')

        else:
            return Result.failed(
                message='User information not contained in the request!'
            )

    @classmethod
    def image_as_base64(cls, image_file, format='jpeg'):
        """
        :param `image_file` for the complete path of image.
        :param `format` is format for image, eg: `png` or `jpg`.
        """
        if not os.path.isfile(image_file):
            return None

        encoded_string = ''
        with open(image_file, 'rb') as img_f:
            encoded_string = base64.b64encode(img_f.read())
        return 'data:image/%s;base64,%s' % (format, encoded_string)

    @classmethod
    def set_avatar(cls, request):
        user_information = jwt.decode(cls.parse_request_user_data(request).get('token'), SECRET_TOKEN_KEY)
        user_id = user_information[KEY_USER_ID]
        avatar = request.FILES['avatar']
        try:
            XrefAvatarUser.objects.get(user_id=User.objects.get(user_id=user_id)).delete()
        except XrefAvatarUser.DoesNotExist:
            return Result.failed(
                message='Some data error!'
            )
        _, serve_urls, exc = StaticServing.save_res(
            [avatar],
            [
                'user_avatar',
                f'{user_id}'
            ]
        )
        if exc is not None:
            raise IOError(f'Save image file failed: {exc}')

        img_url = serve_urls[0]

        try:
            result_create_avatar = XrefAvatarUser.objects.create(
                user_id=User.objects.get(
                    user_id=user_id
                ),
                avatar_file=img_url,
            )

        except Exception as exc:
            # log.error(f'Save person image to db failed: {exc}')
            return Result.failed(
                message=f'Save person image to db failed: {exc}'
            )

        if not result_create_avatar:
            return Result.failed(
                message='Have some problem when add image data!'
            )
        return Result.success(
            message='Success set avatar!'
        )

    @classmethod
    def get_avatar(cls, request):
        user_information = jwt.decode(cls.parse_request_user_data(request).get('token'), SECRET_TOKEN_KEY)
        if not user_information:
            return Result.failed(
                message='Missing data from request!'
            )
        try:
            check_image = XrefAvatarUser.objects.get(
                user_id=User.objects.get(user_id=user_information[KEY_USER_ID])
            )
            link = check_image.avatar_file.split('/static')
            result = cls.image_as_base64(STATIC_DIR + link[1])
            return Result.success(
                message='Get image of person success!',
                data=result
            )
        except (User.DoesNotExist, XrefAvatarUser.DoesNotExist):
            return Result.failed(
                message='User doesnt exist!'
            )

    @classmethod
    def change_password(cls, request):
        old_password= request.data.get('old_password')
        #old_password = cls.generate_password(request.data.get('old_password'))
        new_password = cls.generate_password(request.data.get('new_password'))
        user_information = jwt.decode(cls.parse_request_user_data(request).get('token'), SECRET_TOKEN_KEY)
        #print(old_password)
        cur_user = User.objects.get(user_id=user_information[KEY_USER_ID])
        validated_user_password = cls.check_user_password(
            old_password,
            cur_user.password
        )
        if validated_user_password:
            cur_user.password = new_password
            cur_user.save()
            return Result.success(
                message='Success change password!'
            )
        else:
            return Result.failed(
                message='Old password doesnt match!'
            )

    @classmethod
    def logout(cls, request):

        # Get user information
        user_information = jwt.decode(cls.parse_request_user_data(request).get('token'), SECRET_TOKEN_KEY)

        # Check user is existed
        if user_information:

            # Set user token is logout
            token_available = UserToken.objects.filter(user_id=user_information[KEY_USER_ID],
                                                       token=cls.parse_request_user_data(request).get(
                                                           'token')).values().order_by('-created_at')

            if token_available.exists():
                token_status_available = list(token_available)[0][KEY_TOKEN_STATUS]

                if token_status_available is DEFAULT_TOKEN_ACTIVE:
                    # Set user token is logout
                    result_logout = UserToken.objects.filter(user_id=user_information[KEY_USER_ID],
                                                             token=cls.parse_request_user_data(request).get(
                                                                 'token')).update(
                        status=DEFAULT_TOKEN_DEACTIVE)

                    if result_logout:
                        return Result.success(message='Log out the user successfully!')
                    else:
                        return Result.failed(
                            message='Can not sign out of account because your user credentials are not valid!')
                else:
                    return Result.failed(
                        message='Your account credentials expired!')
            else:
                return Result.failed(
                    message='The token code you provided is not valid!')
        else:
            return Result.failed(
                message='User information not contained in the request!')

    # Reset account for master admin with secret key
    @classmethod
    def reset_master_admin_password(cls, request):

        secret_key = request.data.get(KEY_SECRET_RESTORE_MASTER_ADMIN_PASSWORD)

        master_admin = User.objects.filter(username=DEFAULT_MASTER_ADMIN_USER_NAME).values()

        if secret_key == SECRET_RESET_MASTER_ADMIN_PASSWORD_KEY:
            new_password = cls.generate_password(DEFAULT_MASTER_ADMIN_PASSWORD)
            if master_admin:
                restore_password = User.objects.filter(username=DEFAULT_MASTER_ADMIN_USER_NAME).update(
                    password=new_password)

                if restore_password:
                    return Result.success(
                        message='Reset password for super administrator success!', data={
                            KEY_USER_NAME: DEFAULT_MASTER_ADMIN_USER_NAME,
                            KEY_USER_PASSWORD: DEFAULT_MASTER_ADMIN_PASSWORD
                        })
                else:
                    return Result.success(
                        message='Reset password for super administrator failed!')
            else:
                create_master_admin = User.objects.create(
                    username=DEFAULT_MASTER_ADMIN_USER_NAME,
                    password=new_password,
                    full_name=DEFAULT_MASTER_ADMIN_FULL_NAME,
                    role=DEFAULT_ADMIN_ROLE,
                    status=DEFAULT_USER_STATUS
                )

                if create_master_admin:
                    return Result.success(
                        message='Reset password for super administrator success!', data={
                            KEY_USER_NAME: DEFAULT_MASTER_ADMIN_USER_NAME,
                            KEY_USER_PASSWORD: DEFAULT_MASTER_ADMIN_PASSWORD
                        })
                else:
                    return Result.success(
                        message='Reset password for super administrator failed!')
        else:
            return Result.failed(
                message='The security key to reset the account is incorrect!'
            )

    # Create new token
    @classmethod
    def create_token(cls, user_id, password):
        return make_password(
            password=str(user_id) + SECRET_TOKEN_KEY + password + datetime.datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S'), salt=None)

    # Generate password hasing
    @classmethod
    def generate_password(cls, password):
        return make_password(password=password + SECRET_PASSWORD_KEY, salt=None)

    # Check user password
    @classmethod
    def check_user_password(cls, password, encoded):
        return check_password(password=password + SECRET_PASSWORD_KEY, encoded=encoded)

    @classmethod
    def is_authenticated(cls, user_id, token):
        user_token = UserToken.objects.filter(
            user_id=user_id,
            token=token,
            status=DEFAULT_TOKEN_ACTIVE
        ).values()

        if user_token.exists():
            expiration_date = list(user_token)[0]['expiration_date']
            """
            Reference: https://stackoverflow.com/questions/15307623/
            cant-compare-naive-and-aware-datetime-now-challenge-datetime-end
            Note: f USE_TZ=True then timezone.now() returns a timezone-aware datetime object even
            if pytz is not installed (though it might be recommended to install for other reasons).
            """
            # Compare expiration date vs datetime now
            if expiration_date and expiration_date >= timezone.now():
                return True

            else:
                return False

        else:
            return False

    @classmethod
    def check_authentication(cls, request):
        # Get user information
        user_information = cls.parse_request_user_data(request)

        if user_information:
            return Authen.is_authenticated(
                user_information[KEY_USER_ID],
                user_information[KEY_USER_TOKEN]
            )
        return False

    @classmethod
    def get_profile(cls, request):
        user_information = jwt.decode(cls.parse_request_user_data(request).get('token'), SECRET_TOKEN_KEY)
        user_id = user_information[KEY_USER_ID]
        if not user_id:
            return Result.failed(
                message='Missing data in request!'
            )
        try:
            profile_data = Profile.objects.get(
                user_id=User.objects.get(user_id=user_id)
            )
            print(profile_data)
            result = {
                KEY_PROFILE_ADDRESS: profile_data.address,
                KEY_PROFILE_COMPANY: profile_data.company,
                KEY_USER_FIRSTNAME: profile_data.first_name,
                KEY_USER_LASTNAME: profile_data.last_name,
                KEY_USER_EMAIL: user_information[KEY_USER_EMAIL],
                KEY_USER_NAME: user_information[KEY_USER_NAME],
            }
        except (User.DoesNotExist, Profile.DoesNotExist):
            return Result.failed(
                message='Data doesnt exist!'
            )
        return Result.success(
            message='Success get profile!',
            data=result
        )

    @classmethod
    def parse_set_profile_data(cls, request):

        if (KEY_USER_FIRSTNAME in request.data and
                KEY_USER_LASTNAME in request.data and KEY_PROFILE_ADDRESS in request.data and
                KEY_PROFILE_COMPANY in request.data):
            return {
                KEY_USER_FIRSTNAME: request.data[KEY_USER_FIRSTNAME],
                KEY_USER_LASTNAME: request.data[KEY_USER_LASTNAME],
                KEY_PROFILE_ADDRESS: request.data[KEY_PROFILE_ADDRESS],
                KEY_PROFILE_COMPANY: request.data[KEY_PROFILE_COMPANY],
            }
        else:
            return None

    @classmethod
    def set_profile(cls, request):
        profile_data = cls.parse_set_profile_data(request)
        user_information = jwt.decode(cls.parse_request_user_data(request).get('token'), SECRET_TOKEN_KEY)
        user_id = user_information[KEY_USER_ID]
        if not profile_data:
            return Result.failed(
                message='Missing data in request!'
            )
        profile = Profile.objects.get(user_id=User.objects.get(user_id=user_id))
        profile.first_name = profile_data[KEY_USER_FIRSTNAME]
        profile.last_name = profile_data[KEY_USER_LASTNAME]
        profile.address = profile_data[KEY_PROFILE_ADDRESS]
        profile.company = profile_data[KEY_PROFILE_COMPANY]
        profile.save()
        try:
            avatar = request.FILES['avatar']
        except Exception as exc:
            return Result.failed(
                message=f'Some data error!{exc}'
            )
        print(request.FILES)
        if avatar:
            avatar_user = list(XrefAvatarUser.objects.filter(
                user_id=User.objects.get(user_id=user_id)
            ))
            if avatar_user:
                try:
                    XrefAvatarUser.objects.get(user_id=User.objects.get(user_id=user_id)).delete()
                except XrefAvatarUser.DoesNotExist:
                    return Result.failed(
                        message='Some data error!'
                    )
            _, serve_urls, exc = StaticServing.save_res(
                [avatar],
                [
                    'user_avatar',
                    f'{user_id}'
                ]
            )
            if exc is not None:
                raise IOError(f'Save image file failed: {exc}')

            img_url = serve_urls[0]

            try:
                result_create_avatar = XrefAvatarUser.objects.create(
                    user_id=User.objects.get(
                        user_id=user_id
                    ),
                    avatar_file=img_url,
                )

            except Exception as exc:
                # log.error(f'Save person image to db failed: {exc}')
                return Result.failed(
                    message=f'Save person image to db failed: {exc}'
                )

            if not result_create_avatar:
                return Result.failed(
                    message='Have some problem when add image data!'
                )
        return Result.success(
            message='Success change profile!'
        )

