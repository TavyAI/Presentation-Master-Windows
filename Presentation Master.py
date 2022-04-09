'''
Tavy Presentation Master for Windows
Version 0.4
Designed by Taavi Rübenhagen
'''






'''
venv/Scripts/activate
$env:FLASK_ENV = "development"
python -m flask run --host=0.0.0.0
'''






from flask import Flask, request, render_template, jsonify
import tkinter as tk
from tkinter import *

import threading, os, random, time
import getpass, webbrowser, pyautogui, pyqrcode
from subprocess import Popen

import socket, getpass, webbrowser, pyautogui, pyqrcode
from subprocess import Popen
from pynput import keyboard






username = getpass.getuser()












def add_to_startup():
  file_path = r'"C:\Users\%s\Desktop\Presentation Master.py"'  % username
  bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % username
  with open(bat_path + '\\' + "open.bat", "w+") as bat_file:
    bat_file.write(r'start "" %s' % file_path)












class UIThread(threading.Thread):

  def run(self):

    window = tk.Tk(screenName="Presentation Master")
    window.title = "Tavy Presentation Master"
    window.geometry("900x800")
    window.wm_attributes("-transparentcolor", 'grey')
  
    hostname = socket.gethostname()
    ip = socket.gethostbyname(socket.gethostname())
    ip_qr = pyqrcode.create(ip)
    ip_qr_code = BitmapImage(data = ip_qr.xbm(scale=9))

    app_qr_code = BitmapImage(data = pyqrcode.create("http://tavy-ai.web.app").xbm(scale=2))
    

    frame = tk.Frame(master=window, width=900, height=800)
    logo = tk.Label(master=frame, text="TΛVY AI", font=("Segoe UI", 18, "bold"), foreground="darkblue")
    instruction = tk.Label(master=frame, text="Long press the + icon in the mobile app to scan this code", font=("Segoe UI", 12))
    ip = tk.Label(master=frame, text=ip, font=("Segoe UI", 36))
    background = tk.Label(master=frame, text="The server will keep running in background after you close this window", font=("Segoe UI", 12), cursor="hand2")
    background.bind("<Button-1>", lambda e: webbrowser.open_new("http://tavy-ai.web.app"))
    ip_qr_image = Label(window, image=ip_qr_code)
    app_qr_image = Label(window, image=app_qr_code, activebackground="blue")
    

    frame.pack()
    logo.place(x=450, y=30, anchor=CENTER)
    instruction.place(x=450, y=150, anchor=CENTER)
    ip_qr_image.place(x=450, y=340, anchor=CENTER)
    ip.place(anchor=CENTER, x=450, y=530)
    background.place(x=450, y=700, anchor=CENTER)


    
    window.mainloop()












app = Flask(__name__)






@app.route('/presentation', methods = ["GET", "POST"])
def presentation():
  rawData = request.get_data(as_text=True)#get_json()
  print(rawData)
  dataStrings = rawData.split("&")[0].split("=")
  if len(dataStrings) < 2: dataStrings = ['', '']
  print(dataStrings)
  if dataStrings[1] == '': json_file = {"data": ""}
  else:
    try:
      if dataStrings[0] == "link":
        link = dataStrings[1].replace("%3A", ":")
        link = link.replace("%2F", "/")
        link = link.replace("%23", "#")
        link = link.replace("%3D", "=")
        print(link)
        webbrowser.open_new(link)
        time.sleep(10)
        pyautogui.hotkey("ctrl", "shift", "f5")
      else:
        if dataStrings[1] == "1": pyautogui.hotkey("left")
        elif dataStrings[1] == "2": pyautogui.hotkey("right")
        elif dataStrings[1] == "4": pyautogui.hotkey("esc")
        elif dataStrings[1] == "5": pyautogui.hotkey("ctrl", "w")
        elif dataStrings[1] == "6": pyautogui.hotkey("alt", "f4")
      json_file = {}
      json_file["Code"] = "0"
    except: print("Failed")
  print(json_file)
  finalFile = jsonify(json_file)
  finalFile.headers['Access-Control-Allow-Origin'] = '*'
  return finalFile






class ServerThread(threading.Thread):

  def run(self):

    if __name__ == '__main__':
      app.run(host="0.0.0.0")






add_to_startup()
UIThread().start()
ServerThread().start()