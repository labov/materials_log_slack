import os
import sys
from dataclasses import dataclass, field
from typing import List

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))  # import ../ folders


class General:
    @dataclass
    class Path:
        dir: str = ""
        base: str = ""

    @dataclass
    class MongoInfo:
        database: str = ""
        collection: str = ""
        address: str = (
            "mongodb+srv://fk-sales:7914IZUIFwUV4HQ0@whatacrisp.tognyo4.mongodb.net/?retryWrites=true&w=majority"
        )

    @dataclass
    class AWSData:
        file_path: str = ""
        bucket: str = ""
        object_name: str = ""

    @dataclass
    class SlackUser:
        name: str = ""
        id: str = ""

    @dataclass
    class SlackChannel:
        name: str = ""
        id: str = ""

    @dataclass
    class MailInfo:
        subject: str = "Sales report"
        html: str = ""

        @dataclass
        class Login:
            id: str = ""
            password: str = ""

        login: Login = field(default_factory=Login)
        send_tos: List[str] = field(default_factory=list)
        files: List[str] = field(default_factory=list)

        @dataclass
        class Slack:
            name: str = ""
            id: str = ""

        channels: List[Slack] = field(default_factory=list)
        maintanance: List[Slack] = field(default_factory=list)

    @dataclass
    class LogCount:
        critical: int = 0
        error: int = 0
        warning: int = 0
        info: int = 0
        debug: int = 0


if __name__ == "__main__":
    print("test code")
