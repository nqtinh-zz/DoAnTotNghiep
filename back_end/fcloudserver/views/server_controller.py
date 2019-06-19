#  @Project FCloudConsole
#  @Homepage https://fsmartstore.com
#  @Copyright (c) 2018 Fujinet Systems JSC. All Rights Reserved.
#  @License All resources of the source code are owned by 'Fujinet Systems JSC'.
#  Intentionally infringing, stealing, exchanging, or trading in all of the
#  resources below without our consent, is a violation of intellectual property
#  rights. So, if you accidentally receive this source code, please send an email
#  to rd-support@fujinet.net, so we can find the best solution for this problem.

from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from fcloudserver.helper.process import VideoCamera
from fcloudserver.helper.process.channel_process import ChannelProcess
from fcloudserver.helper.process.project_process import ProjectProcess
from fcloudserver.helper.process.res_camera_process import ResCameraProcess
from fcloudserver.helper.process.res_people_process import ResPeopleProcess
from utils.response import Resp


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes((IsAuthenticated,))
def project_controller(request):
    """
    Project all feature :
        GET: Get all project of user
        POST: Create new project , Choose project
        DELETE: Delete project with param project_code
    :param request: contains data of project
    :return: the message is successful if done feature, otherwise the error message.
    """
    if request.method == 'POST':
        result = ProjectProcess.create_project(request)
    if request.method == 'GET':
        if 'project_code' in request.GET:
            result = ProjectProcess.choose_project(request)
        else:
            result = ProjectProcess.get_all_project(request)
    if request.method == 'DELETE':
        result = ProjectProcess.delete_project(request)
    if result.is_success():
        return JsonResponse(Resp.success(
            message=result.get_message(),
            data=result.get_data()).to_dict(), safe=False)
    else:
        return JsonResponse(Resp.error(message=result.get_message()).to_dict(),
                            safe=False)


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
def function_controller(request):
    """
        Function Controller
            POST: add new function with data: project_id, function_id
        :param request: contains data of function
        :return: the message is successful if success, otherwise the error message.
    """
    if request.method == 'POST':
        result = ProjectProcess.add_function(request)
    if request.method == 'GET':
        result = ProjectProcess.get_function_project(request)
    if result.is_success():
        return JsonResponse(Resp.success(
            message=result.get_message(),
            data=result.get_data()).to_dict(), safe=False)
    else:
        return JsonResponse(Resp.error(message=result.get_message()).to_dict(),
                            safe=False)


@api_view(['GET', 'POST', 'DELETE', 'PUT'])
@permission_classes((IsAuthenticated,))
def people_group_controller(request):
    if request.method == 'POST':
        result = ResPeopleProcess.add_people_group(request)
    if request.method == 'DELETE':
        result = ResPeopleProcess.delete_people_group(request)
    if request.method == 'PUT':
        result = ResPeopleProcess.update_people_group(request)
    if request.method == 'GET':
        if 'people_group_id' in request.GET:
            result = ResPeopleProcess.get_people_group_data(request)
        else:
            result = ResPeopleProcess.get_all_people_group(request)
    if result.is_success():
        return JsonResponse(Resp.success(
            message=result.get_message(),
            data=result.get_data()).to_dict(), safe=False)
    else:
        return JsonResponse(Resp.error(message=result.get_message()).to_dict(),
                            safe=False)


@api_view(['POST', 'GET', 'DELETE', 'PUT'])
@permission_classes((IsAuthenticated,))
def person_controller(request):
    if request.method == 'POST':
        result = ResPeopleProcess.add_person(request)
    if request.method == 'GET':
        result = ResPeopleProcess.get_all_person(request)
    if request.method == 'DELETE':
        result = ResPeopleProcess.delete_person(request)
    if request.method == 'PUT':
        result = ResPeopleProcess.update_person(request)
    if result.is_success():
        return JsonResponse(Resp.success(
            message=result.get_message(),
            data=result.get_data()).to_dict(), safe=False)
    else:
        return JsonResponse(Resp.error(message=result.get_message()).to_dict(),
                            safe=False)


@api_view(['POST', 'GET', 'DELETE', 'PUT'])
@permission_classes((IsAuthenticated,))
def camera_controller(request):
    if request.method == 'POST':
        result = ResCameraProcess.add_camera(request)
    if request.method == 'GET':
        result = ResCameraProcess.get_all_camera(request)
    if request.method == 'DELETE':
        result = ResCameraProcess.delete_camera(request)
    if request.method == 'PUT':
        result = ResCameraProcess.update_camera(request)
    if result.is_success():
        return JsonResponse(Resp.success(
            message=result.get_message(),
            data=result.get_data()).to_dict(), safe=False)
    else:
        return JsonResponse(Resp.error(message=result.get_message()).to_dict(),
                            safe=False)


