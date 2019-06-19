#  @Project FCloudConsole
#  @Homepage https://fsmartstore.com
#  @Copyright (c) 2018 Fujinet Systems JSC. All Rights Reserved.
#  @License All resources of the source code are owned by 'Fujinet Systems JSC'.
#  Intentionally infringing, stealing, exchanging, or trading in all of the
#  resources below without our consent, is a violation of intellectual property
#  rights. So, if you accidentally receive this source code, please send an email
#  to rd-support@fujinet.net, so we can find the best solution for this problem.


import base64
import os
import uuid
from datetime import datetime

import six
from django.core.files.base import ContentFile
from django.db.models import Q

# from config.log_config import log
from config.django_settings import STATIC_DIR
from db_accessor.models import (People, PeopleGroup, Project, ResPeopleImage, XrefPeopleGroup)
from fcloudserver.helper.face_desc_gen import FaceRecCoreV1
from fcloudserver.helper.image_helper import multipart_file_to_np_image
from static_serving import StaticServing
from utils.constants import *
from utils.result import Result


class ResPeopleProcess:

    @classmethod
    def get_file_extension(cls, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension

    @classmethod
    def decode_base64_file(cls, data):

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
                # Generate file name:
                file_name = str(uuid.uuid4())[:12]  # 12 characters are more than enough.
                # Get the file name extension:
                file_extension = cls.get_file_extension(file_name, decoded_file)

                complete_file_name = "%s.%s" % (file_name, file_extension,)

                return ContentFile(decoded_file, name=complete_file_name)
            except TypeError:
                TypeError('invalid_image')

    @classmethod
    def parse_import_person_data(cls, request):
        """
                Parse creation project data from request
                :param request: the data that the user submitted the request
                :return: a dict containing username, password, password_confirm, fullname
                information if it exists, otherwise None
                """

        if KEY_PERSON_CODE in request and KEY_PROJECT_ID in request:
            return {
                KEY_PERSON_CODE: request[KEY_PERSON_CODE],
                KEY_PROJECT_ID: request[KEY_PROJECT_ID],
            }
        else:
            return None

    @classmethod
    def import_person(cls, request):
        person_array = request.FILES.keys()

        if len(person_array) == 0:
            return
        for one_person in person_array:
            check_person_code = People.objects.filter(
                person_code=one_person,
                project_id=Project.objects.get(
                    project_id=request.data.get('project_id')),
                status=DEFAULT_STATUS_ACTIVE,
            ).values()

            if not check_person_code:
                result_create_person = People.objects.create(
                    person_code=one_person,
                    project_id=Project.objects.get(project_id=request.data.get('project_id')),
                    status=DEFAULT_STATUS_ACTIVE
                )

                if result_create_person:
                    person_just_created = list(People.objects.filter(
                        person_code=one_person,
                        project_id=Project.objects.get(project_id=request.data.get('project_id')),
                        status=DEFAULT_STATUS_ACTIVE,
                    ).values())[0]

                    if len(request.FILES.getlist(one_person)) != 0:
                        project_id = request.data.get('project_id')
                        for item in request.FILES.getlist(one_person):
                            face_desc = cls.gen_face_desc(item)
                            if face_desc is not None:
                                _, serve_urls, exc = StaticServing.save_res(
                                    [item],
                                    [
                                        f'{project_id}',
                                        'person_images',
                                        f'{one_person}'
                                    ]
                                )
                                if exc is not None:
                                    raise IOError(f'Save image file failed: {exc}')

                                img_url = serve_urls[0]

                                try:
                                    result_create_image_person = ResPeopleImage.objects.create(
                                        person_id=People.objects.get(
                                            person_id=person_just_created.get(KEY_PERSON_ID)
                                        ),
                                        image_file=img_url,
                                        description=face_desc,
                                    )

                                except Exception as exc:
                                    # log.error(f'Save person image to db failed: {exc}')
                                    return Result.failed(
                                        message=f'Save person image to db failed: {exc}'
                                    )

                                if not result_create_image_person:
                                    return Result.failed(
                                        message='Have some problem when add image data!'
                                    )
                        if request.data.get('group') == '':
                            group_array = []
                        else:
                            group_array = request.data.get('group').split(',')
                            print(group_array)
                        if len(group_array) != 0:
                            for group in group_array:
                                print(group)
                                result_create_group_person = XrefPeopleGroup.objects.create(
                                    person_id=People.objects.get(
                                        person_id=person_just_created.get(KEY_PERSON_ID),
                                        status=DEFAULT_STATUS_ACTIVE
                                    ),
                                    people_group_id=PeopleGroup.objects.get(
                                        people_group_code=group,
                                        project_id=Project.objects.get(project_id=request.data.get('project_id')),
                                        status=DEFAULT_STATUS_ACTIVE
                                    )
                                )
                                if not result_create_group_person:
                                    return Result.failed(
                                        message='Have some problem when create group!'
                                    )

                else:
                    return Result.failed(
                        message='Have some problem when add person!'
                    )
            else:
                ResPeopleImage.objects.filter(
                    person_id=list(
                        People.objects.filter(
                            person_code=one_person,
                            status=DEFAULT_STATUS_ACTIVE,
                            project_id=request.data.get('project_id')).values())[0].get(KEY_PERSON_ID)).delete()
                XrefPeopleGroup.objects.filter(
                    person_id=People.objects.get(
                        person_id=list(People.objects.filter(
                            person_code=one_person,
                            project_id=request.data.get('project_id'),
                            status=DEFAULT_STATUS_ACTIVE,
                        ).values())[0].get(KEY_PERSON_ID))).delete()
                if len(request.FILES.getlist(one_person)) != 0:
                    project_id = request.data.get('project_id')
                    for item in request.FILES.getlist(one_person):
                        face_desc = cls.gen_face_desc(item)
                        if face_desc is not None:
                            _, serve_urls, exc = StaticServing.save_res(
                                [item],
                                [
                                    f'{project_id}',
                                    'person_images',
                                    f'{one_person}'
                                ]
                            )
                            if exc is not None:
                                raise IOError(f'Save image file failed: {exc}')

                            img_url = serve_urls[0]

                            try:
                                result_create_image_person = ResPeopleImage.objects.create(
                                    person_id=People.objects.get(
                                        person_id=list(People.objects.filter(
                                            person_code=one_person,
                                            project_id=request.data.get('project_id'),
                                            status=DEFAULT_STATUS_ACTIVE,
                                        ).values())[0].get(KEY_PERSON_ID)
                                    ),
                                    image_file=img_url,
                                    description=face_desc,
                                )

                            except Exception as exc:
                                # log.error(f'Save person image to db failed: {exc}')
                                return Result.failed(
                                    message=f'Save person image to db failed: {exc}'
                                )

                            if not result_create_image_person:
                                return Result.failed(
                                    message='Have some problem when add image data!'
                                )

                    if request.data.get('group') == '':
                        group_array = []
                    else:
                        group_array = request.data.get('group').split(",")

                    if len(group_array) != 0:
                        for group in group_array:
                            check_group_people = XrefPeopleGroup.objects.filter(
                                person_id=People.objects.get(
                                    person_id=list(People.objects.filter(
                                        person_code=one_person,
                                        project_id=request.data.get('project_id'),
                                        status=DEFAULT_STATUS_ACTIVE,
                                    ).values())[0].get(KEY_PERSON_ID)),
                                people_group_id=PeopleGroup.objects.get(people_group_code=group,
                                                                        project_id=Project.objects.get(
                                                                            project_id=request.data.get(
                                                                                'project_id')), )
                            ).values()

                            if not check_group_people:
                                result_create_group_person = XrefPeopleGroup.objects.create(
                                    person_id=People.objects.get(
                                        person_id=list(People.objects.filter(
                                            person_code=one_person,
                                            project_id=request.data.get('project_id'),
                                            status=DEFAULT_STATUS_ACTIVE,
                                        ).values())[0].get(
                                            KEY_PERSON_ID)),
                                    people_group_id=PeopleGroup.objects.get(people_group_code=group,
                                                                            project_id=Project.objects.get(
                                                                                project_id=request.data.get(
                                                                                    'project_id')), )
                                )
                                if not result_create_group_person:
                                    return Result.failed(
                                        message='Have some problem when create group!'
                                    )

        return Result.success(
            message='Success add person!'
        )

    @classmethod
    def add_person(cls, request):
        project_id = request.data.get('project_id')
        person_code = request.data.get('person_code')
        print(request.data)
        check_person_code = People.objects.filter(
            person_code=person_code,
            project_id=Project.objects.get(
                project_id=project_id),
            status=DEFAULT_STATUS_ACTIVE,
        ).values()
        if not check_person_code:
            result_create_person = People.objects.create(
                person_code=person_code,
                project_id=Project.objects.get(project_id=project_id),
                status=DEFAULT_STATUS_ACTIVE
            )
            if result_create_person:
                person_just_created = list(People.objects.filter(
                    person_code=person_code,
                    project_id=Project.objects.get(project_id=request.data.get('project_id')),
                    status=DEFAULT_STATUS_ACTIVE,
                ).values())[0]
                if request.data.get('group') == '':
                    group_array = []
                else:
                    group_array = request.data.get('group').split(",")
                if len(group_array) != 0:
                    for group in group_array:
                        result_create_group_person = XrefPeopleGroup.objects.create(
                            person_id=People.objects.get(
                                person_id=person_just_created.get(KEY_PERSON_ID),
                                status=DEFAULT_STATUS_ACTIVE
                            ),
                            people_group_id=PeopleGroup.objects.get(
                                people_group_code=group,
                                status=DEFAULT_STATUS_ACTIVE
                            )
                        )
                        if not result_create_group_person:
                            return Result.failed(
                                message='Have some problem when create group!'
                            )

                if len(request.FILES.getlist(person_code)) != 0:
                    project_id = request.data.get('project_id')
                    for item in request.FILES.getlist(person_code):
                        face_desc = cls.gen_face_desc(item)
                        if face_desc is not None:
                            _, serve_urls, exc = StaticServing.save_res(
                                [item],
                                [
                                    f'{project_id}',
                                    'person_images',
                                    f'{person_code}'
                                ]
                            )
                            if exc is not None:
                                raise IOError(f'Save image file failed: {exc}')

                            img_url = serve_urls[0]

                            try:
                                result_create_image_person = ResPeopleImage.objects.create(
                                    person_id=People.objects.get(
                                        person_id=person_just_created.get(KEY_PERSON_ID)
                                    ),
                                    image_file=img_url,
                                    description=face_desc,
                                )

                            except Exception as exc:
                                # log.error(f'Save person image to db failed: {exc}')
                                return Result.failed(
                                    message=f'Save person image to db failed: {exc}'
                                )

                            if not result_create_image_person:
                                return Result.failed(
                                    message='Have some problem when add image data!'
                                )


                return Result.success(
                    message='Success add person!'
                )

            else:
                return Result.failed(
                    message='Have some problem when add person!'
                )
        else:
            return Result.failed(
                message='Person code already existed!'
            )

    @classmethod
    def parse_update_person_data(cls, request):
        """
                Parse creation project data from request
                :param request: the data that the user submitted the request
                :return: a dict containing username, password, password_confirm, fullname
                information if it exists, otherwise None
                """

        if KEY_PERSON_ID in request.data and KEY_PROJECT_ID in request.data:
            return {
                KEY_PERSON_ID: request.data[KEY_PERSON_ID],
                KEY_PERSON_CODE: request.data[KEY_PERSON_CODE],
                KEY_PROJECT_ID: request.data[KEY_PROJECT_ID],
            }
        else:
            return None

    @classmethod
    def update_person(cls, request):
        print(request.data)
        project_id = request.data.get('project_id')
        print(project_id)
        person_id = request.data.get('person_id')
        print(request.FILES)
        # person_code = list(request.FILES.keys())[0]
        person_code = request.data.get('person_code')
        if person_code:
            check_person_code = list(People.objects.filter(
                ~Q(person_id=person_id),
                person_code=person_code,
                project_id=Project.objects.get(
                    project_id=project_id),
                status=DEFAULT_STATUS_ACTIVE,
            ).values())
            if not check_person_code:
                person_update = People.objects.get(person_id=person_id)
                person_update.person_code = person_code
                person_update.updated_at = datetime.now()
                person_update.save()
                ResPeopleImage.objects.filter(person_id=person_id).delete()
                if len(request.FILES.getlist(person_update.person_code)) != 0:
                    for item in request.FILES.getlist(person_update.person_code):
                        face_desc = cls.gen_face_desc(item)
                        if face_desc is not None:
                            _, serve_urls, exc = StaticServing.save_res(
                                [item],
                                [
                                    f'{project_id}',
                                    'person_images',
                                    f'{person_update.person_code}'
                                ]
                            )
                            if exc is not None:
                                raise IOError(f'Save image file failed: {exc}')

                            img_url = serve_urls[0]

                            try:
                                result_create_image_person = ResPeopleImage.objects.create(
                                    person_id=People.objects.get(
                                        person_id=person_id
                                    ),
                                    image_file=img_url,
                                    description=face_desc,
                                )

                            except Exception as exc:
                                # log.error(f'Save person image to db failed: {exc}')
                                return Result.failed(
                                    message=f'Save person image to db failed: {exc}'
                                )

                            if not result_create_image_person:
                                return Result.failed(
                                    message='Have some problem when add image data!'
                                )

                return Result.success(
                    message='Success edit person!'
                )

            else:
                return Result.failed(
                    message='Person code duplicated!'
                )
        else:
            return Result.failed(
                message='Missing data in the request!'
            )

    @classmethod
    def get_all_person(cls, request):
        print(request.data)
        project_id = request.GET['project_id']
        if project_id:
            try:
                all_people = People.objects.filter(
                    project_id=Project.objects.get(project_id=project_id),
                    status=DEFAULT_STATUS_ACTIVE
                )
            except Project.DoesNotExist:
                return Result.failed(
                    message='Project doesnt exist'
                )
            result = []
            list_all_people = list(all_people.values())
            for person in list_all_people:

                try:
                    check_person = People.objects.get(person_id=person.get('person_id'))
                    group_list = []
                    xref_people_group = list(XrefPeopleGroup.objects.select_related('person_id')
                                             .filter(person_id=check_person.person_id).values())
                    for item in xref_people_group:
                        group_item = \
                            list(PeopleGroup.objects.select_related('people_group_id')
                                 .filter(people_group_id=item.get('people_group_id_id'),
                                         project_id=Project.objects.get(project_id=project_id)).values())
                        if len(group_item) > 0:
                            group_list.append(group_item[0])

                    person['group'] = group_list
                    result.append(person)
                except People.DoesNotExist:
                    return Result.failed(
                        message='Person id  not exist!'
                    )
            return Result.success(
                message='Get all people success',
                data=result
            )

        else:
            return Result.failed(
                message='Missing data in the request!'
            )

    @classmethod
    def parse_delete_people_data(cls, request):
        """
                Parse creation project data from request
                :param request: the data that the user submitted the request
                :return: a dict containing username, password, password_confirm, fullname
                information if it exists, otherwise None
                """

        if KEY_PERSON_ID in request.data and KEY_PROJECT_ID in request.data:
            return {
                KEY_PERSON_ID: request.data[KEY_PERSON_ID],
                KEY_PROJECT_ID: request.data[KEY_PROJECT_ID],
            }
        else:
            return None

    @classmethod
    def delete_person(cls, request):
        result_delete_person = cls.parse_delete_people_data(request)
        if result_delete_person:
            try:
                check_person = People.objects.get(
                    person_id=result_delete_person.get(KEY_PERSON_ID),
                    project_id=result_delete_person.get(KEY_PROJECT_ID))
                xref_people_group = XrefPeopleGroup.objects.select_related('person_id') \
                    .filter(person_id=result_delete_person[KEY_PERSON_ID])
                image_people = ResPeopleImage.objects.select_related('person_id') \
                    .filter(person_id=result_delete_person[KEY_PERSON_ID])
                xref_people_group.delete()
                image_people.delete()
                check_person.status = 0
                check_person.save()
                return Result.success(
                    message='Success delete people'
                )
            except People.DoesNotExist:
                return Result.failed(
                    message='There is no person with this ID!'
                )
        else:
            return Result.failed(
                message='Missing data in the request!'
            )

    @classmethod
    def parse_add_people_group_data(cls, request):
        """
            Parse add group data from request
            :param request: the data that the user submitted the request
            :return: a dict containing username, password, password_confirm, fullname
            information if it exists, otherwise None
        """

        if KEY_PROJECT_ID in request.data and KEY_PEOPLE_GROUP_CODE in request.data \
                and KEY_PEOPLE_GROUP_COLOR in request.data and KEY_PEOPLE_GROUP_NAME in request.data:

            return {
                KEY_PROJECT_ID: request.data[KEY_PROJECT_ID],
                KEY_PEOPLE_GROUP_CODE: request.data[KEY_PEOPLE_GROUP_CODE],
                KEY_PEOPLE_GROUP_COLOR: request.data[KEY_PEOPLE_GROUP_COLOR],
                KEY_PEOPLE_GROUP_NAME: request.data[KEY_PEOPLE_GROUP_NAME],
            }
        else:
            return None

    @classmethod
    def add_people_group(cls, request):
        result_group_data = cls.parse_add_people_group_data(request)

        if result_group_data:
            check_group_exist = PeopleGroup.objects.filter(
                project_id=result_group_data[KEY_PROJECT_ID],
                people_group_code=result_group_data[
                    KEY_PEOPLE_GROUP_CODE],
                status=DEFAULT_STATUS_ACTIVE
            )
            if not check_group_exist:
                check_color_exist = PeopleGroup.objects.filter(
                    people_group_color=result_group_data[KEY_PEOPLE_GROUP_COLOR])
                if not check_color_exist:
                    try:
                        result_group = PeopleGroup.objects.create(
                            project_id=Project.objects.get(project_id=result_group_data[KEY_PROJECT_ID]),
                            people_group_code=result_group_data[KEY_PEOPLE_GROUP_CODE],
                            people_group_name=result_group_data[KEY_PEOPLE_GROUP_NAME],
                            people_group_color=result_group_data[KEY_PEOPLE_GROUP_COLOR],
                            status=DEFAULT_STATUS_ACTIVE
                        )
                    except Project.DoesNotExist:
                        return Result.failed(
                            message='Project doesnt exist'
                        )
                    if result_group:
                        new_group = PeopleGroup.objects.filter(
                            people_group_code=result_group_data[KEY_PEOPLE_GROUP_CODE])
                        new_group_data = list(new_group.values())[0]
                        return Result.success(
                            message='New people group has been created',
                            data=new_group_data
                        )
                    else:
                        return Result.failed(
                            message='Have some problem when create new people group'
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
    def parse_delete_people_group_data(cls, request):
        """
            Parse add group data from request
            :param request: the data that the user submitted the request
            :return: a dict containing username, password, password_confirm, fullname
            information if it exists, otherwise None
        """

        if KEY_PEOPLE_GROUP_ID in request.data:
            return {
                KEY_PEOPLE_GROUP_ID: request.data[KEY_PEOPLE_GROUP_ID],
            }
        else:
            return None

    @classmethod
    def delete_people_group(cls, request):
        try:
            people_group_id = request.GET['people_group_id']
            delete_group = PeopleGroup.objects.get(people_group_id=people_group_id)
            if delete_group:
                try:
                    xref_people_group = XrefPeopleGroup.objects.select_related('people_group_id') \
                        .filter(people_group_id=people_group_id)
                    delete_group.status = 0
                    delete_group.save()
                    xref_people_group.delete()
                    return Result.success(
                        message='Delete group success!',
                    )
                except PeopleGroup.DoesNotExist:
                    return Result.failed(
                        message='PeopleGroup matching query does not exist'
                    )

            else:
                return Result.failed(
                    message='Group doesnt exist'
                )
        except PeopleGroup.DoesNotExist:
            return Result.failed(
                message='People group doesnot exist!'
            )
        except Exception as exc:
            return Result.failed(
                message=f'Missing data from request: {exc}'
            )

    @classmethod
    def parse_update_people_group_data(cls, request):
        """
            Parse add group data from request
            :param request: the data that the user submitted the request
            :return: a dict containing username, password, password_confirm, fullname
            information if it exists, otherwise None
        """

        if KEY_PEOPLE_GROUP_ID in request.data \
                and KEY_PEOPLE_GROUP_CODE in request.data \
                and KEY_PEOPLE_GROUP_COLOR in request.data \
                and KEY_PEOPLE_GROUP_NAME in request.data:

            return {
                KEY_PEOPLE_GROUP_ID: request.data[KEY_PEOPLE_GROUP_ID],
                KEY_PEOPLE_GROUP_CODE: request.data[KEY_PEOPLE_GROUP_CODE],
                KEY_PEOPLE_GROUP_COLOR: request.data[KEY_PEOPLE_GROUP_COLOR],
                KEY_PEOPLE_GROUP_NAME: request.data[KEY_PEOPLE_GROUP_NAME],
            }
        else:
            return None

    @classmethod
    def update_people_group(cls, request):
        result_group_data = cls.parse_update_people_group_data(request)
        if result_group_data:
            people_group_choose = PeopleGroup.objects.filter(people_group_id=result_group_data[KEY_PEOPLE_GROUP_ID])
            if people_group_choose:
                check_group_code = PeopleGroup.objects.filter(
                    ~Q(people_group_id=result_group_data[KEY_PEOPLE_GROUP_ID]),
                    people_group_code=result_group_data[KEY_PEOPLE_GROUP_CODE],
                    status=DEFAULT_STATUS_ACTIVE
                )
                check_group_name = PeopleGroup.objects.filter(
                    ~Q(people_group_id=result_group_data[KEY_PEOPLE_GROUP_ID]),
                    people_group_name=result_group_data[KEY_PEOPLE_GROUP_NAME],
                    status=DEFAULT_STATUS_ACTIVE
                )
                check_group_color = PeopleGroup.objects.filter(
                    ~Q(people_group_id=result_group_data[KEY_PEOPLE_GROUP_ID]),
                    people_group_color=result_group_data[KEY_PEOPLE_GROUP_COLOR],
                    status=DEFAULT_STATUS_ACTIVE,
                )
                if check_group_code:
                    return Result.failed(
                        message='This group code exists'
                    )
                elif check_group_name:
                    return Result.failed(
                        message='This group name exists'
                    )
                elif check_group_color:
                    return Result.failed(
                        message='This group color exists'
                    )
                else:
                    people_group_choose.update(people_group_name=result_group_data[KEY_PEOPLE_GROUP_NAME],
                                               people_group_code=result_group_data[KEY_PEOPLE_GROUP_CODE],
                                               people_group_color=result_group_data[KEY_PEOPLE_GROUP_COLOR],
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
    def get_all_people_group(cls, request):
        project_id = request.GET['project_id']
        if project_id:
            try:
                all_people_group = PeopleGroup.objects.filter(
                    project_id=Project.objects.get(project_id=project_id),
                    status=DEFAULT_STATUS_ACTIVE
                )
            except Project.DoesNotExist:
                return Result.failed(
                    message='Project doesnt exist'
                )
            list_all_people_group = list(all_people_group.values())
            return Result.success(
                message='Get all group success',
                data=list_all_people_group
            )

        else:
            return Result.failed(
                message='Missing data in the request!'
            )

    @classmethod
    def get_people_group_data(cls, request):
        people_group_id = request.GET['people_group_id']
        if people_group_id:
            try:
                check_group = PeopleGroup.objects.get(people_group_id=people_group_id)
                result = {
                    KEY_PEOPLE_GROUP_ID: check_group.people_group_id,
                    KEY_PEOPLE_GROUP_CODE: check_group.people_group_code,
                    KEY_PEOPLE_GROUP_NAME: check_group.people_group_name,
                    KEY_PEOPLE_GROUP_COLOR: check_group.people_group_color,
                }
                return Result.success(
                    message='Get group success',
                    data=result
                )
            except PeopleGroup.DoesNotExist:
                return Result.failed(
                    message='Group doesnt exist!'
                )
        else:
            return Result.failed(
                message='Missing data in the request!'
            )

    @classmethod
    def parse_add_person_to_group(cls, request):
        """
            Parse add group data from request
            :param request: the data that the user submitted the request
            :return: a dict containing username, password, password_confirm, fullname
            information if it exists, otherwise None
        """

        if KEY_PERSON_ID in request.data and KEY_PROJECT_ID in request.data:

            return {
                KEY_PERSON_ID: request.data[KEY_PERSON_ID],
                KEY_PROJECT_ID: request.data[KEY_PROJECT_ID],
            }
        else:
            return None

    @classmethod
    def add_person_to_group(cls, request):
        request_data = cls.parse_add_person_to_group(request)
        if request_data:
            try:
                check_person = People.objects.get(
                    person_id=request_data.get(KEY_PERSON_ID),
                    project_id=Project.objects.get(project_id=request_data.get(KEY_PROJECT_ID))
                )
                group_arr = request.data.get(KEY_GROUP_ARRAY)
                for group in group_arr:
                    check_group = PeopleGroup.objects.get(
                        people_group_code=group,
                        project_id=Project.objects.get(project_id=request_data.get(KEY_PROJECT_ID))
                    )
                    check_person_xref = XrefPeopleGroup.objects.filter(
                        person_id=check_person,
                        people_group_id=check_group
                    )
                    if not check_person_xref:
                        result = XrefPeopleGroup.objects.create(
                            person_id=check_person,
                            people_group_id=check_group,
                        )
                        if not result:
                            return Result.failed(
                                message='Have some problem when add person to group!'
                            )
                    else:
                        return Result.failed(
                            message='This person already in this group!'
                        )
                return Result.success(
                    message='Add person to group success!'
                )
            except (People.DoesNotExist, PeopleGroup.DoesNotExist):
                return Result.failed(
                    message='Person id or group id not exist!'
                )
        else:
            return Result.failed(
                message='Missing data in the request!'
            )

    @classmethod
    def parse_delete_person_from_group_data(cls, request):
        """
            Parse add group data from request
            :param request: the data that the user submitted the request
            :return: a dict containing username, password, password_confirm, fullname
            information if it exists, otherwise None
        """

        if KEY_PERSON_ID in request.data and KEY_PEOPLE_GROUP_ID in request.data and KEY_PROJECT_ID in request.data:

            return {
                KEY_PROJECT_ID: request.data[KEY_PROJECT_ID],
                KEY_PERSON_ID: request.data[KEY_PERSON_ID],
                KEY_PEOPLE_GROUP_ID: request.data[KEY_PEOPLE_GROUP_ID],
            }
        else:
            return None

    @classmethod
    def delete_person_from_group(cls, request):
        request_data = cls.parse_delete_person_from_group_data(request)
        if request_data:
            try:
                check_person = People.objects.get(person_id=request_data.get(KEY_PERSON_ID),
                                                  project_id=Project.objects.get(
                                                      project_id=request_data.get(KEY_PROJECT_ID)))
                check_group = PeopleGroup.objects.get(people_group_id=request_data.get(KEY_PEOPLE_GROUP_ID))
                result = XrefPeopleGroup.objects.filter(
                    person_id=check_person,
                    people_group_id=check_group,
                )
                if result:
                    result.delete()
                    return Result.success(
                        message='Delete person from group success!'
                    )
                else:
                    return Result.failed(
                        message='Have some problem when delete person to group!'
                    )
            except (People.DoesNotExist, PeopleGroup.DoesNotExist, Project.DoesNotExist):
                return Result.failed(
                    message='Person id or group id not exist!'
                )
        else:
            return Result.failed(
                message='Missing data in the request!'
            )

    @classmethod
    def get_group_of_person(cls, request):
        person_code = request.GET['person_code']

        if person_code:
            try:
                check_person = People.objects.get(person_id=person_code)
                group_list = []
                xref_people_group = list(XrefPeopleGroup.objects.select_related('person_id')
                                         .filter(person_id=check_person.person_id).values())
                for item in xref_people_group:
                    group_item = \
                        list(PeopleGroup.objects.select_related('people_group_id')
                             .filter(people_group_id=item.get('people_group_id_id')).values())[0]
                    group_list.append(group_item)
                return Result.success(
                    message='Get group of person success!',
                    data=group_list
                )
            except People.DoesNotExist:
                return Result.failed(
                    message='Person id  not exist!'
                )
        else:
            return Result.failed(
                message='Missing data in the request!'
            )

    @classmethod
    def parse_get_image_person_data(cls, request):
        """
            Parse add group data from request
            :param request: the data that the user submitted the request
            :return: a dict containing username, password, password_confirm, fullname
            information if it exists, otherwise None
        """

        if KEY_PERSON_ID in request.data:

            return {
                KEY_PERSON_ID: request.data[KEY_PERSON_ID],
            }
        else:
            return None

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
    def get_image_person(cls, request):
        request_data = cls.parse_get_image_person_data(request)
        if request_data:
            try:
                check_image = ResPeopleImage.objects.filter(
                    person_id=People.objects.get(person_id=request_data[KEY_PERSON_ID])
                ).values()
                result = []
                for item in list(check_image):
                    link = item.get('image_file').split('/static')
                    result.append(cls.image_as_base64(STATIC_DIR + link[1]))
                return Result.success(
                    message='Get image of person success!',
                    data=result
                )
            except People.DoesNotExist:
                return Result.failed(
                    message='Person doesnt exist!'
                )
        else:
            return Result.failed(
                message='Missing data in the request!'
            )

    @staticmethod
    def gen_face_desc(multipart_file):
        np_image = multipart_file_to_np_image(multipart_file)
        face_desc = FaceRecCoreV1.gen_face_desc(np_image)
        if face_desc is None:
            return None

        face_desc_str = ' '.join(
            f'{vector:.25f}' for vector in face_desc
        )

        return face_desc_str

    @classmethod
    def people_group_list_people(cls, request):
        group_id = request.GET['group_id']
        print(group_id)

        if group_id:
            xref_people_group = list(XrefPeopleGroup.objects.select_related('person_id')
                                     .filter(people_group_id=group_id).values())

            print(xref_people_group)
            result = []
            for item in xref_people_group:
                person = list(People.objects.filter(
                    person_id=item.get('person_id_id'),
                    status=DEFAULT_STATUS_ACTIVE).values())[0]
                print(person)
                group_list = []
                xref_person_group_tmp = list(XrefPeopleGroup.objects.select_related('person_id')
                                             .filter(person_id=item.get('person_id_id')).values())
                for tmp in xref_person_group_tmp:
                    group_item = \
                        list(PeopleGroup.objects.select_related('people_group_id')
                             .filter(people_group_id=tmp.get('people_group_id_id'),
                                     ).values())
                    if len(group_item) > 0:
                        group_list.append(group_item[0])
                temp = person
                temp['group'] = group_list
                result.append(temp)
            print('tinh')
            print(result)
            return Result.success(
                message='Status of all person',
                data=result
            )
        else:
            return Result.failed(
                message='Missing data from request!!'
            )