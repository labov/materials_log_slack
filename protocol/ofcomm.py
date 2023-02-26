import os
import sys
from datetime import datetime
from dataclasses import dataclass, field
from typing import List

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))  # import ../ folders


class Comm:

    EOF = "<EOF>"

    @dataclass
    class MachineInfo:
        user_name: str = ""
        public_ip: str = ""
        local_ip: str = ""
        mac_addr: str = ""

    @dataclass
    class ServerInfo:
        ip: str = ""
        port: int = -1

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

    @dataclass
    class Action:
        key: str = ""
        cmd: str = ""

        @dataclass
        class Data:
            request_id: int = -1

            @dataclass
            class ActionItem:
                ridx: int = -1
                action: str = ""
                fidx: int = -1
                fry_count: int = -1

            items: List[ActionItem] = field(default_factory=list)

        data: Data = field(default_factory=Data)

    @dataclass
    class Time:
        key: str = ""
        cmd: str = ""

        @dataclass
        class Data:
            request_id: int = -1

            @dataclass
            class TimeItem:
                openwait_sec: float = -1.0
                closewait_sec: float = -1.0
                frying_sec: float = -1.0
                draining_sec: float = -1.0
                soaking_sec: float = -1.0

                @dataclass
                class FryingItem:
                    offset: float = -1.0
                    airing: float = -1.0

                fitems: List[FryingItem] = field(default_factory=list)

            items: List[TimeItem] = field(default_factory=list)

        data: Data = field(default_factory=Data)

    @dataclass
    class Order:
        key: str = ""
        cmd: str = "order"

        @dataclass
        class Data:
            request_id: int = -1
            oid: str = ""

            @dataclass
            class OrderItem:
                ridx: int = -1
                tray: int = -1
                batter: int = -1
                fry: int = -1

            items: List[OrderItem] = field(default_factory=list)

        data: Data = field(default_factory=Data)

    @dataclass
    class HealthCheck:
        cmd: str = "healthcheck"

        @dataclass
        class Data:
            date: datetime = datetime.min

            @dataclass
            class MachineState:
                env_host: str = ""
                version: str = ""

            machine_state: MachineState = field(default_factory=MachineState)

            @dataclass
            class RobotStatus:
                state: str = ""
                axis_x: float = -1.0
                axis_z: float = -1.0
                gripper: str = ""
                tray_count: int = -1
                batter_count: int = -1
                fry_count: int = -1
                drain_count: int = -1

                @dataclass
                class FryerStatus:
                    fidx: int = -1
                    state: str = ""
                    oid: str = ""
                    oidx: int = -1
                    start: datetime = datetime.min
                    end: datetime = datetime.min
                    frying_sec: float = 0.0
                    airing_sec: float = 0.0
                    tray_sec: float = 0.0
                    pickup_sec: float = 0.0

                fryer: List[FryerStatus] = field(default_factory=list)

            robot_states: List[RobotStatus] = field(default_factory=list)

        data: Data = field(default_factory=Data)


if __name__ == "__main__":
    print("test code")
