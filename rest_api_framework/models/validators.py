class Validator(object):
    """
    Base Validator class
    Used to validate data format
    """
    def validate(self, field):
        raise NotImplemented


class IntegerValidator(Validator):

    def validate(self, field):
        if isinstance(field, int):
            return True
        return False


class StringValidator(Validator):

    def validate(self, field):
        if isinstance(field, basestring):
            return True
        return False