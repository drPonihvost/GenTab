class UnexpectedError(Exception):

    def __init__(self, status_code=400):
        super().__init__()
        self.status_code = status_code

    def to_dict(self):
        data = {
            'msg': 'UnexpectedError',
            'loc': 'None',
            'type': 'UnexpectedError'
        }
        return data
