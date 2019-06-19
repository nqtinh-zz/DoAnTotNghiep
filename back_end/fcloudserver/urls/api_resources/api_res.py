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

res_patterns = [
    path(
        'people-group',
        server_controller.people_group_controller,
        name='People group feature',
    ),
    path(
        'person',
        server_controller.person_controller,
        name='Person feature'
    ),
    path(
        'add-person-to-group',
        server_controller.add_person_to_group,
        name='add_person_to_group'
    ),
    path(
        'get-group-of-person',
        server_controller.get_group_of_person,
        name='get_group_of_person'
    ),
    path(
        'delete-person-from-group',
        server_controller.delete_person_from_group,
        name='delete_person_from_group'
    ),
    path(
        'get-image-person',
        server_controller.get_image_person,
        name='get_image_person'
    ),
    path(
        'import-person',
        server_controller.import_person,
        name='import_person'
    ),
    path(
        'camera',
        server_controller.camera_controller,
        name='Camera feature'
    ),
    path(
        'camera-group',
        server_controller.camera_group_controller,
        name='Camera group feature',
    ),
    path(
        'add-camera-to-group',
        server_controller.add_camera_to_group,
        name='add_camera_to_group'
    ),
    path(
        'delete-camera-from-group',
        server_controller.delete_camera_from_group,
        name='delete_camera_from_group'
    ),
    path(
        'check-camera-url',
        server_controller.check_all_camera_url,
        name='check_camera_url'
    ),
    path(
        'check-camera',
        server_controller.check_camera_url,
        name='check_camera'
    ),
    path(
        'live-stream',
        server_controller.video_feed,
        name='check_camera_url'
    ),
    path(
        'camera-group-list-camera',
        server_controller.camera_group_list_camera,
        name='camera_group_list_camera'
),
    path(
        'turn-off-camera',
        server_controller.turn_off_camera,
        name='turn_off_camera'
    ),
    path(
        'turn-on-camera',
        server_controller.turn_on_camera,
        name='turn_on_camera'),
 path(
        'people-group-list-people',
        server_controller.people_group_list_people,
        name='people_group_list_people'





    )    
]
