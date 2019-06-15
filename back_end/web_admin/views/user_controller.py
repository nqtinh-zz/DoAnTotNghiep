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

from utils.response import Resp
from web_admin.helper.auth import Authen


@api_view(['POST'])
def signup(request):
    """
    Register a new administrator account
    :param request: contains information and data that the user sends
    :return: returns the token and user id if the new user was created
    successfully, otherwise return the error message.
    """

    result_create_user = Authen.create(request)

    if result_create_user.is_success():
        return JsonResponse(
            Resp.success(
                message=result_create_user.get_message(),
                data=result_create_user.get_data()).to_dict(),
            safe=False)
    else:
        return JsonResponse(
            Resp.error(message=result_create_user.get_message()).to_dict(),
            safe=False)


@api_view(['POST'])
def login(request):
    """
    Login with user account
    :param request: contains information and data that the user sends
    :return: returns the token and user id if user login successfully,
    otherwise the error message.
    """

    result_login_user = Authen.login(request)

    if result_login_user.is_success():
        return JsonResponse(
            Resp.success(
                message=result_login_user.get_message(),
                data=result_login_user.get_data()).to_dict(),
            safe=False)
    else:
        return JsonResponse(
            Resp.error(
                message=result_login_user.get_message()).to_dict(),
            safe=False)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_avatar(request):
    result_logout_user = Authen.get_avatar(request)

    if result_logout_user.is_success():
        return JsonResponse(
            Resp.success(
                message=result_logout_user.get_message(),
                data=result_logout_user.get_data()).to_dict(),
            safe=False, )
    else:
        return JsonResponse(
            Resp.error(message=result_logout_user.get_message()).to_dict(),
            safe=False, )


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def change_password(request):
    result_logout_user = Authen.change_password(request)

    if result_logout_user.is_success():
        return JsonResponse(
            Resp.success(
                message=result_logout_user.get_message(),
                data=result_logout_user.get_data()).to_dict(),
            safe=False, )
    else:
        return JsonResponse(
            Resp.error(message=result_logout_user.get_message()).to_dict(),
            safe=False, )


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def logout(request):
    """
    Log out of user accounts
    :param request: contains information and data that the user sends
    :return: the message is successful if the user has logged out of
    the system, otherwise the error message.
    """

    result_logout_user = Authen.logout(request)

    if result_logout_user.is_success():
        return JsonResponse(
            Resp.success(
                message=result_logout_user.get_message(),
                data=result_logout_user.get_data()).to_dict(),
            safe=False, )
    else:
        return JsonResponse(
            Resp.error(message=result_logout_user.get_message()).to_dict(),
            safe=False, )


@api_view(['GET', 'PUT'])
@permission_classes((IsAuthenticated,))
def profile_controller(request):
    if request.method == 'GET':
        result = Authen.get_profile(request)
    if request.method == 'PUT':
        result = Authen.set_profile(request)
    if result.is_success():
        return JsonResponse(
            Resp.success(
                message=result.get_message(),
                data=result.get_data()).to_dict(),
            safe=False, )
    else:
        return JsonResponse(
            Resp.error(message=result.get_message()).to_dict(),
            safe=False, )

