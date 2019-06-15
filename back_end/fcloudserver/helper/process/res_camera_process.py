#  @Project FCloudConsole
#  @Homepage https://fsmartstore.com
#  @Copyright (c) 2018 Fujinet Systems JSC. All Rights Reserved.
#  @License All resources of the source code are owned by 'Fujinet Systems JSC'.
#  Intentionally infringing, stealing, exchanging, or trading in all of the
#  resources below without our consent, is a violation of intellectual property
#  rights. So, if you accidentally receive this source code, please send an email
#  to rd-support@fujinet.net, so we can find the best solution for this problem.
import os
import time

from django.views.decorators import gzip

import cv2
from datetime import datetime
from django.db.models import Q
from django.http import StreamingHttpResponse, Http404

from config import django_settings
# from config.log_config import log
from db_accessor.models import Project, Camera, CameraGroup, XrefCameraGroup
from utils.constants import *
from utils.result import Result


class ResCameraProcess:

    @classmethod
    def parse_add_camera_data(cls, request):
        """
            Parse add camera data from request
            :param request: the data that the user submitted the request
            :return: a dict containing camera name, project id, stream url
            information if it exists, otherwise None
        """

        if KEY_CAMERA_NAME in request.data and KEY_PROJECT_ID in request.data and KEY_STREAM_URL in request.data:
            return {
                KEY_CAMERA_NAME: request.data[KEY_CAMERA_NAME],
                KEY_PROJECT_ID: request.data[KEY_PROJECT_ID],
                KEY_STREAM_URL: request.data[KEY_STREAM_URL]
            }
        else:
            return None

    @classmethod
    def add_camera(cls, request):
        result_camera = cls.parse_add_camera_data(request)
        if result_camera:
            check_camera = Camera.objects.filter(
                camera_name=result_camera[KEY_CAMERA_NAME],
                project_id=Project.objects.get(
                    project_id=result_camera[KEY_PROJECT_ID]),
            ).values()
            if not check_camera:
                result_create_camera = Camera.objects.create(
                    camera_name=result_camera[KEY_CAMERA_NAME],
                    stream_url=result_camera[KEY_STREAM_URL],
                    project_id=Project.objects.get(project_id=result_camera[KEY_PROJECT_ID]),
                    status=DEFAULT_STATUS_ACTIVE,
                )
                if result_create_camera:
                    camera_just_created = list(Camera.objects.filter(
                        camera_name=result_camera[KEY_CAMERA_NAME],
                        status=DEFAULT_STATUS_ACTIVE,
                    ).values())[0]
                    group_array = request.data['group']
                    if len(group_array) != 0:
                        for group in group_array:
                            result_create_group_camera = XrefCameraGroup.objects.create(
                                camera_id=Camera.objects.get(
                                    camera_id=camera_just_created.get(KEY_CAMERA_ID),
                                    status=DEFAULT_STATUS_ACTIVE,
                                ),
                                camera_group_id=CameraGroup.objects.get(
                                    camera_group_name=group,
                                    status=DEFAULT_STATUS_ACTIVE,
                                )
                            )
                            if not result_create_group_camera:
                                return Result.failed(
                                    message='Have some problem when create group!'
                                )
                    return Result.success(
                        message='Success add camera!'
                    )

                else:
                    return Result.failed(
                        message='Have some problem when add camera!'
                    )
            else:
                return Result.failed(
                    message='Camera name already existed!'
                )
        else:
            return Result.failed(
                message='Missing data in the request!'
            )

    @classmethod
    def get_all_camera(cls, request):
        project_id = request.GET['project_id']
        if project_id:
            try:
                all_camera = Camera.objects.filter(
                    project_id=Project.objects.get(project_id=project_id),
                    status=DEFAULT_STATUS_ACTIVE
                )
            except Project.DoesNotExist:
                return Result.failed(
                    message='Project doesnt exist'
                )
            result = []
            list_all_camera = list(all_camera.values())
            for camera in list_all_camera:

                try:
                    check_camera = Camera.objects.get(
                        camera_id=camera.get('camera_id'),
                        status=DEFAULT_STATUS_ACTIVE,
                    )
                    group_list = []
                    xref_camera_group = list(XrefCameraGroup.objects.select_related('camera_id')
                                             .filter(camera_id=check_camera.camera_id).values())
                    for item in xref_camera_group:
                        group_item = \
                            list(CameraGroup.objects.select_related('camera_group_id')
                                 .filter(camera_group_id=item.get('camera_group_id_id'),
                                         project_id=Project.objects.get(project_id=project_id)).values())
                        if len(group_item) > 0:
                            group_list.append(group_item[0])

                    camera['group'] = group_list
                    result.append(camera)

                except Camera.DoesNotExist:
                    return Result.failed(
                        message='Camera id  not exist!'
                    )
            return Result.success(
                message='Get all camera success',
                data=result
            )

        else:
            return Result.failed(
                message='Missing data in the request!'
            )

    @classmethod
    def parse_delete_camera_data(cls, request):
        """
            Parse delete camera data from request
            :param request: the data that the user submitted the request
            :return: a dict containing camera id, project id
            information if it exists, otherwise None
        """

        if KEY_CAMERA_ID in request.data and KEY_PROJECT_ID in request.data:
            return {
                KEY_CAMERA_ID: request.data[KEY_CAMERA_ID],
                KEY_PROJECT_ID: request.data[KEY_PROJECT_ID],
            }
        else:
            return None

    @classmethod
    def delete_camera(cls, request):
        result_delete_camera = cls.parse_delete_camera_data(request)
        if result_delete_camera:
            try:
                check_camera = Camera.objects.get(
                    camera_id=result_delete_camera.get(KEY_CAMERA_ID),
                    project_id=result_delete_camera.get(KEY_PROJECT_ID))
                xref_people_group = XrefCameraGroup.objects.select_related('camera_id') \
                    .filter(camera_id=result_delete_camera[KEY_CAMERA_ID])
                xref_people_group.delete()
                check_camera.status = DEFAULT_STATUS_DEACTIVE
                check_camera.save()
                return Result.success(
                    message='Success delete camera'
                )
            except Camera.DoesNotExist:
                return Result.failed(
                    message='There is no camera with this ID!'
                )
        else:
            return Result.failed(
                message='Missing data in the request!'
            )

    @classmethod
    def parse_update_camera_data(cls, request):
        """
            Parse update camera data from request
            :param request: the data that the user submitted the request
            :return: a dict containing camera id, project id, camera name, stream url
            information if it exists, otherwise None
        """

        if KEY_CAMERA_ID in request.data \
                and KEY_PROJECT_ID in request.data \
                and KEY_CAMERA_NAME in request.data \
                and KEY_STREAM_URL in request.data:
            return {
                KEY_CAMERA_ID: request.data[KEY_CAMERA_ID],
                KEY_PROJECT_ID: request.data[KEY_PROJECT_ID],
                KEY_CAMERA_NAME: request.data[KEY_CAMERA_NAME],
                KEY_STREAM_URL: request.data[KEY_STREAM_URL]
            }
        else:
            return None

    @classmethod
    def update_camera(cls, request):
        result_camera = cls.parse_update_camera_data(request)
        print(result_camera)
        if result_camera:
            check_camera_name = Camera.objects.filter(
                ~Q(camera_id=result_camera[KEY_CAMERA_ID]),
                camera_name=result_camera[KEY_CAMERA_NAME],
                project_id=Project.objects.get(
                    project_id=result_camera[KEY_PROJECT_ID]),
                status=DEFAULT_STATUS_ACTIVE,
            )
            check_camera_url = Camera.objects.filter(
                ~Q(camera_id=result_camera[KEY_CAMERA_ID]),
                stream_url=result_camera[KEY_STREAM_URL],
                project_id=Project.objects.get(
                    project_id=result_camera[KEY_PROJECT_ID]),
                status=DEFAULT_STATUS_ACTIVE,
            )
            if not (check_camera_name or check_camera_url):
                camera_update = Camera.objects.get(
                    camera_id=result_camera[KEY_CAMERA_ID],
                    status=DEFAULT_STATUS_ACTIVE,
                )
                camera_update.camera_name = result_camera[KEY_CAMERA_NAME]
                camera_update.stream_url = result_camera[KEY_STREAM_URL]
                camera_update.updated_at = datetime.now()
                camera_update.save()
                return Result.success(
                    message='Success edit camera!'
                )
            else:
                return Result.failed(
                    message='Name or url exist'
                )
        else:
            return Result.failed(
                message='Missing data in the request!'
            )

    @classmethod
    def parse_add_camera_group_data(cls, request):
        """
            Parse add camera group data from request
            :param request: the data that the user submitted the request
            :return: a dict containing project id, camera group color, camera group name
            information if it exists, otherwise None
        """

        if KEY_PROJECT_ID in request.data and KEY_CAMERA_GROUP_COLOR in request.data \
                and KEY_CAMERA_GROUP_NAME in request.data:

            return {
                KEY_PROJECT_ID: request.data[KEY_PROJECT_ID],
                KEY_CAMERA_GROUP_COLOR: request.data[KEY_CAMERA_GROUP_COLOR],
                KEY_CAMERA_GROUP_NAME: request.data[KEY_CAMERA_GROUP_NAME],
            }
        else:
            return None

    @classmethod
    def add_camera_group(cls, request):
        result_group_data = cls.parse_add_camera_group_data(request)

        if result_group_data:
            check_group_exist = CameraGroup.objects.filter(
                project_id=result_group_data[KEY_PROJECT_ID],
                camera_group_name=result_group_data[KEY_CAMERA_GROUP_NAME],
                status=DEFAULT_STATUS_ACTIVE,
            )
            if not check_group_exist:
                check_color_exist = CameraGroup.objects.filter(
                    camera_group_color=result_group_data[KEY_CAMERA_GROUP_COLOR],
                    status=DEFAULT_STATUS_ACTIVE,
                )
                if not check_color_exist:
                    try:
                        result_group = CameraGroup.objects.create(
                            project_id=Project.objects.get(project_id=result_group_data[KEY_PROJECT_ID]),
                            camera_group_name=result_group_data[KEY_CAMERA_GROUP_NAME],
                            camera_group_color=result_group_data[KEY_CAMERA_GROUP_COLOR],
                            status=DEFAULT_STATUS_ACTIVE,
                        )
                    except Project.DoesNotExist:
                        return Result.failed(
                            message='Project doesnt exist'
                        )
                    if result_group:
                        new_group_id = CameraGroup.objects.get(
                            camera_group_name=result_group_data[KEY_CAMERA_GROUP_NAME],
                            status=DEFAULT_STATUS_ACTIVE
                        ).camera_group_id
                        new_group = CameraGroup.objects.filter(
                            camera_group_id=new_group_id)
                        new_group_data = list(new_group.values())[0]
                        return Result.success(
                            message='New camera group has been created',
                            data=new_group_data
                        )
                    else:
                        return Result.failed(
                            message='Have some problem when create new camera group'
                        )
                else:
                    return Result.failed(
                        message='This group color already existed in this project'
                    )
            else:
                return Result.failed(
                    message='This group code already existed in this project'
                )
        else:
            return Result.failed(
                message='Missing data in the request!'
            )

    @classmethod
    def delete_camera_group(cls, request):
        try:
            camera_group_id = request.GET['camera_group_id']
            delete_group = CameraGroup.objects.get(camera_group_id=camera_group_id)
            if delete_group:
                try:
                    xref_camera_group = XrefCameraGroup.objects.select_related('camera_group_id') \
                        .filter(camera_group_id=camera_group_id)
                    delete_group.status = DEFAULT_STATUS_DEACTIVE
                    delete_group.save()
                    xref_camera_group.delete()
                    return Result.success(
                        message='Delete group success!',
                    )
                except CameraGroup.DoesNotExist:
                    return Result.failed(
                        message='CameraGroup matching query does not exist'
                    )

            else:
                return Result.failed(
                    message='Group doesnt exist'
                )
        except CameraGroup.DoesNotExist:
            return Result.failed(
                message='CameraGroup matching query does not exist!'
            )
        except Exception as exc:
            return Result.failed(
                message=f'Missing data from request: {exc}'
            )

    @classmethod
    def parse_update_camera_group_data(cls, request):
        """
            Parse update camera group data from request
            :param request: the data that the user submitted the request
            :return: a dict containing camera group id, camera group color, camera group name
            information if it exists, otherwise None
        """

        if KEY_CAMERA_GROUP_ID in request.data \
                and KEY_CAMERA_GROUP_COLOR in request.data \
                and KEY_CAMERA_GROUP_NAME in request.data:

            return {
                KEY_CAMERA_GROUP_ID: request.data[KEY_CAMERA_GROUP_ID],
                KEY_CAMERA_GROUP_COLOR: request.data[KEY_CAMERA_GROUP_COLOR],
                KEY_CAMERA_GROUP_NAME: request.data[KEY_CAMERA_GROUP_NAME],
            }
        else:
            return None

    @classmethod
    def update_camera_group(cls, request):
        result_group_data = cls.parse_update_camera_group_data(request)

        if result_group_data:
            camera_group_choose = CameraGroup.objects.filter(
                camera_group_id=result_group_data[KEY_CAMERA_GROUP_ID]
            ).values()
            if camera_group_choose:

                check_group_name = CameraGroup.objects.filter(
                    ~Q(camera_group_id=result_group_data[KEY_CAMERA_GROUP_ID]),
                    camera_group_name=result_group_data[KEY_CAMERA_GROUP_NAME],
                    status=DEFAULT_STATUS_ACTIVE,
                )
                check_group_color = CameraGroup.objects.filter(
                    ~Q(camera_group_id=result_group_data[KEY_CAMERA_GROUP_ID]),
                    camera_group_color=result_group_data[KEY_CAMERA_GROUP_COLOR],
                    status=DEFAULT_STATUS_ACTIVE,
                )

                if check_group_name:
                    return Result.failed(
                        message='This group name exists'
                    )
                elif check_group_color:
                    return Result.failed(
                        message='This group color exists'
                    )
                else:
                    camera_group_choose.update(camera_group_name=result_group_data[KEY_CAMERA_GROUP_NAME],
                                               camera_group_color=result_group_data[KEY_CAMERA_GROUP_COLOR],
                                               updated_at=datetime.now())
                    return Result.success(
                        message='Update group success!'
                    )
            else:
                return Result.failed(
                    message='Group doesnt exist'
                )
        else:
            return Result.failed(
                message='Missing data in the request!'
            )

    @classmethod
    def get_camera_group_data(cls, request):
        camera_group_id = request.GET['camera_group_id']
        if camera_group_id:
            try:
                check_group = CameraGroup.objects.get(
                    camera_group_id=camera_group_id,
                    status=DEFAULT_STATUS_ACTIVE
                )
                result = {
                    KEY_CAMERA_GROUP_ID: check_group.camera_group_id,
                    KEY_CAMERA_GROUP_NAME: check_group.camera_group_name,
                    KEY_CAMERA_GROUP_COLOR: check_group.camera_group_color,
                }
                return Result.success(
                    message='Get group success',
                    data=result
                )
            except CameraGroup.DoesNotExist:
                return Result.failed(
                    message='Group doesnt exist!'
                )
        else:
            return Result.failed(
                message='Missing data in the request!'
            )

    @classmethod
    def get_all_camera_group(cls, request):
        project_id = request.GET['project_id']
        if project_id:
            try:
                all_camera_group = CameraGroup.objects.filter(
                    project_id=Project.objects.get(project_id=project_id),
                    status=DEFAULT_STATUS_ACTIVE,
                )
            except Project.DoesNotExist:
                return Result.failed(
                    message='Project doesnt exist'
                )
            list_all_camera_group = list(all_camera_group.values())
            return Result.success(
                message='Get all group success',
                data=list_all_camera_group
            )

        else:
            return Result.failed(
                message='Missing data in the request!'
            )

    @classmethod
    def parse_add_camera_to_group(cls, request):
        """
            Parse add camera to group data from request
            :param request: the data that the user submitted the request
            :return: a dict containing group array, camera id, project id
            information if it exists, otherwise None
        """

        if KEY_GROUP_ARRAY in request.data and KEY_CAMERA_ID in request.data and KEY_PROJECT_ID in request.data:

            return {
                KEY_GROUP_ARRAY: request.data[KEY_GROUP_ARRAY],
                KEY_CAMERA_ID: request.data[KEY_CAMERA_ID],
                KEY_PROJECT_ID: request.data[KEY_PROJECT_ID],
            }
        else:
            return None

    @classmethod
    def add_camera_to_group(cls, request):
        request_data = cls.parse_add_camera_to_group(request)
        if request_data:
            try:
                check_camera = Camera.objects.get(
                    camera_id=request_data.get(KEY_CAMERA_ID),
                    project_id=Project.objects.get(project_id=request_data.get(KEY_PROJECT_ID)),
                    status=DEFAULT_STATUS_ACTIVE
                )
                group_arr = request.data.get(KEY_GROUP_ARRAY)

                for group in group_arr:
                    check_group = CameraGroup.objects.get(
                        camera_group_name=group,
                        project_id=Project.objects.get(project_id=request_data.get(KEY_PROJECT_ID)),
                        status=DEFAULT_STATUS_ACTIVE
                    )
                    check_camera_xref = XrefCameraGroup.objects.filter(
                        camera_id=check_camera,
                        camera_group_id=check_group
                    )
                    if not check_camera_xref:
                        result = XrefCameraGroup.objects.create(
                            camera_id=check_camera,
                            camera_group_id=check_group,
                        )
                        if not result:
                            return Result.failed(
                                message='Have some problem when add camera to group!'
                            )
                    else:
                        return Result.failed(
                            message='This camera already in this group!'
                        )
                return Result.success(
                    message='Add camera to group success!'
                )
            except (Camera.DoesNotExist, CameraGroup.DoesNotExist):
                return Result.failed(
                    message='Camera id or group id not exist!'
                )
        else:
            return Result.failed(
                message='Missing data in the request!'
            )

    @classmethod
    def parse_delete_camera_from_group_data(cls, request):
        """
            Parse delete camera from group data from request
            :param request: the data that the user submitted the request
            :return: a dict containing camera id, camera group id, project id
            information if it exists, otherwise None
        """

        if KEY_CAMERA_ID in request.data and KEY_CAMERA_GROUP_ID in request.data and KEY_PROJECT_ID in request.data:

            return {
                KEY_PROJECT_ID: request.data[KEY_PROJECT_ID],
                KEY_CAMERA_ID: request.data[KEY_CAMERA_ID],
                KEY_CAMERA_GROUP_ID: request.data[KEY_CAMERA_GROUP_ID],
            }
        else:
            return None

    @classmethod
    def delete_camera_from_group(cls, request):
        request_data = cls.parse_delete_camera_from_group_data(request)

        if request_data:
            try:
                check_camera = Camera.objects.get(
                    camera_id=request_data.get(KEY_CAMERA_ID),
                    project_id=Project.objects.get(
                        project_id=request_data.get(KEY_PROJECT_ID)),
                    status=DEFAULT_STATUS_ACTIVE
                )
                check_group = CameraGroup.objects.get(
                    camera_group_id=request_data.get(KEY_CAMERA_GROUP_ID),
                    status=DEFAULT_STATUS_ACTIVE
                )
                result = XrefCameraGroup.objects.filter(
                    camera_id=check_camera,
                    camera_group_id=check_group,
                )
                if result:
                    result.delete()
                    return Result.success(
                        message='Delete camera from group success!'
                    )
                else:
                    return Result.failed(
                        message='Have some problem when delete camera to group!'
                    )
            except (Camera.DoesNotExist, CameraGroup.DoesNotExist, Project.DoesNotExist):
                return Result.failed(
                    message='Camera id or group id not exist!'
                )
        else:
            return Result.failed(
                message='Missing data in the request!'
            )

    @classmethod
    def check_all_url(cls, request):
        project_id = request.GET['project_id']
        if project_id:
            try:
                all_camera = list(Camera.objects.filter(
                    status=DEFAULT_STATUS_ACTIVE,
                    project_id=Project.objects.get(project_id=project_id)
                ).values())
            except Project.DoesNotExist:
                return Result.failed(
                    message='Project doesnt exist!!'
                )
            list_status = []
            for camera in all_camera:
                item = {
                    KEY_CAMERA_ID: camera.get(KEY_CAMERA_ID),
                    'status': cls.check_camera_available(camera.get('stream_url'))
                }
                list_status.append(item)
            return Result.success(
                message='Status of all cameras',
                data=list_status
            )
        else:
            return Result.failed(
                message='Missing data from request!!'
            )

    @classmethod
    def camera_group_list_camera(cls, request):
        group_id = request.GET['group_id']
        print(group_id)

        if group_id:
            xref_camera_group = list(XrefCameraGroup.objects.select_related('camera_id')
                                         .filter(camera_group_id=group_id).values())

            print(xref_camera_group)
            result = []
            for item in xref_camera_group:
                camera = list(Camera.objects.filter(
                    camera_id=item.get('camera_id_id'),
                    status=DEFAULT_STATUS_ACTIVE).values())[0]
                print(camera)
                group_list = []
                xref_camera_group_tmp = list(XrefCameraGroup.objects.select_related('camera_id')
                                         .filter(camera_id=item.get('camera_id_id')).values())
                for tmp in xref_camera_group_tmp:
                    group_item = \
                        list(CameraGroup.objects.select_related('camera_group_id')
                             .filter(camera_group_id=tmp.get('camera_group_id_id'),
                                     ).values())
                    if len(group_item) > 0:
                        group_list.append(group_item[0])
                temp = camera
                temp['group'] = group_list
                result.append(temp)
            print('tinh')
            print(result)
            return Result.success(
                    message='Status of all cameras',
                    data=result
                )
        else:
            return Result.failed(
                message='Missing data from request!!'
            )

    @staticmethod
    def check_camera_available(stream_url):
        video = cv2.VideoCapture(stream_url)
        # noinspection PyBroadException
        try:
            if not video.isOpened():
                return False

            grabbed, _ = video.read()
            if not grabbed:
                return False

            return True

        except Exception:
            return False

        finally:
            video.release()

    @classmethod
    def check_camera(cls, request):
        camera_id = request.GET['camera_id']
        if camera_id:
            camera_url = Camera.objects.get(camera_id=camera_id).stream_url
            camera_status = cls.check_camera_available(camera_url)
            return Result.success(
                message='Status of all cameras',
                data=camera_status
            )

        else:
            return Result.failed(
                message='Missing data from request!!'
            )
