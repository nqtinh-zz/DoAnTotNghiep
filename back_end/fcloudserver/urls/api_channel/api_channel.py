#  @Project FCloudConsole
#  @Homepage https://fsmartstore.com
#  @Copyright (c) 2018 Fujinet Systems JSC. All Rights Reserved.
#  @License All resources of the source code are owned by 'Fujinet Systems JSC'.
#  Intentionally infringing, stealing, exchanging, or trading in all of the
#  resources below without our consent, is a violation of intellectual property
#  rights. So, if you accidentally receive this source code, please send an email
#  to rd-support@fujinet.net, so we can find the best solution for this problem.

from django.urls import path

from ...views import server_controller

channel_patterns = [
    path(
        'create-process',
        server_controller.create_process,
        name='Create process',
    ),
    path(
        'get-default-config',
        server_controller.get_default_config,
        name='Get default camera config',
    ),
    path(
        'get-process-list',
        server_controller.get_process_list,
        name='Get default camera config',
    ),
    path(
        'delete-process',
        server_controller.delete_process,
        name='Delete process',
    ),
    path(
        'update-process',
        server_controller.update_process,
        name='Update process',
    ),
    path(
        'start-process',
        server_controller.start_process,
        name='Start process',
    ),
    path(
        'stop-process',
        server_controller.stop_process,
        name='Stop process',
    ),
    path(
        'get-process',
        server_controller.get_process,
        name='Get process',
    ),
]
