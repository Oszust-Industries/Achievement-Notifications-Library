## Achievement Notifications Library v1.4.0 - Oszust Industries
dateInformation = "Created on: 5-15-21 - Last update: 8-26-21"
libraryVersion = "v1.4.0"
newestAchievementVersion = libraryVersion
import pickle
import re
import time
from datetime import datetime, date, timedelta

def libraryConfig():
## System Configures
    global bootLanguage, deactivateFileOpening, enableAccountSystem, enableAchievementThreading, exitSystem, overrideResetAchivements, resetSettings, supportedLanguages, systemName
    systemName = "Achievement Notifications Library"
    supportedLanguages = ["english"]
    exitSystem = False
## Change Configures
    resetSettings = False
    bootLanguage = "english"
    ## V|WARNING|: No Playtime/Achievements Saved
    overrideResetAchivements = False
    enableAchievementThreading = True
    deactivateFileOpening = False
    enableAccountSystem = True

def librarySetup():
## Setup Software
    clear()
    print("Achievement Notifications Library " + libraryVersion + " - Oszust Industries"
            "\n" + dateInformation + "\nLibrary Version: " + libraryVersion + "\n\n")
    libraryConfig()
    accountLogin("setup")
    if exitSystem == False:
        Achievements("setup")
        testAchievements()

def accountLogin(accountAction):
## Save User Settings
    import os
    import shutil
    from random import randint, randrange
    import math
    global account2Way, accountEmail, accountInput, accountLanguage, accountOwnedDLC, accountPassword, achievementsActivated, availableAccounts, currentAccountInfoPath, currentAccountPath, currentAccountUsername, deactivateFileOpening, emailCode, emailExpireTime, emailconfirmed, enableAccountSystem, exitSystem, expiredCodes, lockDateTime, packedAccountGames, packedAccountInformation, packedSettings, passwordAttemptsLeft, resetAchievements, tempAvailableAccounts
    weakPasswords = ["1234", "password", "forgot password", "forgotpassword", "default", "incorrect", "back", "quit", "return", "logout"]
    badUsernames = ["disneyhockey40", "guest", "default", ""]
    if accountAction == "setup":
        lockDateTime = ""
        expiredCodes = []
        emailconfirmed = 1
        passwordAttemptsLeft = 5
        accountLanguage = bootLanguage
        currentAccountUsername = ""
        accountLogin("createUserPath")
## Windows Detector
        if os.name != "nt": deactivateFileOpening = True
## Read Available Accounts
        if deactivateFileOpening == False:
            try:
                availableAccounts = pickle.load(open(str(os.getenv('APPDATA') + "\\Oszust Industries\\Available Account.p"), "rb"))
                availableAccounts.sort()
            except OSError: availableAccounts = []
        else:
            availableAccounts = []
            enableAccountSystem = False
        if enableAccountSystem == False:
            currentAccountUsername = "Default"
            currentAccountInfoPath = str(os.getenv('APPDATA') + "\\Oszust Industries\\Accounts\\" + currentAccountUsername)
            currentAccountPath = (currentAccountInfoPath + "\\" + systemName)
            try: packedAccountGames = pickle.load(open(currentAccountInfoPath + "\\accountGames.p", "rb"))
            except OSError: accountLogin("createUserPath")
            accountLogin("readSettings")
            clear()
            return
        tempAvailableAccounts = availableAccounts
        if "Default" in availableAccounts:
            tempAvailableAccounts = tempAvailableAccounts.remove("Default")
            if len(availableAccounts) <= 1: tempAvailableAccounts = []
        if len(tempAvailableAccounts) > 0:
            print("Available Accounts:")
            for i in tempAvailableAccounts:
                if i != "Default": print(str(tempAvailableAccounts.index(i) + 1) + ". " + i)
        else: print("No Available Accounts:")
        print("\n" + str(len(tempAvailableAccounts) + 1) + ". Add account")
        print(str(len(tempAvailableAccounts) + 2) + ". Login as guest")
        if len(tempAvailableAccounts) > 0: print(str(len(tempAvailableAccounts) + 3) + ". Remove account")
        if len(tempAvailableAccounts) > 0: print(str(len(tempAvailableAccounts) + 4) + ". Quit")
        else: print(str(len(tempAvailableAccounts) + 3) + ". Quit")
        accountInput = input("\nType the account number to login. ")
        if accountInput.isnumeric() or accountInput in availableAccounts:
            if accountInput == str(len(tempAvailableAccounts) + 1):
                clear()
                accountLogin("createAccount_1")
            elif accountInput == str(len(tempAvailableAccounts) + 2):
                clear()
                deactivateFileOpening = True
                achievementsActivated = False
                currentAccountUsername = "Guest"
            elif accountInput == str(len(tempAvailableAccounts) + 3) and len(tempAvailableAccounts) > 0:
                clear()
                accountLogin("deleteAccount")
            elif accountInput == str(len(tempAvailableAccounts) + 3) and len(tempAvailableAccounts) <= 0:
                    accountLogin("quit")
            elif accountInput == str(len(tempAvailableAccounts) + 4) and len(tempAvailableAccounts) > 0:
                    accountLogin("quit")
            elif (accountInput < str(len(tempAvailableAccounts) + 1) and int(accountInput) > 0) or accountInput in availableAccounts:
                if accountInput.isnumeric(): currentAccountUsername = availableAccounts[int(accountInput) - 1]
                else: currentAccountUsername = accountInput
                currentAccountInfoPath = str(os.getenv('APPDATA') + "\\Oszust Industries\\Accounts\\" + currentAccountUsername)
                currentAccountPath = (currentAccountInfoPath + "\\" + systemName)
                accountLogin("readSettings")
            else:
                clear()
                print("You typed an unavailable account number.\n\n\n")
                accountLogin("setup")
        else:
            clear()
            print("You typed an unavailable account number.\n\n\n")
            accountLogin("setup")
