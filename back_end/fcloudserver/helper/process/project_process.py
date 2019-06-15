#  @Project FCloudConsole
#  @Homepage https://fsmartstore.com
#  @Copyright (c) 2018 Fujinet Systems JSC. All Rights Reserved.
#  @License All resources of the source code are owned by 'Fujinet Systems JSC'.
#  Intentionally infringing, stealing, exchanging, or trading in all of the
#  resources below without our consent, is a violation of intellectual property
#  rights. So, if you accidentally receive this source code, please send an email
#  to rd-support@fujinet.net, so we can find the best solution for this problem.
import hashlib
import time
from hashlib import blake2b
from json import JSONEncoder
import jwt
from django.contrib.auth.hashers import make_password
from config import django_settings
# from config.log_config import log
from db_accessor.models import Project, Function, ApiKey
from utils.constants import *
from utils.result import Result


class ProjectProcess:

    @classmethod
    def parse_create_project_data(cls, request):
        """
        Parse creation project data from request
        :param request: the data that the user submitted the request
        :return: a dict containing project name, project code if it exists, otherwise None
        """

        if KEY_PROJECT_NAME in request.data and KEY_PROJECT_CODE in request.data:
            return {
                KEY_PROJECT_NAME: request.data[KEY_PROJECT_NAME],
                KEY_PROJECT_CODE: request.data[KEY_PROJECT_CODE],
            }
        else:
            return None

    @classmethod
    def parse_choose_project_data(cls, request):
        """
        Parse choose project data from request
        :param request: the data that the user submitted the request
        :return: a dict containing project code if it exists, otherwise None
        """

        if KEY_PROJECT_CODE in request.data:
            return {
                KEY_PROJECT_CODE: request.data[KEY_PROJECT_CODE],
            }
        else:
            return None

    @classmethod
    def parse_get_all_project_data(cls, request):
        """
        Parse get all project data from request
        :param request: the data that the user submitted the request
        :return: a dict containing project id if it exists, otherwise None
        """

        if KEY_PROJECT_OWNER_ID in request.data:
            return {
                KEY_PROJECT_OWNER_ID: request.data[KEY_PROJECT_OWNER_ID],
            }
        else:
            return None

    @classmethod
    def parse_add_function_data(cls, request):
        """
        Parse add function data from request
        :param request: the data that the user submitted the request
        :return: a dict containing project id, function id if it exists, otherwise None
        """

        if KEY_PROJECT_ID in request.data and KEY_FUNCTION_ID in request.data:
            return {
                KEY_PROJECT_ID: request.data[KEY_PROJECT_ID],
                KEY_FUNCTION_ID: request.data[KEY_FUNCTION_ID],
            }
        else:
            return None

    @classmethod
    def parse_get_function_project_data(cls, request):
        """
        Parse get function of project data from request
        :param request: the data that the user submitted the request
        :return: a dict containing project id if it exists, otherwise None
        """

        if KEY_PROJECT_ID in request.data:
            return {
                KEY_PROJECT_ID: request.data[KEY_PROJECT_ID],
            }
        else:
            return None

    @classmethod
    def make_project_secret_key(cls, project_id):
        time_now = int(round(time.time() * 1000))
        id_hash = '{}{}'.format(str(project_id).zfill(ID_LENGTH), str(time_now)).encode('utf-8')
        return hashlib.sha256(id_hash).hexdigest()

    @classmethod
    def create_project_code(cls, project_id, current_time_ms):
        return blake2b(key=(
            '{}{}'.format(
                str(project_id).zfill(ID_LENGTH),
                str(current_time_ms).zfill(ID_LENGTH)
            ).encode('utf-8')), digest_size=5
        ).hexdigest()

    @classmethod
    def create_project(cls, request):

        project = cls.parse_create_project_data(request)
        user_information = jwt.decode(
            cls.parse_request_user_data(request).get('token'), SECRET_TOKEN_KEY
        )
        if project[KEY_PROJECT_NAME] == '' or project[KEY_PROJECT_CODE] == '':
            return Result.failed(
                message='You need input project name and project code!'
            )
        if project:
            result_check_project_code = Project.objects.filter(
                project_code=project[KEY_PROJECT_CODE],
                status=DEFAULT_STATUS_ACTIVE,
                owner_user_id=user_information[KEY_USER_ID],
            ).values()
            if not result_check_project_code.exists():
                result_create_project = Project.objects.create(
                    project_name=project[KEY_PROJECT_NAME],
                    project_code=project[KEY_PROJECT_CODE],
                    owner_user_id=user_information[KEY_USER_ID],
                    status=DEFAULT_STATUS_ACTIVE
                )

                if result_create_project:
                    try:
                        result = Project.objects.get(
                            project_code=project[KEY_PROJECT_CODE],
                            status=DEFAULT_STATUS_ACTIVE
                        )
                        result.secret_key = cls.make_project_secret_key(result.project_id).upper()
                        result.save()
                    except Project.DoesNotExist:
                        return Result.failed(
                            message='There was an error in creating new project!'
                        )
                    new_project_query_set = Project.objects.filter(
                        project_code=project[KEY_PROJECT_CODE],
                        status=DEFAULT_STATUS_ACTIVE
                    ).values()
                    new_project = list(new_project_query_set)[0]
                    result = {
                        KEY_PROJECT_ID: new_project.get(KEY_PROJECT_ID),
                        KEY_PROJECT_CODE: new_project.get(KEY_PROJECT_CODE),
                        KEY_PROJECT_NAME: new_project.get(KEY_PROJECT_NAME),
                    }
                    return Result.success(
                        message='Create new project success!',
                        data=result
                    )

                else:
                    return Result.failed(
                        message='There was an error in creating new project!'
                    )
            else:
                return Result.failed(
                    message='Project code exists!',
                )
        else:
            return Result.failed(
                message='Project data not contained in the request!'
            )

    @classmethod
    def choose_project(cls, request):
        user_information = jwt.decode(
            cls.parse_request_user_data(request).get('token'), SECRET_TOKEN_KEY
        )
        project_code = request.GET['project_code']
        if project_code:
            result_choose_project = Project.objects.filter(
                project_code=project_code,
                status=DEFAULT_STATUS_ACTIVE,
                owner_user_id=user_information[KEY_USER_ID],
            )
            if result_choose_project:
                chose_project = list(result_choose_project.values())[0]
                result = {
                    KEY_PROJECT_ID: chose_project.get(KEY_PROJECT_ID),
                    KEY_PROJECT_NAME: chose_project.get(KEY_PROJECT_NAME),
                    KEY_PROJECT_CODE: chose_project.get(KEY_PROJECT_CODE),
                    KEY_PROJECT_SECRET_KEY: chose_project.get(KEY_PROJECT_SECRET_KEY),
                }
                return Result.success(
                    message='Choose project success!',
                    data=result
                )
            else:
                return Result.failed(
                    message='Project does not exist'
                )
        else:
            return Result.failed(
                message='Failed to choose project!'
            )

    @classmethod
    def delete_project(cls, request):
        project_code = request.GET['project_code']
        user_information = jwt.decode(
            cls.parse_request_user_data(request).get('token'), SECRET_TOKEN_KEY
        )
        if project_code:
            try:
                result_choose_project = Project.objects.get(
                    project_code=project_code,
                    status=DEFAULT_STATUS_ACTIVE,
                    owner_user_id=user_information[KEY_USER_ID],
                )
                project_id_delete = result_choose_project.project_id
                result_choose_project.status = DEFAULT_STATUS_DEACTIVE
                result_choose_project.save()
                result_function_in_project = ApiKey.objects.filter(
                    project_id=Project.objects.get(project_id=project_id_delete)
                )
                result_function_in_project.delete()
                return Result.success(
                    message='Delete project success!',
                )
            except Project.DoesNotExist:
                return Result.failed(
                    message='Project does not exist'
                )
        else:
            return Result.failed(
                message='Failed to delete project!'
            )

    @classmethod
    def parse_request_user_data(cls, request):
        """
        Check user authentication data is exist in request
        :param request: the data that the user submitted the request
        :return: User information contain token and user_id, user_token if it contains the request otherwise None
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
    def get_all_project(cls, request):
        # Get user  information
        user_information = jwt.decode(cls.parse_request_user_data(request).get('token'), SECRET_TOKEN_KEY)
        if user_information:
            result_get_all_project = Project.objects.filter(
                owner_user_id=user_information[KEY_USER_ID],
                status=DEFAULT_STATUS_ACTIVE
            )
            if result_get_all_project:
                result_project = list(result_get_all_project.values())
                return Result.success(
                    message='Get all project success!',
                    data=result_project,
                )
            else:
                return Result.failed(
                    message='Owner user doesnt exist or there is no project ',
                )
        else:
            return Result.failed(
                message='Project data not contained in the request!'
            )

    # Generate password hash
    @classmethod
    def generate_password(cls, password):
        return make_password(password=password + SECRET_PASSWORD_KEY, salt=None)

    @classmethod
    def add_function(cls, request):
        project_information = cls.parse_add_function_data(request)
        if project_information:
            result_project_by_id = Project.objects.filter(
                project_id=project_information[KEY_PROJECT_ID]
            )
            if result_project_by_id:
                result_function_by_id = Function.objects.filter(
                    function_id=project_information[KEY_FUNCTION_ID]
                )
                if result_function_by_id:
                    check_api_key = ApiKey.objects.filter(
                        project_id=Project.objects.get(project_id=project_information[KEY_PROJECT_ID]),
                        function_id=Function.objects.get(function_id=project_information[KEY_FUNCTION_ID])
                    )
                    if not check_api_key:
                        api_key = {
                            KEY_PROJECT_ID: project_information[KEY_PROJECT_ID],
                            KEY_FUNCTION_ID: project_information[KEY_FUNCTION_ID],
                        }
                        api_key_encode = cls.generate_password(JSONEncoder().encode(api_key))
                        result_add_function = ApiKey.objects.create(
                            project_id=Project.objects.get(project_id=project_information[KEY_PROJECT_ID]),
                            function_id=Function.objects.get(function_id=project_information[KEY_FUNCTION_ID]),
                            api_key=api_key_encode,
                            status=DEFAULT_STATUS_ACTIVE
                        )
                        if result_add_function:
                            # Retrieve api key after create
                            new_api_key_query_set = ApiKey.objects.filter(
                                api_key=api_key_encode,
                                status=DEFAULT_STATUS_ACTIVE
                            ).values()
                            new_api_key = list(new_api_key_query_set)[0]
                            result = {
                                KEY_API_KEY_ID: new_api_key.get(KEY_API_KEY_ID),
                                KEY_API_KEY: new_api_key.get(KEY_API_KEY),
                                KEY_API_KEY_STATUS: new_api_key.get(KEY_API_KEY_STATUS),
                                KEY_PROJECT_ID: new_api_key.get(KEY_PROJECT_ID),
                                KEY_FUNCTION_ID: new_api_key.get(KEY_FUNCTION_ID),
                            }
                            return Result.success(
                                message='Add function to project success!',
                                data=result
                            )

                        else:
                            return Result.failed(
                                message='There was an error in adding function to project'
                            )
                    else:
                        return Result.failed(
                            message='Function already existed in this project'
                        )
                else:
                    return Result.failed(
                        message='Function doesnt exist'
                    )
            else:
                return Result.failed(
                    message='Project doesnt exist'
                )
        else:
            return Result.failed(
                message='Missing data in the request!'
            )

    @classmethod
    def get_function_project(cls, request):
        project_id = request.GET['project_id']
        if project_id:
            result_function = list(ApiKey.objects.filter(
                project_id=Project.objects.get(project_id=project_id),
                status=DEFAULT_STATUS_ACTIVE
            ).values())
            function_list = []
            for item in result_function:
                function_item = list(Function.objects.filter(function_id=item.get('function_id_id')).values())[0]
                function_item['api_key'] = item.get(KEY_API_KEY)
                function_list.append(function_item)
            if result_function:
                return Result.success(
                    message='Get function success',
                    data=function_list
                )
            else:
                return Result.failed(
                    message='Function doesnt exist in project'
                )
        else:
            return Result.failed(
                message='Missing data in the request!'
            )
