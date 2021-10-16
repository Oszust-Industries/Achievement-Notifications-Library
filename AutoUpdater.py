## Achievement Notifications Library v1.5.0 - Oszust Industries
## Achievement Notifications Library - AutoUpdater
from datetime import datetime
from pathlib import Path
from os import path
import os
import pickle
import shutil
import urllib.request
import zipfile

def update(appBuild):
    try:
        try: lastUpdateDate = pickle.load(open(str(Path(__file__).resolve().parent) + "\\lastUpdateDate.p", "rb"))
        except: lastUpdateDate = datetime(2018, 1, 1, 1, 1, 1, 0)
        if (datetime.utcnow() - lastUpdateDate).days != 0:
            print("Updating...")
            current, appdata = str(Path(__file__).resolve().parent), os.getenv('APPDATA') + "\\Oszust Industries"
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
            if os.path.getsize(current + "\\Achievement_Notifications_Library.py") != os.path.getsize(appdata + "\\temp\\Achievement-Notifications-Library-Main\\Achievement_Notifications_Library.py"): restartNeed = True
            else: restartNeed = False
            try: os.remove(current + "\\Achievement_Notifications_Library.py")
            except: pass
            shutil.move(appdata + "\\temp\\Achievement-Notifications-Library-Main\\Achievement_Notifications_Library.py", current)
            try: shutil.rmtree(current + "\\Achievement Icons")
            except: pass
            shutil.move(appdata + "\\temp\\Achievement-Notifications-Library-Main\\Achievement Icons", current)
            try: os.remove(current + "\\AutoUpdater.py")
            except: pass
            shutil.move(appdata + "\\temp\\Achievement-Notifications-Library-Main\\AutoUpdater.py", current)
            ## Clean Update
            shutil.rmtree(appdata + "\\temp")
            pickle.dump(datetime.utcnow(), open(current + "\\lastUpdateDate.p", "wb"))
            if restartNeed == True: return True
    except Exception as Argument: print("Update Failed. (" + str(Argument) + ")")