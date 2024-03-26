import os, sys, subprocess

CWD = os.path.dirname(os.path.realpath(__file__))

def run_script(name: str):
    p = subprocess.Popen(["powershell.exe", os.path.join(CWD, name)], stdout=sys.stdout)
    p.communicate()

def build():
    run_script("build.ps1")

def run():
    run_script("run.ps1")

if __name__ == "__main__":
    build()
