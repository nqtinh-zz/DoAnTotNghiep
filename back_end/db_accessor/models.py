#  @Project FCloudConsole
#  @Homepage https://fsmartstore.com
#  @Copyright (c) 2018 Fujinet Systems JSC. All Rights Reserved.
#  @License All resources of the source code are owned by 'Fujinet Systems JSC'.
#  Intentionally infringing, stealing, exchanging, or trading in all of the
#  resources below without our consent, is a violation of intellectual property
#  rights. So, if you accidentally receive this source code, please send an email
#  to rd-support@fujinet.net, so we can find the best solution for this problem.

from django.db import models

# Create your models here.


from django.db.models.signals import post_delete
from django.dispatch import receiver

MODELS_AUTO_FIELD = models.AutoField(primary_key=True)


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=32)
    email = models.CharField(unique=True, max_length=100)
    password = models.CharField(max_length=128)
    full_name = models.CharField(max_length=200, blank=True, null=True)
    role = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    REQUIRED_FIELDS = ['full_name', 'password']
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    is_authenticated = True
    is_anonymous = True


    class Meta:
        app_label = 'web_admin'
        db_table = 'fccm_user'


    def __str__(self):
        return self.username


class Profile(models.Model):
    profile_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    company = models.CharField(max_length=200, blank=True, null=True)


    class Meta:
        app_label = 'web_admin'
        db_table = 'fccm_profile'


class UserRole(models.Model):
    user_role_id = models.IntegerField(primary_key=True)
    user_role_description = models.CharField(max_length=45, blank=True, null=True)


    class Meta:
        app_label = 'web_admin'
        db_table = 'fccm_user_role'


    def __str__(self):
        return self.user_role_description


class UserToken(models.Model):
    user_token_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    token = models.CharField(max_length=500)
    created_at = models.DateTimeField()
    expiration_date = models.DateTimeField()
    status = models.IntegerField()


    class Meta:
        app_label = 'web_admin'
        db_table = 'fccm_user_token'


    def __str__(self):
        return self.token


class XrefAvatarUser(models.Model):
    avatar_id = models.AutoField(primary_key=True)
    avatar_file = models.CharField(null=True, max_length=2083)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')


    class Meta:
        app_label = 'web_admin'
        db_table = 'fccm_user_avatar'


class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    project_code = models.CharField(max_length=255)
    project_name = models.CharField(max_length=255)
    owner_user_id = models.IntegerField()
    secret_key = models.CharField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    status = models.IntegerField(null=True, blank=True)


    class Meta:
        app_label = 'fcloudserver'
        db_table = 'fccm_project'


class Function(models.Model):
    function_id = models.AutoField(primary_key=True)
    function_name = models.CharField(max_length=255)


    class Meta:
        app_label = 'fcloudserver'
        db_table = 'fccm_function'


class ApiKey(models.Model):
    api_key_id = models.AutoField(primary_key=True)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE, db_column='project_id')
    function_id = models.ForeignKey(Function, on_delete=models.CASCADE, db_column='function_id')
    api_key = models.CharField(max_length=500)
    status = models.IntegerField(null=True, blank=True)


    class Meta:
        app_label = 'fcloudserver'
        db_table = 'fcct_api_key'


class People(models.Model):
    person_id = models.AutoField(primary_key=True)
    person_code = models.CharField(max_length=255)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE, db_column='project_id')
    status = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)


    class Meta:
        app_label = 'fcloudserver'
        db_table = 'res_people'


class ResPeopleImage(models.Model):
    asset_id = models.AutoField(primary_key=True)
    person_id = models.ForeignKey(People, on_delete=models.CASCADE, db_column='person_id')
    image_file = models.CharField(null=True, max_length=2083)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)


    class Meta:
        app_label = 'fcloudserver'
        db_table = 'res_people_recognition_assets_image_v2'


class PeopleGroup(models.Model):
    people_group_id = models.AutoField(primary_key=True)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE, db_column='project_id')
    people_group_code = models.CharField(max_length=50)
    people_group_name = models.CharField(max_length=255)
    people_group_color = models.CharField(max_length=50)
    status = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)


    class Meta:
        app_label = 'fcloudserver'
        db_table = 'res_people_groups'


class XrefPeopleGroup(models.Model):
    person_id = models.ForeignKey(People, on_delete=models.CASCADE, db_column='person_id')
    people_group_id = models.ForeignKey(PeopleGroup, on_delete=models.CASCADE, db_column='people_group_id')


    class Meta:
        app_label = 'fcloudserver'
        db_table = 'res_people_people_groups_xrefs'


class Camera(models.Model):
    camera_id = models.AutoField(primary_key=True)
    camera_name = models.CharField(unique=True, max_length=32)
    stream_url = models.CharField(max_length=1000)
    access_info = models.CharField(max_length=45)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE, db_column='project_id')
    status = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)


    class Meta:
        app_label = 'fcloudserver'
        db_table = 'res_camera'


class CameraGroup(models.Model):
    camera_group_id = MODELS_AUTO_FIELD
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE, db_column='project_id')
    camera_group_name = models.CharField(max_length=255)
    camera_group_color = models.CharField(max_length=50)
    status = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)


    class Meta:
        app_label = 'fcloudserver'
        db_table = 'res_camera_groups'


class XrefCameraGroup(models.Model):
    camera_id = models.ForeignKey(Camera, on_delete=models.CASCADE, db_column='camera_id')
    camera_group_id = models.ForeignKey(CameraGroup, on_delete=models.CASCADE, db_column='camera_group_id')


    class Meta:
        app_label = 'fcloudserver'
        db_table = 'res_camera_camera_groups_xrefs'


class Process(models.Model):
    process_id = models.AutoField(primary_key=True)
    process_name = models.CharField(max_length=255)
    process_token = models.CharField(max_length=100, null=True)
    camera_id = models.ForeignKey(Camera, on_delete=models.CASCADE, db_column='camera_id')
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE, db_column='project_id')
    process_config = models.CharField(null=True, max_length=2083)
    process_status = models.IntegerField()
    people_group_id = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        app_label = 'fcloudserver'
        db_table = 'process'


class XrefProcessPeopleGroup(models.Model):
    process_id = models.ForeignKey(Process, on_delete=models.CASCADE, db_column='process_id')
    people_group_id = models.ForeignKey(PeopleGroup, on_delete=models.CASCADE, db_column='people_group_id')


    class Meta:
        app_label = 'fcloudserver'
        db_table = 'xref_process_people_group'
