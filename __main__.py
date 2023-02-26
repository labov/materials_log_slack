import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))  # import ../ folders


from library.pipcontrol import PipControl

ABS_PATH = os.path.abspath(__file__)
PACKAGES = ["slack_sdk", "dacite"]

pip = PipControl(ABS_PATH)
pip.setup_venv()
pip.install(PACKAGES)
pip.run("run.py")