## Account Logout
    elif accountAction == "logout":
        if exitSystem == False:
            exitSystem = True
            print(interfaceTranslation("string_save_logout"))
        if currentAccountUsername != "":
            Achievements("saving")
            if len(waitingAchievementsList) <= 0: librarySetup()
            else:
                time.sleep(0.3)
                accountLogin("logout")
## Account Logout
    elif accountAction == "quit":
        print(interfaceTranslation("string_save_exit"))
        exitSystem = True
        if currentAccountUsername != "": Achievements("saving")
## Email
    elif "emailAccount" in accountAction:
        if deactivateFileOpening == False:
            print("Loading verification system...")
            emailMessage = str(accountAction.replace("emailAccount_", ""))
            import smtplib
            import ssl
            oo7 = pickle.load(open(str(os.getenv('APPDATA') + "\\Oszust Industries\\Data.p"), "rb"))
            port = 587
            smtp_server = "smtp.gmail.com"
            sender_email = "noreply.oszustindustries@gmail.com"
            receiver_email = accountEmail
            emailExpireTime = datetime.now() + timedelta(minutes=5)
            if emailMessage == "resetPasswordCode":
                message = """\
                Subject: Manage Password Code

                \nBelow is the code to manage the password for your Oszust Industries account:\n\n""" + str(emailCode) + "\n\nThis code expires in 5 minutes.\n\n\nOszust Industries (no-reply)"""
            elif emailMessage == "verificationCode":
                message = """\
                Subject: Verification Code

                \nBelow is the code to login into your Oszust Industries account:\n\n""" + str(account2Way) + "\n\nThis code expires in 5 minutes.\n\n\nOszust Industries (no-reply))"""
            context = ssl.create_default_context()
            with smtplib.SMTP(smtp_server, port) as server:
                server.ehlo()
                server.starttls(context=context)
                server.ehlo()
                server.login(sender_email, oo7)
                server.sendmail(sender_email, receiver_email, message)
## Create Account
    elif "createAccount" in accountAction:
        createAccountStep = int(accountAction.replace("createAccount_", ""))
        if createAccountStep == 1:
            if currentAccountUsername == "": print("Create Account:\n\nType 'back' to return to the previous prompt.\nType 'cancel' to cancel create account.")
            currentAccountUsername = input(str("\n\n\nA username is your name that you will select when logging into the server.\n\nWhat username would you like for your account? "))
            if currentAccountUsername.lower() in ["cancel", "quit", "exit", "back", "return"]: librarySetup()
            elif currentAccountUsername not in availableAccounts:
                if currentAccountUsername.lower() not in badUsernames: accountLogin("createAccount_2")
                else:
                    print("\nThis username is unavailable.")
                    accountLogin("createAccount_1")
            else:
                print("\nThis username is already in use.")
                accountLogin("createAccount_1")
        elif createAccountStep == 2:
            accountPassword = ""
            accountLanguage = input(str("\n\n\n\nThis is the language that all text will be shown in.\n\nWhat language would you like to use? " + str(supportedLanguages) + " "))
            if accountLanguage.lower() == "en": accountLanguage = "english"
            if accountLanguage.lower() in ["cancel", "quit", "exit"]: librarySetup()
            elif accountLanguage.lower() in ["back", "return"]:
                currentAccountUsername = ""
                accountLogin("createAccount_1")
            elif accountLanguage.lower() not in supportedLanguages:
                print("\nThis is not a supported language. We support: " + str(supportedLanguages))
                accountLogin("createAccount_2")
            else: accountLogin("createAccount_3")
        elif createAccountStep == 3:
            accountEmail = input(str("\n\n\n\nAn email is required strictly for when you forget your password or a verification code needs to be sent.\n\nWhat email would you like to use for your account? "))
            if accountEmail.lower() in ["cancel", "quit", "exit"]: librarySetup()
            elif accountEmail.lower() in ["back", "return"]: accountLogin("createAccount_2")
            elif "@" in accountEmail and "." in accountEmail: accountLogin("createAccount_4")
            else:
                print("\nThis email is not a valid email.")
                accountLogin("createAccount_3")
        elif createAccountStep == 4:
            if accountPassword == "": accountInput = input(str("\n\n\n\nA password will add more security to your account. The password will be required whenever an account action needs to take place.\n\nWould you like a password on your account? (yes/no) "))
            else: accountInput = "yes"
            if accountInput.lower() in ["cancel", "quit", "exit"]: librarySetup()
            elif accountInput.lower() in ["back", "return"]: accountLogin("createAccount_3")
            elif accountInput.lower() in ["y", "yes"]:
                accountLogin("createAccount_5")
            elif accountInput.lower() in ["n", "no"]:
                accountPassword = "none"
                accountLogin("createAccount_6")
            else:
                print("\nPlease type yes or no.")
                accountLogin("createAccount_4")
        elif createAccountStep == 5:
            accountPassword = input(str("\nWhat password would you like for your account? "))
            if accountPassword.lower() in ["cancel", "quit", "exit"]: librarySetup()
            elif accountPassword.lower() in ["back", "return"]:
                accountPassword = ""
                accountLogin("createAccount_4")
            elif len(accountPassword) < 5:
                print("\n\n\nYour password needs to be at least five characters long.")
                accountLogin("createAccount_5")
            elif accountPassword.lower() in weakPasswords:
                print("\n\n\nYour password is too weak. Create a more unique password.")
                accountLogin("createAccount_5")
            else: accountLogin("createAccount_6")
        elif createAccountStep == 6:
            if accountPassword == "": print("\n\n\n\n2 factor verification will add more security to your account. This will be used whenever an account action needs to take place.")
            elif accountPassword != "": print("\n\n\n\n2 factor verification will add even more security to your account. This will be used with your password whenever an account action needs to take place.")
            accountInput = input(str("\n2 factor verification will email you a code to type in when it is required.\n\nWould you like 2 factor verification on your account? (yes/no) "))
            if accountInput.lower() in ["cancel", "quit", "exit"]: librarySetup()
            elif accountInput.lower() in ["back", "return"]:
                accountPassword = ""
                accountLogin("createAccount_4")
            elif accountInput.lower() in ["y", "yes"]:
                account2Way = "active"
                accountLogin("createAccount_7")
            elif accountInput.lower() in ["n", "no"]:
                account2Way = "none"
                accountLogin("createAccount_7")
            else:
                print("\nPlease type yes or no.")
                accountLogin("createAccount_6")
        elif createAccountStep == 7:
            print("\n\n\n\n\n" + ("-" * 50) + "\nAccount Confirmation:" + "\n\n\nAccount username: " + currentAccountUsername + "\nAccount language: " + accountLanguage + "\nAccount email: " + accountEmail)
            if accountPassword != "none": print("Account password: Active")
            else: print("Account password: Inactive")
            if account2Way != "none": print("Account 2 factor verification: Active")
            else: print("Account 2 factor verification: Inactive")
            accountInput = input(str("\nDo these account details look right? (yes/no) "))
            if accountInput.lower() in ["back", "return"]: accountLogin("createAccount_6")
            elif accountInput.lower() in ["y", "yes"]:
                availableAccounts.append(currentAccountUsername)
                pickle.dump(availableAccounts, open(str(os.getenv('APPDATA') + "\\Oszust Industries\\Available Account.p"), "wb"))
                packedAccountInformation = [currentAccountUsername, accountLanguage, accountEmail, accountPassword, account2Way, lockDateTime]
                clear()
                accountLogin("createUserPath")
            elif accountInput.lower() in ["n", "no"]:
                clear()
                accountLogin("createAccount_1")
            else:
                print("\nPlease type yes or no.")
                accountLogin("createAccount_7")
        return
