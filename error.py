class UnexpectedError(Exception):
    def __init__(self, msg, error, loc=None, status_code=400):
        super().__init__()
        self.status_code = status_code
        self.msg = msg
        self.loc = loc
        self.type = error.__class__.__name__

    def to_dict(self):
        data = {
            'msg': self.msg,
            'loc': self.loc,
            'type': self.type
        }
        return data


class NotFound(Exception):
    def __init__(self, msg, loc=None, status_code=404):
        super().__init__()
        self.status_code = status_code
        self.msg = msg
        self.loc = loc


    def to_dict(self):
        data = {
            'msg': self.msg,
            'loc': self.loc
        }
        return data
