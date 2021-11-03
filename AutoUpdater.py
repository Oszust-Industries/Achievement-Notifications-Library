## Achievement Notifications Library v1.5.1 - Oszust Industries
## Achievement Notifications Library - AutoUpdater
from datetime import datetime
from os import path
from os import walk
from pathlib import Path
import os
import pickle
import shutil
import urllib.request
import zipfile

def update(appBuild, appVersion):
    try:
        try: lastUpdateDate = pickle.load(open(str(Path(__file__).resolve().parent) + "\\lastUpdateDate.p", "rb"))
        except: lastUpdateDate = datetime(2018, 1, 1, 1, 1, 1, 0)
        if (datetime.utcnow() - lastUpdateDate).days != 0:
            for line in urllib.request.urlopen("https://raw.githubusercontent.com/Oszust-Industries/Achievement-Notifications-Library/main/Version.txt"):
                newestVersion = "".join([s for s in line.decode("utf-8") if s.strip("\r\n")])
            if newestVersion != appVersion:
                current, appdata = str(Path(__file__).resolve().parent), os.getenv('APPDATA') + "\\Oszust Industries"
                print("Updating...")
                ## Download Update
                if path.exists(appdata) == False: os.mkdir(appdata)
                if path.exists(appdata + "\\temp") == False: os.mkdir(appdata + "\\temp")
                else:
                    shutil.rmtree(appdata + "\\temp")
                    os.mkdir(appdata + "\\temp")
                if appBuild.lower() == "main": urllib.request.urlretrieve("https://github.com/Oszust-Industries/Achievement-Notifications-Library/archive/refs/heads/main.zip", str(os.getenv('APPDATA') + "\\Oszust Industries\\temp\\Achievement-Notifications-Library.zip"))
                elif appBuild.lower() == "beta": urllib.request.urlretrieve("https://github.com/Oszust-Industries/Achievement-Notifications-Library/archive/refs/heads/Beta.zip", str(os.getenv('APPDATA') + "\\Oszust Industries\\temp\\Achievement-Notifications-Library.zip"))
                else: return False
                with zipfile.ZipFile(appdata + "\\temp\\Achievement-Notifications-Library.zip", 'r') as zip_ref: zip_ref.extractall(appdata + "\\temp")
                os.remove(appdata + "\\temp\\Achievement-Notifications-Library.zip")
                if appBuild == "Beta": os.rename(appdata + "\\temp\\Achievement-Notifications-Library-Beta", appdata + "\\temp\\Achievement-Notifications-Library-Main")
                ## Files to Update
                filenames = next(walk(current), (None, None, []))[2]
                for i in filenames:
                    try: os.remove(current + "\\" + i)
                    except: pass
                    shutil.move(appdata + "\\temp\\Achievement-Notifications-Library-Main\\" + i, current)
                try: shutil.rmtree(current + "\\Achievement Icons")
                except: pass
                shutil.move(appdata + "\\temp\\Achievement-Notifications-Library-Main\\Achievement Icons", current)
                ## Clean Update
                shutil.rmtree(appdata + "\\temp")
                pickle.dump(datetime.utcnow(), open(current + "\\lastUpdateDate.p", "wb"))
                return True
    except Exception as Argument: print("Update Failed. (" + str(Argument) + ")")