## Create Account Path
    elif accountAction == "createUserPath":
        if deactivateFileOpening == False:
            if currentAccountUsername != "": print("\n\nCreating Account...")
            try: filePathTest = pickle.load(open(str(os.getenv('APPDATA') + "\\Oszust Industries\\Available Account.p"), "rb"))
            except OSError:
                try:
                    os.mkdir(str(os.getenv('APPDATA') + "\\Oszust Industries"))
                    pickle.dump([], open(str(os.getenv('APPDATA') + "\\Oszust Industries\\Available Account.p"), "wb"))
                    pickle.dump("D/~RQuY(1c?BS)Iau*W7", open(str(os.getenv('APPDATA') + "\\Oszust Industries\\Data.p"), "wb"))
                    os.mkdir(str(os.getenv('APPDATA') + "\\Oszust Industries\\Accounts"))
                except OSError:
                    shutil.rmtree(str(os.getenv('APPDATA') + "\\Oszust Industries"))
                    accountLogin("createUserPath")
            if currentAccountUsername != "":
                try:
                    currentAccountInfoPath = str(os.getenv('APPDATA') + "\\Oszust Industries\\Accounts\\" + currentAccountUsername)
                    os.mkdir(currentAccountInfoPath)
                except OSError: pass
                try:
                    currentAccountPath = str(currentAccountInfoPath + "\\" + systemName)
                    os.mkdir(currentAccountPath)
                except OSError: pass
                if currentAccountUsername.lower() == "default": packedAccountInformation = ["Default", bootLanguage, "Default", "none", "none", lockDateTime]
                pickle.dump(packedAccountInformation, open(currentAccountInfoPath + "\\accountInformation.p", "wb"))
                clear()
        if currentAccountUsername != "":
            accountLogin("readSettings")
## Find Account Games
    elif accountAction == "accountGames":
        if deactivateFileOpening == False:
            try: packedAccountGames = pickle.load(open(currentAccountInfoPath + "\\accountGames.p", "rb"))
            except OSError: packedAccountGames = []
            if systemName not in packedAccountGames:
                try:
                    currentAccountPath = str(currentAccountInfoPath + "\\" + systemName)
                    os.mkdir(currentAccountPath)
                except OSError: pass
                packedAccountGames.append(systemName)
            pickle.dump(packedAccountGames, open(currentAccountInfoPath + "\\accountGames.p", "wb"))
