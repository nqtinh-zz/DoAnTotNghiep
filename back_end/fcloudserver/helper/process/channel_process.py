#  @Project FCloudConsole
#  @Homepage https://fsmartstore.com
#  @Copyright (c) 2018 Fujinet Systems JSC. All Rights Reserved.
#  @License All resources of the source code are owned by 'Fujinet Systems JSC'.
#  Intentionally infringing, stealing, exchanging, or trading in all of the
#  resources below without our consent, is a violation of intellectual property
#  rights. So, if you accidentally receive this source code, please send an email
#  to rd-support@fujinet.net, so we can find the best solution for this problem.
import json
import datetime
from hashlib import blake2b
from utils.result import Result
import httplib2
from urllib.parse import urlencode
from fcloudserver.helper.process.default_config import DefaultConfig
from utils.constants import *
from db_accessor.models import User, UserToken, Project, Profile, Process,Camera


class ChannelProcess:

    @classmethod
    def parse_create_process(cls, request):
        """
        Parse creation user information from request
        :param request: the data that the user submitted the request
        :return: a dict containing username, password, password_confirm, fullname
        information if it exists, otherwise None
        """

        if (KEY_PROCESS_NAME in request.data and KEY_PROCESS_PEOPLE_GROUP_ID in request.data and
                KEY_PROCESS_CONFIG in request.data and KEY_PROCESS_CAMERA_ID in request.data
                and KEY_PROCESS_PROJECT_ID in request.data):
            return {
                KEY_PROCESS_NAME: request.data[KEY_PROCESS_NAME],
                KEY_PROCESS_PEOPLE_GROUP_ID: request.data[KEY_PROCESS_PEOPLE_GROUP_ID],
                KEY_PROCESS_CONFIG: request.data[KEY_PROCESS_CONFIG],
                KEY_PROCESS_CAMERA_ID: request.data[KEY_PROCESS_CAMERA_ID],
                KEY_PROCESS_PROJECT_ID: request.data[KEY_PROCESS_PROJECT_ID]
            }
        else:
            return None

    @classmethod
    def parse_update_process(cls, request):
        """
        Parse creation user information from request
        :param request: the data that the user submitted the request
        :return: a dict containing username, password, password_confirm, fullname
        information if it exists, otherwise None
        """

        if (KEY_PROCESS_ID in request.data and KEY_PROCESS_NAME in request.data and KEY_PROCESS_PEOPLE_GROUP_ID in request.data and
                KEY_PROCESS_CONFIG in request.data and KEY_PROCESS_CAMERA_ID in request.data
                and KEY_PROCESS_PROJECT_ID in request.data ):
            return {
                KEY_PROCESS_ID: request.data[KEY_PROCESS_ID],
                KEY_PROCESS_NAME: request.data[KEY_PROCESS_NAME],
                KEY_PROCESS_PEOPLE_GROUP_ID: request.data[KEY_PROCESS_PEOPLE_GROUP_ID],
                KEY_PROCESS_CONFIG: request.data[KEY_PROCESS_CONFIG],
                KEY_PROCESS_CAMERA_ID: request.data[KEY_PROCESS_CAMERA_ID],
                KEY_PROCESS_PROJECT_ID: request.data[KEY_PROCESS_PROJECT_ID],
            }
        else:
            return None

    @classmethod
    def get_default_config(cls, request):
        data = DefaultConfig.data
        return Result.success(
            message="Success get default config",
            data=data
        )

    @classmethod
    def create_process_token(cls, process_id, current_time_ms):
        return blake2b(key=(
            '{}{}'.format(
                str(process_id).zfill(ID_LENGTH),
                str(current_time_ms).zfill(ID_LENGTH)
            ).encode('utf-8')), digest_size=5
        ).hexdigest()

    @classmethod
    def create_process(cls, request):
        process = cls.parse_create_process(request)
        if process:
            result_check_processname = Process.objects.filter(process_name=process[KEY_PROCESS_NAME]).values()
            if not result_check_processname.exists():
                result_create_process = Process.objects.create(
                    process_name=process[KEY_PROCESS_NAME],
                    process_config=process[KEY_PROCESS_CONFIG],
                    people_group_id=process[KEY_PROCESS_PEOPLE_GROUP_ID],
                    camera_id=Camera.objects.get(camera_id=process[KEY_PROCESS_CAMERA_ID]),
                    project_id=Project.objects.get(project_id=process[KEY_PROCESS_PROJECT_ID]),
                    process_status=DEFAULT_PROCESS_CREATE
                )
                if result_create_process:
                    get_process_id = list(Process.objects.filter(process_name=process[KEY_PROCESS_NAME]).values())[0].get('process_id')
                    tmp_process_token = cls.create_process_token(get_process_id, datetime.datetime.now())
                    result = Process.objects.get(
                        process_name=process[KEY_PROCESS_NAME])
                    result.process_token = tmp_process_token
                    result.save()
                    return Result.success(
                        message="Success create process",
                    )
                else:
                    return Result.failed(
                        message='Can not create process',
                    )
            else:
                return Result.failed(
                    message='Process name exits',
                )
        else:
            return Result.failed(
                message='Data empty',
            )

    @classmethod
    def get_process_list(cls, request):
        project_id = request.GET['project_id']
        if project_id:
            try:
                all_process = Process.objects.filter(
                    project_id=Project.objects.get(project_id=project_id),
                )
            except Project.DoesNotExist:
                return Result.failed(
                    message='Project doesnt exist'
                )
            result = []
            list_all_process = list(all_process.values())
            print()
            for process in list_all_process:
                #print(json.loads(json.dumps(process.get('process_config'))))
                result.append(process)
            return Result.success(
                message="Get all process successful",
                data=result
            )
        else:
            return Result.failed(
                message="Project id not exists",
            )

    @classmethod
    def start_process(cls, request):
        process_id = request.GET['process_id']
        if process_id:
            process_update = Process.objects.get(
                process_id=process_id,
            )
            process_update.process_status = KEY_PROCESS_START
            process_update.save()
            result = list(Process.objects.filter(process_id=process_id,).values())[0]
            return Result.success(
                message='Success start process!',
                data = result
            )
        else:
            return Result.failed(
                message='Missing data in the request!'
            )

    @classmethod
    def stop_process(cls, request):
        process_id = request.GET['process_id']
        if process_id:
            process_update = Process.objects.get(
                process_id=process_id,
            )
            process_update.process_status = KEY_PROCESS_STOP
            process_update.save()
            result = list(Process.objects.filter(process_id=process_id, ).values())[0]
            return Result.success(
                message='Success stop process!',
                data=result
            )
        else:
            return Result.failed(
                message='Missing data in the request!'
            )

    @classmethod
    def get_process(cls, request):
        process_id = request.GET['process_id']
        if process_id:
            try:
                process = Process.objects.filter(
                    process_id=process_id,
                )
            except Process.DoesNotExist:
                return Result.failed(
                    message='Process doesnt exist'
                )
            get_process = list(process.values())[0]
            print(get_process.get('camera_id_id'))
            return Result.success(
                message="Get process successful",
                data=get_process
            )
        else:
            return Result.failed(
                message="Process id not exists",
            )

    @classmethod
    def update_process(cls, request):
        process = cls.parse_update_process(request)
        print(process)
        if process:
            Process.objects.filter(process_id=process[KEY_PROCESS_ID]).update(
                process_name=process[KEY_PROCESS_NAME],
                process_config=process[KEY_PROCESS_CONFIG],
                people_group_id = process[KEY_PROCESS_PEOPLE_GROUP_ID],
                camera_id=Camera.objects.get(camera_id=process[KEY_PROCESS_CAMERA_ID])
            )


            print('test')
            return Result.success(
                message='Success edit process!'
            )
        else:
            return Result.failed(
                message='Missing data in the request!'
            )

    @classmethod
    def delete_process(cls, request):
        process_id = request.GET['process_id']
        if process_id:
            try:
                check_process = Process.objects.select_related('process_id') \
                    .filter(process_id=request.GET['process_id'])
                check_process.delete()
                return Result.success(
                    message='Success delete process'
                )
            except Camera.DoesNotExist:
                return Result.failed(
                    message='There is no process with this ID!'
                )
        else:
            return Result.failed(
                message='Missing data in the request!'
            )
