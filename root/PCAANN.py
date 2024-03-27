import os, sys, subprocess
import tkinter as tk
from tkinter import filedialog

CWD = os.path.dirname(os.path.realpath(__file__))

def exec_script(name: str):
    p = subprocess.Popen(['call', os.path.join(CWD, name)], stdout=sys.stdout, shell=True)
    p.communicate()

def build():
    exec_script("build.bat")

def run():
    exec_script("run.bat")

def stop():
    exec_script("stop.bat")

def update():
    exec_script("update.bat")

def driver(first_run=False):
    if first_run:
        os.system("cls")
    print("-----------------------------------------------------------------")
    print("Options: <start> <stop> <build> <data> <update> <exit>")
    user_input = input(":: ")
    if user_input == 'start':
        print('Starting PCAANN...')
        run()
    elif user_input == 'stop':
        print('Stopping...')
        stop()
    elif user_input == 'build':
        build()
    elif user_input == 'update':
        update()
    elif user_input == 'data':
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        if file_path.endswith('.xlsx'):
            print(f'Selected file: {file_path}')
            file_path = file_path.replace('/', '\\')
            os.system(f"copy \"{file_path}\" {os.path.join('PCA-ANN-code', 'RAW-DATA')}")
            pass
        else:
            print('Error: data must be in .xlsx format')
    elif user_input == 'exit':
        exit()
    driver()

if __name__ == "__main__":
    driver(first_run=True)
