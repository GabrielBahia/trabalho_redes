import json
from sys import getsizeof


class Package:
    def __init__(self, sequence_number=None, body=None) -> None:
        self.sequence_number = sequence_number
        self.body = body

    def to_json_str(self) -> str:
        return json.dumps(self, default=lambda obj: obj.__dict__)
    
    @classmethod
    def empty_package_size(cls) -> int:
        return getsizeof(str.encode(cls().to_json_str()))

    @classmethod
    def empty_package_length(cls) -> int:
        return len(cls().to_json_str())
