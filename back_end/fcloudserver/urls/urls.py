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

from django.urls import include, path

from fcloudserver.urls.api_channel.api_channel import channel_patterns
from .api_function.api_function import function_patterns
from .api_project.api_project import project_patterns
from .api_resources.api_res import res_patterns

fserver_patterns = [
    path('project/', include(project_patterns)),
    path('project/function/', include(function_patterns)),
    path('project/resources/', include(res_patterns)),
    path('project/channel/', include(channel_patterns), )
]
