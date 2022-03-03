# HC-RAT
Hacker Community Remote Access Trojan
# Requirements
python 3.7>=

libs:

``
pip install pyrebase4
``

``
pip install keyboard
``

``
pip install colorama
``
# Usage
HC RAT is a RAT that contain two kinds of attacks. [keylogger](https://en.wikipedia.org/wiki/Keystroke_logging) and [RCE](https://www.bugcrowd.com/glossary/remote-code-execution-rce/)

first file HC.py is the virus that keylog and controller.py is the controller of rce and keylogging

Target computer:

``
python HC.py
``

Controller computer:

```
python controller.py

[FirstRat@HCn1 ~] $ help

 help               showing this message
 cd               navigate remoted pc (Please Note that you should only add path after cd        
 updateId               move to newest session
 delete               delete current database
 fileout               write keylog to pc
 (any command else)               RCE
```

 Use ``updateID`` to control and reach the newest session

 Use ``delete`` to delete database content

 Use ``fileout`` to write out on your PC the keylog of the targeted PC

 ``any command else`` will run on the command prompt of the hacked PC 

# NOTE 

I am not responsible of any inappropriate usage of this script

# Advice 

You can make the RAT executable that will be better for hacking PC's that doesnt contain Python.

You may compile this way:

```
pip install pyinstaller
pyinstaller HC.py --noconsole --onefile 
```

Leave a star in your Way out

ZeD_OnE
