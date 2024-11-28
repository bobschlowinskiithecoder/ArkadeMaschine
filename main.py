from datetime import datetime
from os.path import isfile, join
from types import SimpleNamespace
import os
import time
import json
import subprocess
import codecs

directory = "/media/benjamin"
diskMounted = False
running = True

def log(string):
    print(f"[{datetime.now().strftime('%d.%m.%Y %H:%M:%S')}]: {string}")

def eject_drive(drive):
    try:
        subprocess.run(["eject", drive], check=True)
        log(f"drive {drive} ejected successfully")
    except subprocess.CalledProcessError as e:
        log(f"failed to eject drive {drive}: {e}")
    except FileNotFoundError:
        log("eject command not installed") 

def refreshDeviceList(d):
    items = os.listdir(d)
    if len(items) != 1:
        return 1
    return items[0]

def useDisk():
    global diskMounted
    diskMounted=True
    log("called useDisk()")
    d = refreshDeviceList(directory)
    if d == 1:
        log("o  ERROR: invalied # of disks; quitting...")
        diskMounted = False
        return
    
    log(f"|  disk found ({d}); trying to mount...")

    base = f"{directory}/{d}/"
    items = os.listdir(base)
    projs = findFileType(items=items, ext="html")

    try: 
        with open(base + 'projects.json', 'r') as file:
            projects = json.load(file, object_hook=lambda d: SimpleNamespace(**d))
    except Exception:
        log(f"o  ERROR: no projects.json found in path, quitting...")
        diskMounted = False
        return
    
    log(f"|  mounted!")
    log(f"|  found {projs} Scratch Project(s):")
    for i in range(len(projects.items)):
        log(f"|  |  name: \"{projects.items[i].name}\", description: \"{projects.items[i].description}\", path: \"{projects.items[i].path}\"")
    log("|  o")

    using = int(input(""))
    

def findFileType(items, ext):
    count = 0
    for item in range(len(items)):
        if items[item].split(".")[-1] == ext: count+=1
    return count

while running == True:
    if diskMounted == False: useDisk()
    time.sleep(5)
