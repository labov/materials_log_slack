import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))  # import ../ folders

from library.materials import Materials

ABS_PATH = os.path.abspath(__file__)
materials = Materials(ABS_PATH)

"""
# How to get slack token
go to api.slack.com
Features - OAuth & Permissions - Scopes - Add an OAuth Scope [chat:write, write.customize, ...]
Settings - Install App - Install to Workspace => get token of client

# How to add bot to channel
Add bot apps to channel (channel detail : integratons tab)
"""

materials.slack.set_client("xoxb-4671852801846-4860408327522-t4DjtzNovsvEa1S8eWb8mMON")
materials.log.slack_channel_id = "C04RA8E78BU"


materials.log.debug_option = False

materials.log.info("logger start, save to log/Y/M/D/logs_LEVEL.log")

materials.log.info("default setting explaination")
materials.log.info("console prompt shows above info level")

materials.log.debug("save 2 files info and debug")
materials.log.warning("send message to slack above warning level")
materials.log.warning("change bot name to file-name_level above warning level")

materials.log.info("can send below info level messsage using slack option", True)
materials.log.debug("upload files to slack (need to add files scope in slack api)", True)
MAIN_FILE = os.path.join(materials.abspath.dir, "__main__.py")
materials.slack.upload_files([ABS_PATH, MAIN_FILE], materials.log.slack_channel_id)

materials.log.info("renaming files to seperate logs")
materials.log.renaming_file()

materials.log.info("logger end")
materials.log.removeAllHandlers()


with Materials(ABS_PATH) as m:
    m.log.debug("__enter__, __exit__ test")
    m.log.info("__exit__ renaming and remove handler test")
