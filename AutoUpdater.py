from datetime import datetime, timedelta
from pathlib import Path
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
            current = str(Path(__file__).resolve().parent)
            ## Download Update
            if appBuild == "Main": urllib.request.urlretrieve("https://github.com/Oszust-Industries/Achievement-Notifications-Library/archive/refs/heads/main.zip", "Achievement-Notifications-Library.zip")
            elif appBuild == "Beta": urllib.request.urlretrieve("https://github.com/Oszust-Industries/Achievement-Notifications-Library/archive/refs/heads/Beta.zip", "Achievement-Notifications-Library.zip")
            else: return
            with zipfile.ZipFile(r"./Achievement-Notifications-Library.zip", 'r') as zip_ref: zip_ref.extractall("")
            os.remove(current + "\\Achievement-Notifications-Library.zip")
            if appBuild == "Beta": os.rename(current + "\\Achievement-Notifications-Library-Beta", current + "\\Achievement-Notifications-Library-main")
            ## Files to Update
            if os.path.getsize(current + "\\Achievement_Notifications_Library.py") != os.path.getsize(current + "\\Achievement-Notifications-Library-main\\Achievement_Notifications_Library.py"): restartNeed = True
            try: os.remove(current + "\\Achievement_Notifications_Library.py")
            except: pass
            shutil.move(current + "\\Achievement-Notifications-Library-main\\Achievement_Notifications_Library.py", current)
            try: shutil.rmtree(current + "\\Achievement Icons")
            except: pass
            shutil.move(current + "\\Achievement-Notifications-Library-main\\Achievement Icons", current)
            try: os.remove(current + "\\AutoUpdater.py")
            except: pass
            shutil.move(current + "\\Achievement-Notifications-Library-main\\AutoUpdater.py", current)
            ## Clean Update
            shutil.rmtree(current + "\\Achievement-Notifications-Library-main")
            pickle.dump(datetime.utcnow(), open(current + "\\lastUpdateDate.p", "wb"))
            if restartNeed == True: return True
            else: return False
    except: print("Update Failed.")