## Delete Account
    elif accountAction == "deleteAccount":
        if currentAccountUsername == "":
            print("Delete Account:")
            for i in availableAccounts:
                if i != "Default": print(str(availableAccounts.index(i) + 1) + ". " + i)
            accountInput = input("\nType the account number to delete the account. ")
            if (accountInput < str(len(tempAvailableAccounts) + 1) and int(accountInput) > 0) or accountInput in availableAccounts:
                if accountInput.isnumeric(): currentAccountUsername = availableAccounts[int(accountInput) - 1]
                else: currentAccountUsername = accountInput
                currentAccountPath = str(os.getenv('APPDATA') + "\\Oszust Industries\\Accounts\\" + currentAccountUsername + "\\" + systemName)
                accountLogin("deleteAccount")
            else:
                clear()
                print("You typed an unavailable account number.\n\n\n")
                accountLogin("deleteAccount")
        else:
            accountLogin("readSettings")
            accountInput = input("\nAre you sure you would like to permanently delete " + currentAccountUsername + "'s account from all your games? ")
            if accountInput.lower() in ["y", "yes"]: accountLogin("deleteAccountForever")
            elif accountInput.lower() in ["n", "no"]:
                clear()
                currentAccountUsername = ""
                accountLogin("setup")
            else:
                print("\nPlease type yes or no.\n\n\n")
                accountLogin("deleteAccount")
## Delete Account Forever
    elif accountAction == "deleteAccountForever":
        print("Deleting Account...")
        shutil.rmtree(str(os.getenv('APPDATA') + "\\Oszust Industries\\Accounts\\" + currentAccountUsername))
        if currentAccountUsername.lower() != "default": availableAccounts.remove(currentAccountUsername)
        pickle.dump(availableAccounts, open(str(os.getenv('APPDATA') + "\\Oszust Industries\\Available Account.p"), "wb"))
        clear()
        currentAccountUsername = ""
        print("The account has been deleted.\n\n\n")
        accountLogin("setup")
        return
## Rename Account
    elif accountAction == "renameAccount":
        print("Rename Account:")
        newAccountUsername = input(str("\nWhat would you like to rename " + currentAccountUsername + "'s account to? "))
        if newAccountUsername not in availableAccounts:
            if newAccountUsername.lower() not in badUsernames:
                availableAccounts.remove(currentAccountUsername)
                availableAccounts.append(newAccountUsername)
                pickle.dump(availableAccounts, open(str(os.getenv('APPDATA') + "\\Oszust Industries\\Available Account.p"), "wb"))
                currentAccountUsername = newAccountUsername
                packedAccountInformation = [currentAccountUsername, accountLanguage, accountEmail, accountPassword, account2Way, lockDateTime]
                clear()
                accountLogin("createUserPath")
            else:
                print("This username is unavailable.\n\n\n")
                accountLogin("renameAccount")
        else:
            print("This username is already in use.\n\n\n")
            accountLogin("renameAccount")
## Change Password
    elif accountAction == "changeAccountPassword":
        if emailconfirmed == 0:
            clear()
            print("Change Account Password:")
        if accountPassword == "none":
            print("1.Add password")
            accountInput = input(str("\nType the number of the action for " + currentAccountUsername + "'s password: "))
            if accountInput == "1":
                accountPassword = input(str("\nWhat password would you like for your account? "))
                pickle.dump([currentAccountUsername, accountLanguage, accountEmail, accountPassword, account2Way, lockDateTime], open(currentAccountInfoPath + "\\accountInformation.p", "wb"))
                print("\n\nThe password has been added to your account.")
            else:
                clear()
                print("Please type one of the following actions.\n\n\n")
                accountLogin("changeAccountPassword")
        else:
            if emailconfirmed == 1:
                accountInput = input(str("\nType your email to confirm your identity: "))
                emailconfirmed = 2
            if emailconfirmed == 2:
                if accountInput == accountEmail:
                    emailCode = randrange(100000, 999999)
                    accountLogin("emailAccount_resetPasswordCode")
                    accountInput = input(str("\nA code has been sent to your email to manage your password. Type the code here: "))
                else:
                    clear()
                    print("\n\nEmail doesn't match account's email.\n\n\n")
                    accountLogin("setup")
            if emailconfirmed == 3 or (accountInput == str(emailCode) and datetime.now() < emailExpireTime):
                emailconfirmed = 3
                print("\n\n1.Change password\n2.Remove password")
                accountInput = input(str("\nType the number of the action for " + currentAccountUsername + "'s password: "))
                if accountInput == "1":
                    accountPassword = input(str("\nWhat new password would you like for your account? "))
                    if len(accountPassword) < 5:
                        print("Your password needs to be at least five characters long.")
                        accountLogin("changeAccountPassword")
                    elif accountPassword.lower() in weakPasswords:
                        print("Your password is too weak. Create a more unique password.")
                        accountLogin("changeAccountPassword")
                    else:
                        pickle.dump([currentAccountUsername, accountLanguage, accountEmail, accountPassword, account2Way], open(currentAccountInfoPath + "\\accountInformation.p", "wb"))
                        print("\n\nThe password has been changed on your account.")
                        clear()
                        accountLogin("setup")
                elif accountInput == "2":
                    pickle.dump([currentAccountUsername, accountLanguage, accountEmail, "none", account2Way], open(currentAccountInfoPath + "\\accountInformation.p", "wb"))
                    print("\n\nThe password has been removed from your account.")
                    clear()
                    accountLogin("readSettings")
                else:
                    clear()
                    print("Please type one of the following actions.\n\n\n")
                    accountLogin("changeAccountPassword")
            elif (accountInput == str(emailCode) and datetime.now() >= emailExpireTime) or int(accountInput) in expiredCodes:
                print("\n\nThis code has expired. A new code has been sent to your email.")
                expiredCodes = expiredCodes.append(account2Way)
                emailCode = randrange(100000, 999999)
                accountLogin("changeAccountPassword")
            else:
                clear()
                print("\n\nIncorrect verification code.\n\n\n")
                accountLogin("setup")