@api_view(['GET', 'POST', 'DELETE', 'PUT'])
@permission_classes((IsAuthenticated,))
def camera_group_controller(request):
    if request.method == 'POST':
        result = ResCameraProcess.add_camera_group(request)
    if request.method == 'DELETE':
        result = ResCameraProcess.delete_camera_group(request)
    if request.method == 'PUT':
        result = ResCameraProcess.update_camera_group(request)
    if request.method == 'GET':
        if 'camera_group_id' in request.GET:
            result = ResCameraProcess.get_camera_group_data(request)
        else:
            result = ResCameraProcess.get_all_camera_group(request)
    if result.is_success():
        return JsonResponse(Resp.success(
            message=result.get_message(),
            data=result.get_data()).to_dict(), safe=False)
    else:
        return JsonResponse(Resp.error(message=result.get_message()).to_dict(),
                            safe=False)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def add_person_to_group(request):
    """
        Add person to group
        :param request:
        :return: the message is successful if the information of project , otherwise the error message.
    """
    result = ResPeopleProcess.add_person_to_group(request)
    if result.is_success():
        return JsonResponse(Resp.success(
            message=result.get_message(),
            data=result.get_data()).to_dict(), safe=False)
    else:
        return JsonResponse(Resp.error(message=result.get_message()).to_dict(),
                            safe=False)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_group_of_person(request):
    """
        Get group of person
        :param request:
        :return: the message is successful if the information of project , otherwise the error message.
    """
    result = ResPeopleProcess.get_group_of_person(request)
    if result.is_success():
        return JsonResponse(Resp.success(
            message=result.get_message(),
            data=result.get_data()).to_dict(), safe=False)
    else:
        return JsonResponse(Resp.error(message=result.get_message()).to_dict(),
                            safe=False)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def delete_person_from_group(request):
    """
        Get group of person
        :param request:
        :return: the message is successful if the information of project , otherwise the error message.
    """
    result = ResPeopleProcess.delete_person_from_group(request)
    if result.is_success():
        return JsonResponse(Resp.success(
            message=result.get_message(),
            data=result.get_data()).to_dict(), safe=False)
    else:
        return JsonResponse(Resp.error(message=result.get_message()).to_dict(),
                            safe=False)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def get_image_person(request):
    """
        Get group of person
        :param request:
        :return: the message is successful if the information of project , otherwise the error message.
    """
    result = ResPeopleProcess.get_image_person(request)
    if result.is_success():
        return JsonResponse(Resp.success(
            message=result.get_message(),
            data=result.get_data()).to_dict(), safe=False)
    else:
        return JsonResponse(Resp.error(message=result.get_message()).to_dict(),
                            safe=False)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def import_person(request):
    """
        import person
        :param request:
        :return: the message is successful if the information of project , otherwise the error message.
    """
    result = ResPeopleProcess.import_person(request)
    if result.is_success():
        return JsonResponse(Resp.success(
            message=result.get_message(),
            data=result.get_data()).to_dict(), safe=False)
    else:
        return JsonResponse(Resp.error(message=result.get_message()).to_dict(),
                            safe=False)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def add_camera_to_group(request):
    """
        Add camera to group
        :param request:
        :return: the message is successful if the information of project , otherwise the error message.
    """
    result = ResCameraProcess.add_camera_to_group(request)
    if result.is_success():
        return JsonResponse(Resp.success(
            message=result.get_message(),
            data=result.get_data()).to_dict(), safe=False)
    else:
        return JsonResponse(Resp.error(message=result.get_message()).to_dict(),
                            safe=False)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def delete_camera_from_group(request):
    """
        delete camera from group
        :param request:
        :return: the message is successful if the information of project , otherwise the error message.
    """
    result = ResCameraProcess.delete_camera_from_group(request)
    if result.is_success():
        return JsonResponse(Resp.success(
            message=result.get_message(),
            data=result.get_data()).to_dict(), safe=False)
    else:
        return JsonResponse(Resp.error(message=result.get_message()).to_dict(),
                            safe=False)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def check_all_camera_url(request):
    """
        check camera url
        :param request:
        :return: the message is successful if the information of project , otherwise the error message.
    """
    result = ResCameraProcess.check_all_url(request)
    if result.is_success():
        return JsonResponse(Resp.success(
            message=result.get_message(),
            data=result.get_data()).to_dict(), safe=False)
    else:
        return JsonResponse(Resp.error(message=result.get_message()).to_dict(),
                            safe=False)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def check_camera_url(request):
    """
        check camera url
        :param request:
        :return: the message is successful if the information of project , otherwise the error message.
    """
    result = ResCameraProcess.check_camera(request)
    if result.is_success():
        return JsonResponse(Resp.success(
            message=result.get_message(),
            data=result.get_data()).to_dict(), safe=False)
    else:
        return JsonResponse(Resp.error(message=result.get_message()).to_dict(),
                            safe=False)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def camera_group_list_camera(request):
    """
        check camera url
        :param request:
        :return: the message is successful if the information of project , otherwise the error message.
    """
    result = ResCameraProcess.camera_group_list_camera(request)
    if result.is_success():
        return JsonResponse(Resp.success(
            message=result.get_message(),
            data=result.get_data()).to_dict(), safe=False)
    else:
        return JsonResponse(Resp.error(message=result.get_message()).to_dict(),
                            safe=False)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def people_group_list_people(request):
    """
        check camera url
        :param request:
        :return: the message is successful if the information of project , otherwise the error message.
    """
    result = ResPeopleProcess.people_group_list_people(request)
    if result.is_success():
        return JsonResponse(Resp.success(
            message=result.get_message(),
            data=result.get_data()).to_dict(), safe=False)
    else:
        return JsonResponse(Resp.error(message=result.get_message()).to_dict(),
                            safe=False)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def create_process(request):
    result = ChannelProcess.create_process(request)
    if result.is_success():
        return JsonResponse(Resp.success(
            message=result.get_message(),
            data=result.get_data()).to_dict(), safe=False)
    else:
        return JsonResponse(Resp.error(message=result.get_message()).to_dict(),
                            safe=False)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_default_config(request):
    result = ChannelProcess.get_default_config(request)
    if result.is_success():
        return JsonResponse(Resp.success(
            message=result.get_message(),
            data=result.get_data()).to_dict(), safe=False)
    else:
        return JsonResponse(Resp.error(message=result.get_message()).to_dict(),
                            safe=False)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_process_list(request):
    result = ChannelProcess.get_process_list(request)
    if result.is_success():
        return JsonResponse(Resp.success(
            message=result.get_message(),
            data=result.get_data()).to_dict(), safe=False)
    else:
        return JsonResponse(Resp.error(message=result.get_message()).to_dict(),
                            safe=False)


