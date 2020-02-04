# coding: utf-8


class AppException(Exception):
    def __init__(self, field_name='', message=''):
        self.field_name = field_name
        self.message = message

    def __str__(self):
        return f'Field: {self.field_name}, Message: {self.message}'


class BodyNotFound(AppException):
    def __init__(self, field_name='', message=''):
        super().__init__(field_name, message)


class DBError(AppException):
    def __init__(self, field_name='', message=''):
        super().__init__(field_name, message)


class ParamError(AppException):
    def __init__(self, field_name='', message=''):
        super().__init__(field_name, message)