## Read Game Settings
    elif accountAction == "readSettings":
        print("\n\nLoading Account...")
        currentAccountInfoPath = str(os.getenv('APPDATA') + "\\Oszust Industries\\Accounts\\" + currentAccountUsername)
        currentAccountPath = (currentAccountInfoPath + "\\" + systemName)
        accountLogin("accountGames")
        if deactivateFileOpening == False:
            try: packedAccountInformation = pickle.load(open(currentAccountInfoPath + "\\accountInformation.p", "rb"))
            except OSError: packedAccountInformation = ["N/A"]
            if resetSettings == True: packedSettings = [True, False]
            else:
                try: packedSettings = pickle.load(open(currentAccountPath + "\\settingsSave.p", "rb"))
                except OSError: packedSettings = [True, False]
        else:
            packedAccountInformation = ["N/A"]
            packedSettings = [True, False]
        if "N/A" not in packedAccountInformation:
            currentAccountUsername = packedAccountInformation[0]
            accountLanguage = packedAccountInformation[1]
            accountEmail = packedAccountInformation[2]
            accountPassword = packedAccountInformation[3]
            account2Way = packedAccountInformation[4]
            lockDateTime = packedAccountInformation[5]
        elif deactivateFileOpening == False: accountLogin("corruptAccount")
        elif deactivateFileOpening == True:
            accountPassword = "none"
            account2Way = "none"
        if lockDateTime != "" and datetime.now() < lockDateTime:
            clear()
            timeLeftInLock = int(math.ceil((lockDateTime - datetime.now()).seconds / 60))
            if timeLeftInLock <= 1: print("This account is still locked for " + str(timeLeftInLock) + " more minute.\n\n\n")
            else: print("This account is still locked for " + str(timeLeftInLock) + " more minutes.\n\n\n")
            accountLogin("setup")
            return
        if accountPassword == "none" and account2Way == "none": clear()
        if passwordAttemptsLeft <= 0:
            clear()
            print("\n\nIncorrect password.\nThe account has been locked for 5 minute.\n\n\n")
            lockDateTime = datetime.now() + timedelta(minutes=5)
            pickle.dump([currentAccountUsername, accountLanguage, accountEmail, accountPassword, account2Way, lockDateTime], open(currentAccountInfoPath + "\\accountInformation.p", "wb"))
            accountLogin("setup")
            return
        if accountPassword != "none":
            accountInput = input(str("\n\n\nType 'forgot password' if you have forgotten your password.\n\nThis account has a password. What is your account password? "))
            if accountInput.lower() == "forgot password": accountLogin("changeAccountPassword")
            elif accountInput == accountPassword: clear()
            elif accountInput.lower() in ["back", "quit", "return", "logout"]:
                librarySetup()
                return
            else:
                clear()
                print("\n\nIncorrect password.\n\n\n")
                passwordAttemptsLeft -= 1
                accountLogin("readSettings")
        if deactivateFileOpening == False and account2Way != "none":
            import socket
            try:
                sock = socket.create_connection(("www.google.com", 80))
                if sock is not None:
                    sock.close
                    pass
            except OSError: account2Way = "unavailable"
        if account2Way not in ["none", "unavailable"]:
            account2Way = randrange(100000, 999999)
            accountLogin("emailAccount_verificationCode")
            accountInput = input(str("\nThis account has 2 factor verification enabled. An email has been sent with the code. Type the code here: "))
            if accountInput == str(account2Way) and datetime.now() < emailExpireTime:
                if accountPassword == "none": clear()
            elif accountInput.lower() in ["back", "quit", "return", "logout"]:
                librarySetup()
                return
            elif (accountInput == str(account2Way) and datetime.now() >= emailExpireTime) or int(accountInput) in expiredCodes:
                clear()
                print("\n\nThis code has expired. A new code has been sent to your email.")
                expiredCodes.append(account2Way)
                accountLogin("readSettings")
            else:
                clear()
                print("\n\nIncorrect verification code.\nThe account has been locked for 1 minute.\n\n\n")
                lockDateTime = datetime.now() + timedelta(minutes=1)
                pickle.dump([currentAccountUsername, accountLanguage, accountEmail, accountPassword, account2Way, lockDateTime], open(currentAccountInfoPath + "\\accountInformation.p", "wb"))
                accountLogin("setup")
        elif account2Way == "unavailable":
            clear()
            print("This account has 2 factor verification enabled. We are unable to securely send a code. Please try again in a little bit.\n\n\n")
            accountLogin("setup")
        if len(packedSettings) >= 1: achievementsActivated = packedSettings[0]
        else: achievementsActivated = True
        if len(packedSettings) >= 2: resetAchievements = packedSettings[1]
        else: achievementsActivated = False
        accountLogin("saveSettings")
        accountLogin("readOwnedDLC")
## Save Settings
    elif accountAction == "saveSettings":
        if deactivateFileOpening == False:
            packedSettings = [achievementsActivated, resetAchievements]
            pickle.dump(packedSettings, open(currentAccountPath + "\\settingsSave.p", "wb"))
