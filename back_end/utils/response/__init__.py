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

DEFAULT_SUCCESS_CODE = 0
DEFAULT_ERROR_CODE = -1
DEFAULT_MESSAGE = 'No messages are provided!'
DEFAULT_SUCCESS_MESSAGE = 'Request was successfully processed!'
DEFAULT_ERROR_MESSAGE = 'The request was processed failed!'
DEFAULT_DATA = None


#  @Project FCloudConsole
#  @Homepage https://fsmartstore.com
#  @Copyright (c) 2018 Fujinet Systems JSC. All Rights Reserved.
#  @License All resources of the source code are owned by 'Fujinet Systems JSC'.
#  Intentionally infringing, stealing, exchanging, or trading in all of the
#  resources below without our consent, is a violation of intellectual property
#  rights. So, if you accidentally receive this source code, please send an email
#  to rd-support@fujinet.net, so we can find the best solution for this problem.

class Resp:

    def __init__(self, code, message, data):
        self.code = code
        self.message = message
        self.data = data

    def get_code(self):
        return self.code

    def get_message(self):
        return self.message

    def get_data(self):
        return self.data

    def to_dict(self):
        return {
            'code': self.code,
            'message': self.message,
            'data': self.data
        }

    @staticmethod
    def create(code, message, data):
        return Resp(code, message, data)

    @staticmethod
    def success(code=DEFAULT_SUCCESS_CODE, message=DEFAULT_SUCCESS_MESSAGE, data=DEFAULT_DATA):
        return Resp(code, message, data)

    @staticmethod
    def error(code=DEFAULT_ERROR_CODE, message=DEFAULT_ERROR_MESSAGE, data=DEFAULT_DATA):
        return Resp(code, message, data)
