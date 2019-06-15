"""
@Project FSmartDoor
@Homepage https://fsmartstore.com
@Copyright (c) 2018 Fujinet Systems JSC. All Rights Reserved.
@License All resources of the source code are owned by 'Fujinet Systems JSC'.
Intentionally infringing, stealing, exchanging, or trading in all of the
resources below without our consent, is a violation of intellectual property
rights. So, if you accidentally receive this source code, please send an email
to rd-support@fujinet.net, so we can find the best solution for this problem.
"""

#  @Project FCloudConsole
#  @Homepage https://fsmartstore.com
#  @Copyright (c) 2018 Fujinet Systems JSC. All Rights Reserved.
#  @License All resources of the source code are owned by 'Fujinet Systems JSC'.
#  Intentionally infringing, stealing, exchanging, or trading in all of the
#  resources below without our consent, is a violation of intellectual property
#  rights. So, if you accidentally receive this source code, please send an email
#  to rd-support@fujinet.net, so we can find the best solution for this problem.

from django.urls import path

from ..views import user_controller

user_patterns = [
    path(
        'signup',
        user_controller.signup,
        name='signup_new_user'
    ),
    path(
        'login',
        user_controller.login,
        name='login_user'
    ),
    path(
        'logout',
        user_controller.logout,
        name='logout_user'
    ),
    path(
        'get-avatar',
        user_controller.get_avatar,
        name='get avatar user'
    ),
    path(
        'change-password',
        user_controller.change_password,
        name='change password user'
    ),

    path(
        'profile',
        user_controller.profile_controller,
        name='profile controller'
    ),
]