## Corrupt Account
    elif accountAction == "corruptAccount":
        print("\n\nAccount is unreadable.")
        accountInput = input(str("\nWould you like to delete this account? "))
        if accountInput.lower() in ["y", "yes"]: accountLogin("deleteAccountForever")
        elif accountInput.lower() in ["n", "no"]:
            clear()
            librarySetup()
        else: accountLogin("corruptAccount")
## Read Owned DLC
    elif accountAction == "readOwnedDLC":
        freeGameDLC = []
        accountActiveOwnedDLC = []
        if deactivateFileOpening == False:
            try: accountOwnedDLC = pickle.load(open(currentAccountPath + "\\accountOwnedDLC.p", "rb"))
            except OSError:
                accountOwnedDLC = [currentAccountUsername]
                pickle.dump(accountOwnedDLC, open(currentAccountPath + "\\accountOwnedDLC.p", "wb"))
            if accountOwnedDLC[0] != currentAccountUsername: accountLogin("corruptAccount")
            for i in freeGameDLC:
                if i not in accountOwnedDLC:
                    accountOwnedDLC.extend((i, "enable"))
            for i in accountOwnedDLC:
                if accountOwnedDLC.index(i) < (len(accountOwnedDLC) - 1) and accountOwnedDLC[accountOwnedDLC.index(i) + 1] == "enable":
                    accountActiveOwnedDLC.append(i)
            pickle.dump(accountOwnedDLC, open(currentAccountPath + "\\accountOwnedDLC.p", "wb"))
        else: accountActiveOwnedDLC = freeGameDLC

def interfaceTranslation(currentString):
    if currentString == "string_debug_command_fail":
        if accountLanguage.lower() == "english": return "Debug command not accepted."
    elif currentString == "string_save_exit":
        if accountLanguage.lower() == "english": return "\n\n\nDo not close application.\nSaving and exiting...\n"
    elif currentString == "string_save_logout":
        if accountLanguage.lower() == "english": return "\n\n\nDo not close application.\nSaving and logging out...\n"
    elif currentString == "string_reset_achievements_message":
        if accountLanguage.lower() == "english": return "Loading 1/2: (Resetting achievements - " + newestAchievementVersion + ")..."
    elif currentString == "string_stats_command":
        if accountLanguage.lower() == "english": return "Current achievements: " + str(gained_Achievements) + "\nCurrent achievement progress: " + str(achievementProgressTracker)
    elif currentString == "string_stats_command_fail":
        if accountLanguage.lower() == "english": return "Either achievements are disabled or file opening is disabled."
    elif currentString == "string_Achievement_Welcome_title":
        if accountLanguage.lower() == "english": return "Bronze - Welcome to the Game - 1"
    elif currentString == "string_Achievement_Welcome_description":
        if accountLanguage.lower() == "english": return "Start a new game. - 1"
    elif currentString == "string_blank":
        if accountLanguage.lower() == "english": return ""

def clear():
## Clear Output
    print("\n" * 70)

def waitingAchievements():
## Threading - Waiting Achievements
    global waitingAchievementsList
    while True:
        if len(waitingAchievementsList) > 0 and toaster.notification_active() == False:
            Achievements(waitingAchievementsList[0])
            waitingAchievementsList.remove(str(waitingAchievementsList[0]))
        elif exitSystem == True and len(waitingAchievementsList) == 0: return
        else: time.sleep(0.3)

def Achievements(achievementToGain):
## Achievement System
    global achievementProgressTracker, achievementVersion, availableAchievements, bronzeIcon, currentPlaytime, earnedBronze, earnedGold, earnedPlatinum, earnedSilver, gained_Achievements, goldIcon, lastPlaytimeDatePlayed, platinumIcon, playtimeStartTime, resetAchievements, silverIcon, toaster, waitingAchievementsList
    availableAchievements = 5
    defaultAchievementProgressTracker = [0, 10, 0, 5]
## Last Play Date
    if exitSystem == True: lastPlaytimeDatePlayed = date.today().strftime("%m/%d/%y")
    else: lastPlaytimeDatePlayed = "Currently In-game"
## Reset Achievements
    if achievementToGain == "reset":
        print(interfaceTranslation("string_reset_achievements_message"))
        achievementProgressTracker = defaultAchievementProgressTracker
        if newestAchievementVersion not in ["v1.0.0", "v1.1.0", "v1.2.0"]: gained_Achievements = [newestAchievementVersion, lastPlaytimeDatePlayed, currentPlaytime, availableAchievements, 0, 0, 0, 0,]
        elif newestAchievementVersion not in ["v1.0.0"]: gained_Achievements = [availableAchievements, 0, 0, 0, 0,]
        else: gained_Achievements = []
        if deactivateFileOpening == False:
            pickle.dump(achievementProgressTracker, open(currentAccountPath + "\\achievementProgressTracker.p", "wb"))
            pickle.dump(gained_Achievements, open(currentAccountPath + "\\achievementSave.p", "wb"))
        resetAchievements = False
        accountLogin("saveSettings")
        return