@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def delete_process(request):
    result = ChannelProcess.delete_process(request)
    if result.is_success():
        return JsonResponse(Resp.success(
            message=result.get_message(),
            data=result.get_data()).to_dict(), safe=False)
    else:
        return JsonResponse(Resp.error(message=result.get_message()).to_dict(),
                            safe=False)


@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def update_process(request):
    result = ChannelProcess.update_process(request)
    if result.is_success():
        return JsonResponse(Resp.success(
            message=result.get_message(),
            data=result.get_data()).to_dict(), safe=False)
    else:
        return JsonResponse(Resp.error(message=result.get_message()).to_dict(),
                            safe=False)


@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def start_process(request):
    result = ChannelProcess.start_process(request)
    if result.is_success():
        return JsonResponse(Resp.success(
            message=result.get_message(),
            data=result.get_data()).to_dict(), safe=False)
    else:
        return JsonResponse(Resp.error(message=result.get_message()).to_dict(),
                            safe=False)


@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def stop_process(request):
    result = ChannelProcess.stop_process(request)
    if result.is_success():
        return JsonResponse(Resp.success(
            message=result.get_message(),
            data=result.get_data()).to_dict(), safe=False)
    else:
        return JsonResponse(Resp.error(message=result.get_message()).to_dict(),
                            safe=False)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_process(request):
    result = ChannelProcess.get_process(request)
    if result.is_success():
        return JsonResponse(Resp.success(
            message=result.get_message(),
            data=result.get_data()).to_dict(), safe=False)
    else:
        return JsonResponse(Resp.error(message=result.get_message()).to_dict(),
                            safe=False)


@api_view(['GET'])
def video_feed(request):
    result = VideoCamera.livefe(request)
    return result


@api_view(['GET'])
def turn_off_camera(request):
    result = ResCameraProcess.turn_off_camera(request)
    if result.is_success():
        return JsonResponse(Resp.success(
            message=result.get_message(),
            data=result.get_data()).to_dict(), safe=False)
    else:
        return JsonResponse(Resp.error(message=result.get_message()).to_dict(),
                            safe=False)


@api_view(['GET'])
def turn_on_camera(request):
    result = ResCameraProcess.turn_on_camera(request)
    if result.is_success():
        return JsonResponse(Resp.success(
            message=result.get_message(),
            data=result.get_data()).to_dict(), safe=False)
    else:
        return JsonResponse(Resp.error(message=result.get_message()).to_dict(),
                            safe=False)
