import os
import sys

# import socket
# import json
import logging
import time

# import boto3
# import getpass
# import re
from uuid import getnode

# import requests

from datetime import datetime
from typing import List
from slack_sdk import WebClient

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))  # import ../ folders


from protocol.protocol import Protocol


class Log:
    def __init__(self, abs_path):
        self.debug_option: bool = True
        # self.debug_option: bool = False

        self.slack = SlackContorller(self)

        dtn = datetime.now()
        self.exe_base = os.path.basename(abs_path)
        self.log_dir = os.path.join(os.path.dirname(abs_path), "log", str(dtn.year), str(dtn.month), str(dtn.day))
        os.makedirs(self.log_dir, exist_ok=True)
        self.log_base = "logs.log"
        self.slack_channel_id = "C04RA8E78BU"
        self.levels = []
        self.log_paths = []
        self.time_utcnow = datetime.now()

        self.getLogger()
        self.addHandler(level=logging.INFO, stream_flag=True)
        self.addHandler(level=logging.INFO)
        if self.debug_option:
            self.addHandler(level=logging.DEBUG, add_format="| %(filename)s | %(funcName)s | %(lineno)d")

        self.clear_widget()

    def getLogger(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.logger.setLevel(logging.INFO)

    def addHandler(self, level: int, add_format: str = "", stream_flag: bool = False):
        format_str = f"%(asctime).19s | %(levelname)-5s | %(message)s {add_format}"
        self.format = logging.Formatter(format_str)
        if stream_flag:  # log console stream
            self.handler = logging.StreamHandler(sys.stdout)
        else:  # log file
            self.log_base = f"logs_{logging.getLevelName(level)}.log"
            self.log_path = os.path.join(self.log_dir, self.log_base)
            self.handler = logging.FileHandler(self.log_path)
            self.levels.append(level)
            self.log_paths.append(self.log_path)
        self.handler.setLevel(level)
        self.handler.setFormatter(self.format)
        self.logger.addHandler(self.handler)

    def removeAllHandlers(self):
        handlers = self.logger.handlers
        for handler in handlers:
            self.logger.removeHandler(handler)

    def maintanance(self):
        return self.log_count.error > 0 or self.log_count.critical > 0

    def renaming_file(self):
        prefix = datetime.now().strftime("%Y%m%d_%H%M%S_")
        for level in self.levels:
            log_base = f"logs_{logging.getLevelName(level)}.log"
            old = os.path.join(self.log_dir, log_base)
            new = os.path.join(self.log_dir, prefix + log_base)
            os.rename(old, new)

    def calc_sec(self) -> float:
        time_delta = datetime.now() - self.time_utcnow
        time_delta_sec = time_delta.total_seconds()
        self.time_utcnow = datetime.now()
        return time_delta_sec

    def calc_sec_str(self) -> str:
        sec = self.calc_sec()
        if sec < 0.1**4:
            return f"{sec*10**6:.1f}us"
        elif sec < 0.1:
            return f"{sec*10**3:.1f}ms"
        else:
            return f"{sec:.1f}s"

    def clear_widget(self):
        self.widgets: List = []

    def add_widget(self, widget=None):
        self.widgets.append(widget)

    def log(self, level: int, msg: str, slack: bool = None):
        if slack is True or level > logging.INFO:
            bot_name = self.exe_base + "_" + logging.getLevelName(level)
            if level > logging.INFO:
                self.slack.chat_postMessage(self.slack_channel_id, msg, bot_name)
            else:
                self.slack.chat_postMessage(self.slack_channel_id, msg)
        elif slack is False:
            pass
        else:
            logging.log(logging.DEBUG, f"check Log.log slack arg : {slack}")
        if level > logging.DEBUG:
            msg = f"{msg} ({self.calc_sec_str()})"

        logging.log(level, msg)
        for widget in self.widgets:
            widget(msg)

    def critical(self, message: str, slack: bool = None):
        self.log(logging.CRITICAL, message, slack)

    def error(self, message: str, slack: bool = None):
        self.log(logging.ERROR, message, slack)

    def warning(self, message: str, slack: bool = None):
        self.log(logging.WARNING, message, slack)

    def info(self, message: str, slack: bool = None):
        self.log(logging.INFO, message, slack)

    def debug(self, message: str, slack: bool = None):
        self.log(logging.DEBUG, message, slack)

    def level_count(self):
        self.log_count = Protocol.LogCount()
        with open(os.path.join(self.log_dir, self.log_base), "r") as f:
            for line in f.readlines():
                if line[0:32].find("CRITICAL") > -1:
                    self.log_count.critical += 1
                if line[0:32].find("ERROR") > -1:
                    self.log_count.error += 1
                if line[0:32].find("WARNING") > -1:
                    self.log_count.warning += 1
                if line[0:32].find("INFO") > -1:
                    self.log_count.info += 1
                if line[0:32].find("DEBUG") > -1:
                    self.log_count.debug += 1
        return self.log_count


class SlackContorller:
    def __init__(self, log: Log):
        self.log = log
        self.set_client()

    def set_client(self, token: str = ""):
        self.bot_token = "xoxb-4671852801846-4860408327522-t4DjtzNovsvEa1S8eWb8mMON"
        if token != "":
            self.bot_token = token
        self.client = WebClient(token=self.bot_token)

    def chat_postMessage(self, channel: str, text: str, username: str = None):
        response = self.client.chat_postMessage(channel=channel, text=text, username=username, link_names=True)
        self.log.debug(response)

    def chat_postEphemeral(self, channel: str, text: str, user: str, username: str = None):
        response = self.client.chat_postEphemeral(
            channel=channel,
            user=user,
            text=text,
            username=username,
        )
        self.log.debug(response)

    def upload_file(self, file_: str, channel_: str):
        response = self.client.files_upload_v2(
            file=file_,
            channel=channel_,
            filename=os.path.basename(file_),
        )
        self.log.debug(response)

    def upload_files(self, files: List[str], channel: str):
        try:
            dicts = []
            for file_path in files:
                dict = {}
                dict["file"] = file_path
                dict["title"] = os.path.basename(file_path)
                dicts.append(dict)
            response = self.client.files_upload_v2(file_uploads=dicts, channel=channel)
            self.log.debug(response)
        except Exception as e:
            self.log.error("exception msg : " + str(e))

    def channel_list(self):
        response = self.client.conversations_list()
        self.log.debug(response)


class Materials:
    def __init__(self, abs_path):
        self.abspath: Protocol.Path = self.set_abspath(abs_path)
        self.log = Log(abs_path)
        self.slack = SlackContorller(self.log)
        # self.client = ClientHandler(self.log)
        # self.server = ServerHandler(self.log)
        # self.aws = AWS(self.log)
        # self.mongodb = MongoDB(self.log)

        # self.machin_info = Protocol.MachineInfo()
        # self.get_machine_info()
        # self.server_info = Protocol.ServerInfo()
        # self.set_server_info("192.168.219.102", 9009)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.log.renaming_file()
        self.log.removeAllHandlers()

    @staticmethod
    def set_abspath(abs_path):
        return Protocol.Path(dir=os.path.dirname(abs_path), base=os.path.basename(abs_path))

    @staticmethod
    def wait(sec: int = 1):
        time.sleep(sec)

    # def get_machine_info(self):
    #     user_name = getpass.getuser()
    #     public_ip = requests.get("https://api64.ipify.org").text
    #     with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    #         s.connect(("8.8.8.8", 80))
    #         local_ip = s.getsockname()[0]
    #     mac_addr = ":".join(re.findall("..", "%012x" % getnode()))
    #     self.machin_info = Protocol.MachineInfo(user_name, public_ip, local_ip, mac_addr)

    # def set_server_info(self, ip: str, port: int):
    #     """change 3rd number of local ip to current access local adress.
    #     eg. 192.168.219.190 => 192.168.0.190"""
    #     local_ips = Protocol.MachineInfo.local_ip.split(".")
    #     server_ips = ip.split(".")
    #     if len(local_ips) == 4 and len(server_ips) == 4 and local_ips[2] != server_ips[2]:
    #         ip = f"{local_ips[0]}.{local_ips[1]}.{local_ips[2]}.{server_ips[3]}"
    #     self.server_info = Protocol.ServerInfo(ip, port)


if __name__ == "__main__":
    pass
