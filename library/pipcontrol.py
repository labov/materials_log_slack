import os
import sys


class PipControl:
    def __init__(self, abs_path: str = "") -> None:
        self.cmd = sys.executable
        self.abs_path = abs_path
        print(abs_path)
        self.abs_dir = os.path.dirname(abs_path)
        self.pip_path = os.path.join(self.abs_dir, "pip_list.txt")
        self.requirement_path = os.path.join(self.abs_dir, "requirements.txt")
        self.venv_path = os.path.join(self.abs_dir, "venv")
        if sys.platform == "linux" or sys.platform == "linux2":
            self.cmd_venv = os.path.join(self.venv_path, "bin", "python3")
        elif sys.platform == "darwin":
            self.cmd_venv = os.path.join(self.venv_path, "bin", "python3")
        elif sys.platform == "win32":
            self.cmd_venv = os.path.join(self.venv_path, "bin", "python")

    def setup_venv(self):
        os.system(f"{self.cmd} -m pip install --user --upgrade pip")
        os.system(f"{self.cmd} -m venv {self.venv_path}")
        self.cmd = self.cmd_venv
        os.system(f"{self.cmd} -m pip install --user --upgrade pip")

    def run(self, file_name: str = ""):
        file_path = os.path.join(self.abs_dir, file_name)
        os.system(f"{self.cmd} {file_path}")

    def get_pip_list(self):
        os.system(f"{self.cmd} -m pip list >> " + self.pip_path.replace(" ", "\ "))
        os.system(f"{self.cmd} -m pip install --upgrade pip")
        with open(f"{self.pip_path}", "r", encoding="utf-8-sig") as f:
            self.pip_lines = f.readlines()
        os.remove(f"{self.pip_path}")

    def install(self, packages: list):
        self.get_pip_list()
        for package in packages:
            check_intalled = False
            for search in self.pip_lines:
                check_intalled = check_intalled or search.split(" ")[0].lower() == package.lower()
            if check_intalled is False:
                print(f"[{package}] install")
                os.system(f"{self.cmd} -m pip install {package}")
            else:
                print(f"[{package}] is installed")

    def update(self, packages: list):
        for package in packages:
            check_intalled = False
            for pip_line in self.pip_lines:
                check_intalled = check_intalled or pip_line.split(" ")[0].lower() == package.lower()
            if check_intalled is True:
                os.system(f"{self.cmd} -m pip install --upgrade {package}")

    def uninstall(self, packages: list):
        for package in packages:
            check_intalled = False
            for search in self.pip_lines:
                check_intalled = check_intalled or search.split(" ")[0].lower() == package.lower()
            if check_intalled is True:
                os.system(f"sudo {self.cmd} -m pip uninstall -y {package}")

    def requirement_install(self):
        os.system(f"{self.cmd} -m pip install -r {self.requirement_path}")

    def requirement_uninstall(self):
        os.system(f"sudo {self.cmd} -m pip uninstall -r {self.requirement_path} -y")

    def requirement_freeze(self):
        os.system(f"{self.cmd} -m pip freeze > {self.requirement_path}")


if __name__ == "__main__":
    import os

    ABS_PATH = os.path.dirname(os.path.abspath(__file__))
    pipcontrol = PipControl(ABS_PATH)

    pipcontrol.install(packages=["boto3", "urllib3", "wheel", "twine"])
    pipcontrol.update(packages=["boto3", "urllib3", "wheel", "twine"])
    # pipcontrol.uninstall(packages=["boto3", "urllib3", "wheel", "twine"])

    pipcontrol.requirement_freeze()
    # pipcontrol.requirement_install()
    # pipcontrol.requirement_uninstall()

    pipcontrol.setup_venv()
    pipcontrol.run("run.py")
