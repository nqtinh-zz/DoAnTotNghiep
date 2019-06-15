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

class Result:
    # Define key
    KEY_CODE = 'code'
    KEY_MESSAGE = 'message'
    KEY_STATUS = 'status'
    KEY_DATA = 'data'

    # Define default value
    DEFAULT_SUCCESS_CODE = 0
    DEFAULT_ERROR_CODE = -1
    DEFAULT_MESSAGE = 'No messages are provided!'
    DEFAULT_SUCCESS_MESSAGE = 'The method returns success!'
    DEFAULT_FAILED_MESSAGE = 'The method returns failed!'
    DEFAULT_DATA = None

    def __init__(self, code, message, data, status):
        self.code = code
        self.message = message
        self.data = data
        self.status = status

    def get_code(self):
        return self.code

    def get_message(self):
        return self.message

    def get_data(self):
        return self.data

    def to_dict(self):
        return {
            self.__class__.KEY_CODE: self.code,
            self.__class__.KEY_MESSAGE: self.message,
            self.__class__.KEY_DATA: self.data,
            self.__class__.KEY_STATUS: self.status
        }

    def is_success(self):
        return self.status

    @staticmethod
    def create(code, message, data, status):
        return Result(code, message, data, status)

    @staticmethod
    def success(
            code=DEFAULT_SUCCESS_CODE,
            message=DEFAULT_SUCCESS_MESSAGE,
            status=True,
            data=DEFAULT_DATA
    ):
        return Result(code, message, data, status)

    @staticmethod
    def failed(
            code=DEFAULT_ERROR_CODE,
            message=DEFAULT_FAILED_MESSAGE,
            status=False,
            data=DEFAULT_DATA
    ):
        return Result(code, message, data, status)
