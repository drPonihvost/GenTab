class AlchemyError(Exception):
    status_code = 400

    def __init__(self, status_code=None, payload=None):
        super().__init__()
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload


    def to_dict(self):
        rv = [{}]
        rv[0]['msg'] = str(self.payload.orig)
        rv[0]['loc'] = ['database']
        rv[0]['type'] = str(self.payload.__class__.__name__)
        return rv
