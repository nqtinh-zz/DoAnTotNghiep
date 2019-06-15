#  @Project FCloudConsole
#  @Homepage https://fsmartstore.com
#  @Copyright (c) 2018 Fujinet Systems JSC. All Rights Reserved.
#  @License All resources of the source code are owned by 'Fujinet Systems JSC'.
#  Intentionally infringing, stealing, exchanging, or trading in all of the
#  resources below without our consent, is a violation of intellectual property
#  rights. So, if you accidentally receive this source code, please send an email
#  to rd-support@fujinet.net, so we can find the best solution for this problem.

# Combine with user id for get token value
SECRET_TOKEN_KEY = 'e61a80a8eeb1233baeb0f66de824efe2'
SECRET_PASSWORD_KEY = '38edb88fd01f74862a4be38cd43eb06d'
SECRET_RESET_MASTER_ADMIN_PASSWORD_KEY = '8d3439f2af9cfa90a92b7336b4be8c92'

# ID LENGTH PLUS
ID_LENGTH = 10

# Key user information in request
KEY_USER_ID = 'user_id'
KEY_USER_TOKEN_ID = 'user_token_id'
KEY_USER_TOKEN = 'token'
KEY_USER_NAME = 'username'
KEY_USER_EMAIL = 'email'
KEY_USER_FULLNAME = 'full_name'
KEY_USER_PASSWORD = 'password'
KEY_USER_PASSWORD_CONFIRM = 'password_confirm'
KEY_USER_FIRSTNAME = 'first_name'
KEY_USER_LASTNAME = 'last_name'
KEY_TOKEN_EXPIRATION_DATE = 'expiration_date'
KEY_TOKEN_STATUS = 'status'
KEY_SECRET_RESTORE_MASTER_ADMIN_PASSWORD = 'key_restore_master_admin_password'
KEY_REQUEST_AUTHENTICATION: str = 'HTTP_AUTHORIZATION'
# Profile data
KEY_PROFILE_ID = 'profile_id'
KEY_PROFILE_ADDRESS = 'address'
KEY_PROFILE_COMPANY = 'company'

# Project data in request
KEY_PROJECT_ID = 'project_id'
KEY_PROJECT_CODE = 'project_code'
KEY_PROJECT_NAME = 'project_name'
KEY_PROJECT_OWNER_ID = 'owner_user_id'
KEY_PROJECT_SECRET_KEY = 'secret_key'
KEY_PROJECT_STATUS = 'status'

# Asset data in request
KEY_ASSET_ID = 'asset_id'
KEY_ASSET_PERSON_ID = 'person_id'
KEY_ASSET_IMAGE = 'image_file'

# Group people data in request
KEY_PEOPLE_GROUP_ID = 'people_group_id'
KEY_PEOPLE_GROUP_CODE = 'people_group_code'
KEY_PEOPLE_GROUP_NAME = 'people_group_name'
KEY_PEOPLE_GROUP_COLOR = 'people_group_color'
KEY_GROUP_ARRAY = 'group_arr'

# Function data in request
KEY_FUNCTION_ID = 'function_id'

# Api key data in request
KEY_API_KEY_ID = 'api_key_id'
KEY_API_KEY = 'api_key'
KEY_API_KEY_STATUS = 'status'

# People key data in request
KEY_PERSON_CODE = 'person_code'
KEY_PERSON_ID = 'person_id'

# Camera key data in request
KEY_CAMERA_NAME = 'camera_name'
KEY_CAMERA_ID = 'camera_id'
KEY_STREAM_URL = 'stream_url'

# Group people data in request
KEY_CAMERA_GROUP_ID = 'camera_group_id'
KEY_CAMERA_GROUP_CODE = 'camera_group_code'
KEY_CAMERA_GROUP_NAME = 'camera_group_name'
KEY_CAMERA_GROUP_COLOR = 'camera_group_color'
KEY_CAMERA_GROUP_ARRAY = 'group_arr'

# Process in request
KEY_PROCESS_ID = 'process_id'
KEY_PROCESS_NAME = 'process_name'
KEY_PROCESS_TOKEN = 'process_token'
KEY_PROCESS_PEOPLE_GROUP_ID = 'people_group_id'
KEY_PROCESS_CONFIG = 'process_config'
KEY_PROCESS_CAMERA_ID = 'camera_id'
KEY_PROCESS_PROJECT_ID = 'project_id'
KEY_PROCESS_STATUS = 'process_status'
DEFAULT_PROCESS_CREATE = 0
KEY_PROCESS_START = 1
KEY_PROCESS_STOP = 2
# Default value
DEFAULT_STATUS_ACTIVE = 1
DEFAULT_STATUS_DEACTIVE = 0
DEFAULT_ADMIN_ROLE = 1
DEFAULT_USER_STATUS = 1
DEFAULT_TOKEN_ACTIVE = 1
DEFAULT_TOKEN_DEACTIVE = 0
DEFAULT_TOKEN_EXPIRATION_DATE = 1
DEFAULT_MASTER_ADMIN_USER_NAME = 'admin'
DEFAULT_MASTER_ADMIN_FULL_NAME = 'Administrator'
DEFAULT_MASTER_ADMIN_PASSWORD = 'admin'
DEFAULT_WHITE_SPACE_VALUE = ' '
DEFAULT_MESSAGE_REQUIRE_LOGIN = 'Your authentication information is invalid or expired!'