## Setup System
    elif achievementToGain == "setup":
        if deactivateFileOpening == False:
            bronzeIcon = r"./Achievement Icons/ps5-bronze-trophy.ico"
            silverIcon = r"./Achievement Icons/ps5-silver-trophy.ico"
            goldIcon = r"./Achievement Icons/ps5-gold-trophy.ico"
            platinumIcon = r"./Achievement Icons/ps5-platinum-trophy.ico"
        if enableAchievementThreading == True:
            import threading
            backroundAchievementThread = threading.Thread(name='waitingAchievements', target=waitingAchievements)
            backroundAchievementThread.start()
            waitingAchievementsList = []
        if deactivateFileOpening == False:
            try:
                gained_Achievements = pickle.load(open(currentAccountPath + "\\achievementSave.p", "rb"))
                if len(gained_Achievements) > 0: currentPlaytime = gained_Achievements[2]
                else: currentPlaytime = "0"
            except OSError:
                resetAchievements = True
                currentPlaytime = "0"
        else: currentPlaytime = "0"
## Remove User Achievements
        if deactivateFileOpening == False and (overrideResetAchivements == True or resetAchievements == True) and achievementsActivated == True: Achievements("reset")
        elif deactivateFileOpening == True and achievementsActivated == True: Achievements("reset")
## Load Achievement System
        if deactivateFileOpening == False and achievementsActivated == True:
            from win10toast import ToastNotifier
            toaster = ToastNotifier()
            try: gained_Achievements = pickle.load(open(currentAccountPath + "\\achievementSave.p", "rb"))
            except OSError: Achievements("reset")
        else: toaster = ""
## Load Achievement Progress System
        if (deactivateFileOpening == False and achievementsActivated == True) and (overrideResetAchivements == False and resetAchievements == False):
            try: achievementProgressTracker = pickle.load(open(currentAccountPath + "\\achievementProgressTracker.p", "rb"))
            except OSError: achievementProgressTracker = defaultAchievementProgressTracker
        else: achievementProgressTracker = defaultAchievementProgressTracker
## Compatibility Versions
        if deactivateFileOpening == False and achievementsActivated == True:
            pickle.dump(achievementProgressTracker, open(currentAccountPath + "\\achievementProgressTracker.p", "wb"))
            if len(gained_Achievements) > 0:
                achievementVersion = gained_Achievements[0]
                if ("v1" not in str(achievementVersion)) and (len(gained_Achievements) >= 7) and ("Achievement" not in str(gained_Achievements[6])): achievementVersion = "v1.2.0"
                elif str(achievementVersion) == "0" or str(achievementVersion) == str(availableAchievements): achievementVersion = "v1.1.0"
                elif "v1" not in str(achievementVersion): achievementVersion = "v1.0.0"
            else: achievementVersion = "v1.0.0"
            if achievementVersion not in ["v1.0.0", "v1.1.0", "v1.2.0"]:
                playtimeStartTime = datetime.now()
                currentPlaytime = float(gained_Achievements[2])
                earnedBronze = int(gained_Achievements[4])
                earnedSilver = int(gained_Achievements[5])
                earnedGold = int(gained_Achievements[6])
                earnedPlatinum = int(gained_Achievements[7])
            elif achievementVersion not in ["v1.0.0"]:
                earnedBronze = int(gained_Achievements[1])
                earnedSilver = int(gained_Achievements[2])
                earnedGold = int(gained_Achievements[3])
                earnedPlatinum = int(gained_Achievements[4])
        elif achievementsActivated == True:
            achievementVersion = newestAchievementVersion
            toaster = ""
        Achievements("saving")
        if achievementsActivated == True:
            print("Current Achievements: " + str(gained_Achievements))
            print("Current Version: " + achievementVersion)
