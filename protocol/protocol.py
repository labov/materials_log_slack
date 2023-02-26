import os
import sys
import json
from datetime import datetime
from dataclasses import dataclass, field, asdict
from dacite.core import from_dict

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))  # import ../ folders

from protocol.ofgeneral import General
from protocol.ofcomm import Comm


@dataclass
class Protocol(General, Comm):
    @dataclass
    class Response:
        key: str = ""
        cmd: str = ""

        @dataclass
        class Data:
            request_id: int = -1
            result: str = ""
            message: str = ""

        data: Data = field(default_factory=Data)

    @staticmethod
    def todict(class_object):
        return asdict(class_object)

    @staticmethod
    def tojson(class_object):
        return json.dumps(asdict(class_object))

    @staticmethod
    def toclass(protocol_type, data_dict: dict, type_recovery: bool = False):
        for key in data_dict.keys():
            if str(key).find("datetime") > -1 and type(data_dict[key]) == str:
                data_dict[key] = datetime.strptime(data_dict[key], "%Y-%m-%d %H:%M:%S")
            else:
                if type_recovery:
                    type_dict = Protocol.todict(protocol_type())
                    data_dict[key] = type(type_dict[key])(data_dict[key])

        return from_dict(protocol_type, data_dict)


if __name__ == "__main__":
    print("test code")
    items = Protocol.Action.Data.ActionItem(0, "grip", 0, 3)
    data = Protocol.Action.Data("id123", [items])
    action = Protocol.Action("key", "action", data)

    json_str = Protocol.tojson(action)
