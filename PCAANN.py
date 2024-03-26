import os, sys, subprocess, signal

CWD = os.path.dirname(os.path.realpath(__file__))

def exec_script(name: str):
    print(os.path.join(CWD, name))
    p = subprocess.Popen(['call', os.path.join(CWD, name)], stdout=sys.stdout, shell=True)
    p.communicate()

def build():
    exec_script("build.bat")

def run():
    exec_script("run.bat")

def stop():
    exec_script("stop.bat")

def driver():
    pass

if __name__ == "__main__":
    driver()