## System Achievements
    if toaster != "" and toaster.notification_active() and enableAchievementThreading == True:
        waitingAchievementsList.append(str(achievementToGain))
        return
    if deactivateFileOpening == False and achievementsActivated == True and achievementToGain not in ["reset", "setup", "ready"] and "Progress" not in achievementToGain and achievementToGain not in gained_Achievements:
        if achievementToGain == "Achievement_Welcome":
            toaster.show_toast(interfaceTranslation("string_Achievement_Welcome_title"), str(interfaceTranslation("string_Achievement_Welcome_description") + "\n(" + currentAccountUsername + ")"), icon_path = bronzeIcon, duration=5, threaded=enableAchievementThreading)
            if achievementVersion not in ["v1.0.0"]: medalEarned = "Bronze"
        elif achievementToGain == "Achievement_Welcome2":
            toaster.show_toast("Bronze - Welcome to the Game - 2", str("Start a new game. - 2" + "\n(" + currentAccountUsername + ")"), icon_path = bronzeIcon, duration=5, threaded=enableAchievementThreading)
            if achievementVersion not in ["v1.0.0"]: medalEarned = "Bronze"
        elif achievementToGain == "Achievement_Welcome3":
            toaster.show_toast("Bronze - Welcome to the Game - 3", str("Start a new game. - 3" + "\n(" + currentAccountUsername + ")"), icon_path = bronzeIcon, duration=5, threaded=enableAchievementThreading)
            if achievementVersion not in ["v1.0.0"]: medalEarned = "Bronze"
        elif achievementToGain == "Achievement_All_Animals":
            toaster.show_toast("Gold - Zoologist", str("Complete all the game topics in the animals category." + "\n(" + currentAccountUsername + ")"), icon_path = goldIcon, duration=5, threaded=enableAchievementThreading)
            if achievementVersion not in ["v1.0.0"]: medalEarned = "Gold"
        elif achievementToGain == "Achievement_Hot_Streak":
            toaster.show_toast("Silver - You're on Fire!", str("Go on a streak of 5 correct games." + "\n(" + currentAccountUsername + ")"), icon_path = silverIcon, duration=5, threaded=enableAchievementThreading)
            if achievementVersion not in ["v1.0.0"]: medalEarned = "Silver"
        elif achievementToGain == "Achievement_DEBUG":
            toaster.show_toast("Trophy Level - Achievement Title", str("Achievement Description." + "\n(" + currentAccountUsername + ")"), icon_path = bronzeIcon, duration=5, threaded=enableAchievementThreading)
            if achievementVersion not in ["v1.0.0"]: medalEarned = "Silver"
        elif achievementToGain != "saving": print("GAME ERROR(No Achievement with that name found)")
        if achievementVersion not in ["v1.0.0"] and achievementToGain != "saving":
            if medalEarned == "Bronze": earnedBronze += 1
            elif medalEarned == "Silver": earnedSilver += 1
            elif medalEarned == "Gold": earnedGold += 1
            elif medalEarned == "Platinum": earnedPlatinum += 1
        if achievementVersion not in ["v1.0.0", "v1.1.0", "v1.2.0"]:
            duration = datetime.now() - playtimeStartTime
            currentPlaytime = round(float(currentPlaytime) + duration.total_seconds(), 2)
            playtimeStartTime = datetime.now()
        if achievementVersion not in ["v1.0.0", "v1.1.0", "v1.2.0"]: gained_Achievements = [str(achievementVersion)] + [str(lastPlaytimeDatePlayed)] + [str(currentPlaytime)] + [str(availableAchievements)] + [str(earnedBronze)] + [str(earnedSilver)] + [str(earnedGold)] + [str(earnedPlatinum)] + gained_Achievements[8:]
        elif achievementVersion not in ["v1.0.0"]: gained_Achievements = [str(availableAchievements)] + [str(earnedBronze)] + [str(earnedSilver)] + [str(earnedGold)] + [str(earnedPlatinum)] + gained_Achievements[5:]
        else: gained_Achievements = gained_Achievements
        if achievementToGain != "saving": gained_Achievements.append(achievementToGain)
        if achievementVersion not in ["v1.0.0", "v1.1.0"] and achievementToGain != "saving": gained_Achievements.append(str(date.today().strftime("%m/%d/%y") + " " + datetime.now().strftime("%I:%M %p")))
        if overrideResetAchivements == False and resetAchievements == False and deactivateFileOpening == False: pickle.dump(gained_Achievements, open(currentAccountPath + "\\achievementSave.p", "wb"))
## System Achievements Progress
    elif deactivateFileOpening == False and achievementsActivated == True and achievementToGain not in ["reset", "setup", "ready"] and "Progress" in achievementToGain:
        achievementToGain = achievementToGain.replace("Achievement_Progress_", "")
        animalsCategory = int(achievementProgressTracker[0])
        maxAnimalsCategory = int(achievementProgressTracker[1])
        winningStreak = int(achievementProgressTracker[2])
        maxWinningStreak = int(achievementProgressTracker[3])
        if achievementToGain == "Animals": animalsCategory += 1
        if animalsCategory >= maxAnimalsCategory: Achievements("Achievement_All_Animals")
## Streak Counter
        if winningStreak >= maxWinningStreak: Achievements("Achievement_Hot_Streak")
## Save Progress
        achievementProgressTracker = [animalsCategory, maxAnimalsCategory, winningStreak, maxWinningStreak]
        if overrideResetAchivements == False and resetAchievements == False and deactivateFileOpening == False: pickle.dump(achievementProgressTracker, open(currentAccountPath + "\\achievementProgressTracker.p", "wb"))


## Library Testing:
def testAchievements():
## Activate Achievement
    global exitSystem
    userAnswer = input("\nINPUT: ")
    start = time.time()
    if userAnswer.lower() == "welcome":
        print("Rewarding achievement = Achievement_Welcome")
        Achievements("Achievement_Welcome")
    elif userAnswer.lower() == "welcome2":
        print("Rewarding achievement = Achievement_Welcome2")
        Achievements("Achievement_Welcome2")
    elif userAnswer.lower() == "welcome3":
        print("Rewarding achievement = Achievement_Welcome3")
        Achievements("Achievement_Welcome3")
    elif userAnswer.lower() == "hot streak":
        print("Rewarding achievement = Achievement_Hot_Streak")
        Achievements("Achievement_Hot_Streak")
    elif userAnswer.lower() == "animal":
        currentCategory = "Animals"
        print("Rewarding one more = " + currentCategory)
        Achievements("Achievement_Progress_" + currentCategory)
    elif userAnswer.lower() == "exit": 
        accountLogin("quit")
        return
    elif userAnswer.lower() == "stats":
        if achievementsActivated == True and deactivateFileOpening == False: print(interfaceTranslation("string_stats_command"))
        else: print(interfaceTranslation("string_stats_command_fail"))
    elif userAnswer.lower() == "rename": accountLogin("renameAccount")
    elif userAnswer.lower() == "logout":
        accountLogin("logout")
        return
    elif userAnswer.lower() in ["clear", "reset"]: Achievements("reset")
    else: print(interfaceTranslation("string_debug_command_fail"))
    print("(" + str(round((time.time() - start), 6)) + " seconds)")
    testAchievements()


## Start System
librarySetup()
