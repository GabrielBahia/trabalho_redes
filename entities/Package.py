import json


class Package:
    def __init__(self) -> None:
        self._sequence_number = 0
        self._body = {}

    @property
    def body(self):
        return self._body
    
    @body.setter
    def body(self, value):
        self._body = value

    @property
    def sequence_number(self):
        return self._sequence_number
    
    @sequence_number.setter
    def sequence_number(self, value):
        self._sequence_number = value

    def to_json_str(self) -> str:
        return json.dumps(self, default=lambda obj: obj.__dict__)
