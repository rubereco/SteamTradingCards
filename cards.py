from selenium.common.exceptions import InvalidSessionIdException
from selenium.webdriver.common.by import By
from requests_html import HTMLSession
from difflib import SequenceMatcher
from tkinter import messagebox
from selenium import webdriver
from tkinter import filedialog
from pathlib import Path
from time import sleep
from tkinter import *
import subprocess
import webbrowser
import threading 
import datetime
import logging
import sqlite3
import pickle
# import psutil
import ctypes
import time
# import sys
import os
##SIZE
NORMAL_WIDTH=100#x
NORMAL_HEIGTH=30#y
##AXIS X
POX_X_SPACING=20
POS_COL1_X=POX_X_SPACING
POS_COL2_X=(POX_X_SPACING*2)+NORMAL_WIDTH
POS_COL3_X=(POX_X_SPACING*3)+(NORMAL_WIDTH*2)
POS_COL4_X=(POX_X_SPACING*4)+(NORMAL_WIDTH*3)
POS_COL5_X=(POX_X_SPACING*5)+(NORMAL_WIDTH*4)
POS_COL6_X=(POX_X_SPACING*6)+(NORMAL_WIDTH*5)
POS_COL7_X=(POX_X_SPACING*7)+(NORMAL_WIDTH*6)
##AXIS Y
POX_Y_SPACING=20
POS_ROW1_Y=POX_Y_SPACING
POS_ROW2_Y=(POX_Y_SPACING*2)+NORMAL_HEIGTH
POS_ROW3_Y=(POX_Y_SPACING*3)+(NORMAL_HEIGTH*2)
POS_ROW4_Y=(POX_Y_SPACING*4)+(NORMAL_HEIGTH*3)
POS_ROW5_Y=(POX_Y_SPACING*5)+(NORMAL_HEIGTH*4)
POS_ROW6_Y=(POX_Y_SPACING*6)+(NORMAL_HEIGTH*5)
POS_ROW7_Y=(POX_Y_SPACING*7)+(NORMAL_HEIGTH*6)
##WINDOWS
CARDS_WIDTH=(POX_X_SPACING*7)+(NORMAL_WIDTH*6)
CARDS_HEIGTH=(POX_Y_SPACING*8)+(NORMAL_HEIGTH*7)
LOGIN_WIDTH=(POX_X_SPACING*3)+(NORMAL_WIDTH*2)
LOGIN_HEIGHT=(POX_Y_SPACING*5)+(NORMAL_HEIGTH*4)
START_WIDTH=(POX_X_SPACING*3)+(NORMAL_WIDTH*2)
START_HEIGHT=(POX_Y_SPACING*7)+(NORMAL_HEIGTH*6)
SETTINGS_HEIGHT=(POX_Y_SPACING*8)+(NORMAL_HEIGTH*7)
SETTINGS_WIDTH=int(POX_X_SPACING*3.5)+(NORMAL_WIDTH*3)
GPOP_WIDTH=int(POX_X_SPACING*3.5)+(NORMAL_WIDTH*3)
GPOP_HEIGHT=(POX_Y_SPACING*7)+(NORMAL_HEIGTH*6)
##VERSION
VERSION="V1.16"
##CREDENTIALS
URL="https://store.steampowered.com/login/"
##SETTINGS
class Settings():
    def save():
        with open(SETTINGS_FILE,"wb") as piklefile:
            pickle.dump(SETTINGS, piklefile)
    def GetWindowRectFromName(menu):
        name = SETTINGS["TITLE"]
        hwnd = ctypes.windll.user32.FindWindowW(0, name)
        rect = ctypes.wintypes.RECT()
        ctypes.windll.user32.GetWindowRect(hwnd, ctypes.pointer(rect))
        SETTINGS[menu] = (rect.left, rect.top)
        Settings.save()

SETTINGS_FILE = f"{Path.home()}\\Documents\\YPPAHSOFT\\settings.pkl"
if os.path.exists(SETTINGS_FILE):
   with open(SETTINGS_FILE,"rb") as piklefile:
        SETTINGS = pickle.load(piklefile)
else:
    APP_DIRECTORY=f"{Path.home()}\\Documents\\YPPAHSOFT\\"
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    SETTINGS = {
        "ACCID": None,
        "COUNTER": 0,
        "TIME": 0,
        "GRID": 0,
        "IPAGE": 0,
        "PRICE": 0,
        "STOP": False,
        "COOKIES": [],
        "S_DB_FILE": f"{Path.home()}\\Documents\\YPPAHSOFT\\cards.db",
        "APP_DIRECTORY": APP_DIRECTORY,
        "BG_COLOR": "SystemButtonFace",
        "TXT_COLOR": "black",
        "VERSION_CD": None,
        "PRICE_MULTIPLIER": 1.40,
        "START_POS": (int(user32.GetSystemMetrics(0)-(user32.GetSystemMetrics(0)/2)-100), int(user32.GetSystemMetrics(1)/2)-200),
        "CARDS_POS": (int(user32.GetSystemMetrics(0)-(user32.GetSystemMetrics(0)/2.5)), int(user32.GetSystemMetrics(1)/7)),
        "SETTINGS_POS": (int(user32.GetSystemMetrics(0)-(user32.GetSystemMetrics(0)/2)-250), int(user32.GetSystemMetrics(1)/2)-250),
        "GAMES_POS": (int(user32.GetSystemMetrics(0)-(user32.GetSystemMetrics(0)/2.5)), int(user32.GetSystemMetrics(1)/7)),
        "AUTO_POS": None,
        "TITLE": "CARD FARMER",
        "GPOP_FILTER": {
            "MAX_PRICE": None,
            "QUANTITY_ARS": None,
            "QUANTITY_GAM": None,
            "WALLET_QTTY": None,
        },
        "STEAM_DIR": None
    }
    if not os.path.exists(APP_DIRECTORY):
        os.mkdir(APP_DIRECTORY)
    Settings.save()

# if (SETTINGS["VERSION_CD"] == None or time.time()-SETTINGS["VERSION_CD"]) > 86400:
#     UPDATES_URL="https://github.com/YPPPAH/SteamTradingCards"
#     session = HTMLSession()
#     request = session.get(UPDATES_URL)
#     version = request.html.find("#repo-content-pjax-container", first=True).find(".markdown-title", first=True).text
#     if version != None:
#         if float(version) > VERSION:
#             result = messagebox.askquestion("","There is a newer version of the bot, do you want to download?")
#             SETTINGS["VERSION_CD"]=time.time()
#             if result == 'yes':
#                 webbrowser.open_new(UPDATES_URL)

class Functions():
    def fnd(driver,path):
        speed = True
        count = 0
        while speed:
            if count > 20:
                speed = False
                res = None
            try:
                res = driver.find_element(By.XPATH,path)
                speed = False
                print("found1 {}".format(path))
            except:
                print("nfound1 {}".format(path))
                count+=1
                sleep(0.1)
        return res

    def fndcn(driver,path):
        speed = True
        count = 0
        while speed:
            if count > 20:
                speed = False
                res = None
            try:
                res = driver.find_element(By.CLASS_NAME,path)
                speed = False
                print("found2 {}".format(path))
            except:
                print("nfound2 {}".format(path))
        return res

    def fnds(driver,path):
        speed = True
        count = 0
        while speed:
            if count > 20:
                speed = False
                res = None
            try:
                res = driver.find_elements(By.XPATH,path)
                speed = False
                print("found3 {}".format(path))
            except:
                print("nfound3 {}".format(path))
                pass
        return res
    
class Menus():

    def StartM():
        win = Tk()
        win.title(SETTINGS['TITLE'])
        win.config(bg=SETTINGS["BG_COLOR"])
        win.resizable(width=False, height=False)
        win.geometry(f"{START_WIDTH}x{START_HEIGHT}+{SETTINGS['START_POS'][0]}+{SETTINGS['START_POS'][1]}")

        def login():
            Settings.GetWindowRectFromName('START_POS')
            win.destroy()
            Menus.LoginM()
        
        def cards():
            if SETTINGS["COOKIES"]==[]:
                messagebox.showinfo('', 'You need to login to do this')    
            else:
                Settings.GetWindowRectFromName('START_POS')
                win.destroy()
                Menus.CardsM()

        def games():
            if SETTINGS["COOKIES"]==[]:
                messagebox.showinfo('', 'You need to login to do this')
            else:
                Settings.GetWindowRectFromName('START_POS')
                win.destroy()
                Menus.GamesMPop()

        def settings():
            Settings.GetWindowRectFromName('START_POS')
            win.destroy()
            Menus.SettingsM() 

        def logout():
            SETTINGS["COOKIES"]=[]
            Settings.save()
            Settings.GetWindowRectFromName('START_POS')
            win.destroy()
            Menus.StartM()

        def idle():
            if SETTINGS["STEAM_DIR"] == None:
                if not process_exists("Steam.exe"):
                    filename = 'C:\Program Files\Steam\steam.exe'
                    while not os.path.exists(filename):
                        messagebox.showinfo('', 'Select your steam exe')
                        filename = filedialog.askopenfilename(initialdir = "/", title = "Select a File", filetypes = (("Text files", "*.exe*"), ("all files", "*.*")))
                    SETTINGS["STEAM_DIR"] = filename
                    subprocess.Popen([SETTINGS['STEAM_DIR']])
                    Settings.save()
                    sleep(10)
                    windowHandle = ctypes.windll.user32.FindWindowW(None, "Steam")
                    ctypes.windll.user32.ShowWindow(windowHandle, 6)
                subprocess.Popen([f"{os.path.abspath(os.path.dirname(__file__))}/idle_master_extended_v1.7/IdleMasterExtended.exe"])
            else:
                if not process_exists("Steam.exe"):
                    subprocess.Popen([SETTINGS['STEAM_DIR']])
                    sleep(10)
                    windowHandle = ctypes.windll.user32.FindWindowW(None, "Steam")
                    ctypes.windll.user32.ShowWindow(windowHandle, 6)
                subprocess.Popen([f"{os.path.abspath(os.path.dirname(__file__))}/idle_master_extended_v1.7/IdleMasterExtended.exe"])


        def process_exists(process_name):
            call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
            output = subprocess.check_output(call).decode()
            last_line = output.strip().split('\r\n')[-1]
            return last_line.lower().startswith(process_name.lower())
        
        def idle_redirect():
            try:
                thread = threading.Thread(target=idle)
                if not thread.is_alive():
                    thread.start()
                else:
                    idle()
            except:
                pass

        def auto():
            pass

        cardsb = Button(win, text="Sell Cards", relief="flat", fg=SETTINGS["TXT_COLOR"], cursor="hand2", bg=SETTINGS["BG_COLOR"], font=("Times", "14", "bold"), command=cards)
        gamesb = Button(win, text="Buy Games", relief="flat", fg=SETTINGS["TXT_COLOR"], cursor="hand2", bg=SETTINGS["BG_COLOR"], font=("Times", "14", "bold"), command=games)
        idleb = Button(win, text="Idle Games", relief="flat", fg=SETTINGS["TXT_COLOR"], cursor="hand2", bg=SETTINGS["BG_COLOR"], font=("Times", "14", "bold"), command=idle_redirect)
        autob = Button(win, text="Auto", relief="flat", fg=SETTINGS["TXT_COLOR"], cursor="hand2", bg=SETTINGS["BG_COLOR"], font=("Times", "14", "bold"), command=auto)
        settingsb = Button(win, text="Settings", relief="flat", fg=SETTINGS["TXT_COLOR"], cursor="hand2", bg=SETTINGS["BG_COLOR"], font=("Times", "14", "bold"), command=settings)

        cardsb.place(x=POS_COL1_X+60,y=POS_ROW1_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        gamesb.place(x=POS_COL1_X+60,y=POS_ROW2_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        idleb.place(x=POS_COL1_X+60,y=POS_ROW3_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        autob.place(x=POS_COL1_X+60,y=POS_ROW4_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        settingsb.place(x=POS_COL1_X+60,y=POS_ROW5_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)

        if SETTINGS["COOKIES"]==[]:
            btn = Button(win, text="Login", relief="flat", fg=SETTINGS["TXT_COLOR"], cursor="hand2", bg=SETTINGS["BG_COLOR"], font=("Times", "14", "bold"), command=login)
            btn.place(x=POS_COL1_X+60,y=POS_ROW6_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        else:
            btnt = Label(win,text='Logged',bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"], font=("Times", "14", "bold"))
            btnt.place(x=POS_COL1_X,y=POS_ROW6_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
            btnl = Button(win, text="Logout?", relief="flat", fg=SETTINGS["TXT_COLOR"], cursor="hand2", bg=SETTINGS["BG_COLOR"], font=("Times", "14", "bold"), command=logout)
            btnl.place(x=POS_COL2_X,y=POS_ROW6_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
            # link = Label(win, text="Hyperlink", fg="black", cursor="hand2", bg=SETTINGS["BG_COLOR"])
            # link.bind("<Button-1>", lambda e: webbrowser.open_new("http://www.google.com"))
            # link.place(x=POS_COL2_X,y=POS_ROW4_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)

        win.mainloop()

    def LoginM():
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        win = Tk()
        win.title(SETTINGS['TITLE'])
        win.geometry(f"{LOGIN_WIDTH}x{LOGIN_HEIGHT}+{int(user32.GetSystemMetrics(0)-(user32.GetSystemMetrics(0)/2)-100)}+{int(user32.GetSystemMetrics(1)/2)-200}")
        win.config(bg=SETTINGS["BG_COLOR"])
        win.resizable(width=False, height=False)

        def loging():
            u = usri.get()
            p = pswi.get()
            check_counter=0
            if p == "":
                warn = "Password can't be empty"
            else:
                check_counter += 1
            if u == "":
                warn = "Username can't be empty"
            else:
                check_counter += 1
            if check_counter == 2:
                driver = webdriver.Firefox()
                # print_and_console("LOGING...")
                driver.get(URL)
                user = Functions.fnd(driver,"//input[@id='input_username']")
                password = Functions.fnd(driver,"//input[@id='input_password']")
                user.send_keys(usri.get())
                password.send_keys(pswi.get())
                Functions.fndcn(driver,'login_btn').click()
                sleep(2)
                # print_and_console("2FA...")
                _2fa = f2ai.get()
                if _2fa!="":
                    try:
                        twofactor = Functions.fnd(driver,"//input[@id='twofactorcode_entry']")
                        twofactor.send_keys(_2fa)
                    except:
                        # print_and_console("NO 2FA FOUND")
                        pass
                else:
                    # print_and_console("NO USER INPUT")
                    pass
                # print_and_console("2FA DONE")
                try:
                    Functions.fnds(driver,"//div[@id='login_twofactorauth_buttonset_entercode']//div")[0].click()
                except:
                    sleep(0.5)
                    Functions.fnd(driver,"//div[@id='error_display]'").text = "The account name or password that you have entered is incorrect."
                    driver.quit()
                    messagebox.showinfo('', "Incorrect input")
                # print_and_console("LOGGED")
                SETTINGS["COOKIES"]=driver.get_cookies()
                SETTINGS["ACCID"]=Functions.fnds(driver,"//div[@id='global_actions']//a")[-1].get_attribute("href")
                driver.quit()
                win.destroy()
                Menus.StartM()
                Settings.save()
            else:
                messagebox.showinfo('', warn)

        def login_redirect():
            try:
                thread = threading.Thread(target=loging)
                if not thread.is_alive():
                    thread.start()
                else:
                    loging()
            except:
                pass

        def back():
            win.destroy()
            Menus.StartM()

        # labels
        usr = Label(win, text='Username ',bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"], font=("Times", "14"))
        psw = Label(win, text='Password ',bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"], font=("Times", "14"))
        f2a = Label(win,text='2fa',bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"], font=("Times", "14"))

        usr.place(x=POS_COL1_X,y=POS_ROW1_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        psw.place(x=POS_COL1_X,y=POS_ROW2_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        f2a.place(x=POS_COL1_X,y=POS_ROW3_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        
        # Entry
        usri = Entry(win, fg=SETTINGS["TXT_COLOR"], font=("Times", "14"), bg=SETTINGS["BG_COLOR"])
        pswi = Entry(win, fg=SETTINGS["TXT_COLOR"], font=("Times", "14"), bg=SETTINGS["BG_COLOR"], show="*")
        f2ai = Entry(win, fg=SETTINGS["TXT_COLOR"], font=("Times", "14"), bg=SETTINGS["BG_COLOR"])

        usri.place(x=POS_COL2_X,y=POS_ROW1_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        pswi.place(x=POS_COL2_X,y=POS_ROW2_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        f2ai.place(x=POS_COL2_X,y=POS_ROW3_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)

        # button 
        btn = Button(win, text="Login", relief="flat", fg=SETTINGS["TXT_COLOR"], bg=SETTINGS["BG_COLOR"], font=("Times", "14", "bold"), command=login_redirect)
        btn.place(x=POS_COL1_X+60,y=POS_ROW4_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)

        Backbt = Button(win, text="<", fg=SETTINGS["TXT_COLOR"], cursor="hand2", bg=SETTINGS["BG_COLOR"], command=back)
        Backbt.place(x=0,y=0,width=POX_X_SPACING, height=POX_Y_SPACING)

        win.mainloop()
    
    def SettingsM():
        win = Tk()
        win.title(SETTINGS['TITLE'])
        win.config(bg=SETTINGS["BG_COLOR"])
        win.resizable(width=False, height=False)
        win.geometry(f"{SETTINGS_WIDTH}x{SETTINGS_HEIGHT}+{SETTINGS['SETTINGS_POS'][0]}+{SETTINGS['SETTINGS_POS'][1]}")
        OPTIONS = ["1.0","1.1","1.2","1.3","1.4","1.5","1.6","1.7","1.8","1.9","2.0"]
        variable = StringVar(win)
        variable.set(OPTIONS[4])

        def dark_theme():
            if SETTINGS["BG_COLOR"] == "SystemButtonFace":
                SETTINGS["BG_COLOR"] = "#1e1e1e"
                lblcolor["text"]="black"
            else:
                SETTINGS["BG_COLOR"] = "SystemButtonFace"
                lblcolor["text"]="white"

            if SETTINGS["TXT_COLOR"] == "black":
                SETTINGS["TXT_COLOR"] = "white"
            else:
                SETTINGS["TXT_COLOR"] = "black"
            Settings.GetWindowRectFromName('SETTINGS_POS')
            win.destroy()
            Menus.SettingsM()

        def savemulti():
            SETTINGS['PRICE_MULTIPLIER'] = float(variable.get())
            messagebox.showinfo('', 'succesfully updated')
            
        def back():
            Settings.GetWindowRectFromName('SETTINGS_POS')
            win.destroy()
            Menus.StartM()
        
        def clear_cache():
            import shutil
            folder = f"{Path.home()}\\AppData\\Local\\Temp\\"
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))
        
        Backbt = Button(win, text="<", fg=SETTINGS["TXT_COLOR"], cursor="hand2", bg=SETTINGS["BG_COLOR"], command=back)
        Backbt.place(x=0,y=0,width=POX_X_SPACING, height=POX_Y_SPACING)
        darkbtn = Button(win, text="Dark Theme", fg=SETTINGS["TXT_COLOR"], cursor="hand2", bg=SETTINGS["BG_COLOR"], command=dark_theme)
        darkbtn.place(x=POS_COL1_X,y=POS_ROW1_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        backbtn = Button(win, text="Save", fg=SETTINGS["TXT_COLOR"], relief="groove" , cursor="hand2", bg=SETTINGS["BG_COLOR"], command=savemulti)
        backbtn.place(x=POS_COL2_X,y=POS_ROW2_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        Option = OptionMenu(win, variable, *OPTIONS)
        Option.configure(bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"])
        Option.place(x=POS_COL1_X,y=POS_ROW2_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        lblLine1 = Label(win,text="-->",bg=SETTINGS["BG_COLOR"], relief="groove", fg=SETTINGS["TXT_COLOR"])
        lblLine1.place(x=POS_COL2_X,y=POS_ROW1_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        # lblLine2 = Label(win,text="-->",bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"])
        # lblLine2.place(x=POS_COL2_X,y=POS_ROW3_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        lblcolor = Label(win,text="",bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"])
        lblcolor.place(x=POS_COL3_X,y=POS_ROW1_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        lblcache = Label(win,text="Clear tmp folder",bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"])
        lblcache.place(x=POS_COL1_X,y=POS_ROW3_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        cachebtn = Button(win, text="Clear", fg=SETTINGS["TXT_COLOR"], relief="groove" , cursor="hand2", bg=SETTINGS["BG_COLOR"], command=clear_cache)
        cachebtn.place(x=POS_COL2_X,y=POS_ROW3_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        if SETTINGS["BG_COLOR"] == "SystemButtonFace":
            lblcolor["text"]="white"
        else:
            lblcolor["text"]="black"
        lblmultiplier = Label(win,text=f"x{SETTINGS['PRICE_MULTIPLIER']}%",bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"])
        lblmultiplier.place(x=POS_COL3_X,y=POS_ROW2_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        

        win.mainloop()

    def GamesM():
        pass

    def GamesMPop():
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        win = Tk()
        win.title(SETTINGS['TITLE'])
        win.geometry(f"{GPOP_WIDTH}x{GPOP_HEIGHT}+{int((user32.GetSystemMetrics(0)/2)+50)}+{int(user32.GetSystemMetrics(1)/2)-200}")
        win.config(bg=SETTINGS["BG_COLOR"])
        win.resizable(width=False, height=False)

        def back():
            win.destroy()
            Menus.StartM()

        def save():
            if gamepric.get() != "":
                if qttars.get() == "" and qttgam.get() == "" and limitwa.get() == "":
                    messagebox.showinfo('', 'You have to enter atleast one filter')
                else:
                    SETTINGS["BG_COLOR"]["MAX_PRICE"] = gamepricl.get()
                    if qttars.get() != "":
                        SETTINGS["BG_COLOR"]["QUANTITY_ARS"] = qttars.get()
                    if qttgam.get() != "":
                        SETTINGS["BG_COLOR"]["QUANTITY_GAM"] = qttgam.get()
                    if limitwa.get() != "":
                        SETTINGS["BG_COLOR"]["WALLET_QTTY"] = limitwa.get()
                    Settings.save()
                    win.destroy()
                    Menus.GamesM()
            else:
                messagebox.showinfo('', 'Enter max price')

        Backbt = Button(win, text="<", fg=SETTINGS["TXT_COLOR"], cursor="hand2", bg=SETTINGS["BG_COLOR"], command=back)
        Backbt.place(x=0,y=0,width=POX_X_SPACING, height=POX_Y_SPACING)
        gamepricl = Label(win, text='Max price per game (Ars$)',bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"], font=("Times", "14"))
        qttarsl = Label(win, text='A Quantity of (Ars$)',bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"], font=("Times", "14"))
        qttgaml = Label(win, text='A Quantity of (Games)', bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"], font=("Times", "14"))
        limitwal = Label(win, text='Limiting min wallet (Ars$)', bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"], font=("Times", "14"))

        gamepricl.place(x=POS_COL1_X,y=POS_ROW1_Y,width=NORMAL_WIDTH*2, height=NORMAL_HEIGTH)
        qttarsl.place(x=POS_COL1_X,y=POS_ROW3_Y,width=NORMAL_WIDTH*2, height=NORMAL_HEIGTH)
        qttgaml.place(x=POS_COL1_X,y=POS_ROW4_Y,width=NORMAL_WIDTH*2, height=NORMAL_HEIGTH)
        limitwal.place(x=POS_COL1_X,y=POS_ROW5_Y,width=NORMAL_WIDTH*2, height=NORMAL_HEIGTH)

        buyby = Label(win, text='BUY BY',bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"], font=("Times", "14"))
        buyby.place(x=POS_COL1_X,y=POS_ROW2_Y,width=NORMAL_WIDTH*3, height=NORMAL_HEIGTH)

        gamepric = Entry(win, fg=SETTINGS["TXT_COLOR"], font=("Times", "14"), bg=SETTINGS["BG_COLOR"])
        qttars = Entry(win, fg=SETTINGS["TXT_COLOR"], font=("Times", "14"), bg=SETTINGS["BG_COLOR"])
        qttgam = Entry(win, fg=SETTINGS["TXT_COLOR"], font=("Times", "14"), bg=SETTINGS["BG_COLOR"])
        limitwa = Entry(win, fg=SETTINGS["TXT_COLOR"], font=("Times", "14"), bg=SETTINGS["BG_COLOR"])

        gamepric.place(x=POS_COL3_X,y=POS_ROW1_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        qttars.place(x=POS_COL3_X,y=POS_ROW3_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        qttgam.place(x=POS_COL3_X,y=POS_ROW4_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        limitwa.place(x=POS_COL3_X,y=POS_ROW5_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)

        backbtn = Button(win, text="Continue", fg=SETTINGS["TXT_COLOR"], font=("Times", "14"), relief="groove" , cursor="hand2", bg=SETTINGS["BG_COLOR"], command=save)
        backbtn.place(x=POS_COL2_X,y=POS_ROW6_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)

        win.mainloop()

    def CardsM():
        win = Tk()
        win.title(SETTINGS['TITLE'])
        win.config(bg=SETTINGS["BG_COLOR"])
        win.resizable(width=False, height=False)
        win.geometry(f"{CARDS_WIDTH}x{CARDS_HEIGTH}+{SETTINGS['CARDS_POS'][0]}+{SETTINGS['CARDS_POS'][1]}")

        def stop():
            SETTINGS["STOP"]=True

        def back():
            Settings.GetWindowRectFromName('CARDS_POS')
            win.destroy()
            Menus.StartM()

        def Clean():
            mylist.delete(0,END)

        def print_console(text):
            mylist.insert(END, text)

        def All():
            Clean()
            ##DB
            mylist.insert(END,"|  id  |  Card Name  |  Price  |  Percent  |  Game  |  Date  |  ")
            connection = sqlite3.connect(SETTINGS["S_DB_FILE"])
            cursor = connection.cursor()
            cursor.execute('''SELECT * FROM Cards''')
            select = cursor.fetchall()
            for doc in select:
                mylist.insert(END, "| nº{} | {} | ARS${} | {}% | {} | {} |".format(doc[0],doc[1],doc[2],doc[3],doc[4],doc[5]))
            connection.commit()
            connection.close()
            mylist.see("end")

        def Del():
            text = txtInput1.get()
            if text!="":
                ##DB
                connection = sqlite3.connect(SETTINGS["S_DB_FILE"])
                cursor = connection.cursor()
                cursor.execute('''DELETE FROM Cards WHERE id = {}'''.format(text))
                connection.commit()
                connection.close()
                All()
            else:
                print_and_console("***NOT FOUND***")

        def Sel():
            Clean()
            ##DB
            connection = sqlite3.connect(SETTINGS["S_DB_FILE"])
            cursor = connection.cursor()
            cursor.execute('''SELECT * FROM Cards''')
            select = cursor.fetchall()
            for doc in select:
                if compare(txtInput1.get(),doc[4])>0.7:
                    mylist.insert(END, "| nº{} | {} | ARS${} | {}% | {} | {} |".format(doc[0],doc[1],doc[2],doc[3],doc[4],doc[5]))
            connection.commit()
            connection.close()
        
        def compare(dbtext,imtext):
            return SequenceMatcher(None, dbtext, imtext).ratio()
        
        def sell_redirect():
            try:
                thread = threading.Thread(target=cromos_sell)
                if not thread.is_alive():
                    thread.start()
                else:
                    cromos_sell()
            except:
                pass

        def Replace(string):
            return string.replace(",",".")

        def Get_cookies(driver):
            for cookie in SETTINGS["COOKIES"]:
                driver.add_cookie(cookie)
            return driver

        def reset_settings():
            SETTINGS["COUNTER"]=0
            SETTINGS["TIME"]=0
            SETTINGS["GRID"]=0
            SETTINGS["IPAGE"]=0
            SETTINGS["PRICE"]=0

        def GotoPage(driver,inventory_url):
            driver.get(inventory_url)##load inv
            sleep(1)
            if SETTINGS["IPAGE"] > 0:##scroll
                sleep(0.5)
                for x in range(SETTINGS["IPAGE"]):
                    driver.find_element(By.XPATH,"//a[@id='pagebtn_next']").click()
                    sleep(1)

        def cromos_sell():
            try:
                if not os.path.exists(SETTINGS["S_DB_FILE"]):
                    ##DB
                    connection = sqlite3.connect(SETTINGS["S_DB_FILE"])
                    cursor = connection.cursor()
                    cursor.execute('''CREATE TABLE IF NOT EXISTS Cards (id INT PRIMARY KEY,Name TEXT, Price FLOAT, Percent INT, Game TEXT, Date TEXT)''')
                    connection.commit()
                    connection.close()
                Clean()
                lblCounter["text"]=SETTINGS["COUNTER"]
                lblPrice["text"]=SETTINGS["PRICE"]
                lblTime["text"]=SETTINGS["TIME"]
                driver = webdriver.Firefox()
                driver.implicitly_wait(3)
                driver.get("https://steamcommunity.com/")
                driver = Get_cookies(driver)
                driver.execute_script('''window.open("","_blank");''')
                driver.switch_to.window(driver.window_handles[0])
                inventory_url = f"{SETTINGS['ACCID']}/inventory/#753"
                #---start doing sells
                driver.get(URL)
                driver.execute_script('''ChangeLanguage( 'english' );''')
                sleep(1)
                GotoPage(driver,inventory_url)##load inv & scroll
                SETTINGS["STOP"]=False
                card_nameb = None
                name = ["",""]
                res = None
                for x in range(10000):
                    if SETTINGS["STOP"]==False:
                        Tstart = time.time()
                        Get_inventory_grid(driver,1,inventory_url)
                        name = ["",""]
                        gname = ["",""]
                        try:##find card name
                            name[0] = driver.find_element(By.XPATH,"//h1[@id='iteminfo0_item_name']").text
                            gname[0] = driver.find_element(By.XPATH,"//div[@id='iteminfo0_game_info']//div[3]").text
                        except:
                            pass
                        try:
                            name[1] = driver.find_element(By.XPATH,"//h1[@id='iteminfo1_item_name']").text
                            gname[1] = driver.find_element(By.XPATH,"//div[@id='iteminfo1_game_info']//div[3]").text
                        except:
                            pass
                        if name[0]=="":
                            card_namea=name[1]
                            res = 1 
                        else:
                            card_namea=name[0]
                            res = 0
                        if gname[0]=="":
                            game_name = gname[1]
                        else:
                            game_name = gname[0]
                        if card_namea != card_nameb:
                            card_nameb = card_namea
                            ##---selling
                            name = ["",""]
                            sleep(1)
                            try:##find card link
                                if res ==0:
                                    name[0] = Functions.fnd(driver,"//div[@id='iteminfo0_item_market_actions']//a").get_attribute("href")
                            except:
                                pass
                            try:
                                if res == 1:
                                    name[1] = Functions.fnd(driver,"//div[@id='iteminfo1_item_market_actions']//a").get_attribute("href")
                            except:
                                pass
                            if name[0]=="":
                                card_url=name[1]
                            else:
                                card_url=name[0]
                            ##loking for price
                            print_and_console("GETTING CARD PRICE...")
                            driver.switch_to.window(driver.window_handles[1])
                            driver.get(card_url)##load card
                            speed = True
                            refresh = 0
                            while speed:
                                refresh+=1
                                if refresh > 1:
                                    driver.refresh()
                                try:
                                    text = driver.find_elements(By.XPATH,"//div[@id='market_commodity_forsale_table']//td")[0].text
                                    speed = False
                                except:
                                    pass
                            price = str(text.split(" ")[1])
                            try:
                                price = round(float(Replace(price))*SETTINGS["PRICE_MULTIPLIER"],2)
                                print_and_console("PRICE FOUND")
                                driver.switch_to.window(driver.window_handles[0])
                                finish_sell(driver, price, card_namea, game_name, inventory_url,Tstart)
                            except ValueError:
                                SETTINGS["GRID"]+=1
                        else:
                            card_nameb = card_namea
                            finish_sell(driver, price, card_namea, game_name, inventory_url,Tstart)
                    else:
                        driver.quit()
                        print_and_console("***STOPED***")
                        break
            except InvalidSessionIdException:
                print_and_console("BROWSER CONNECTION LOST")
            except Exception as e:
                logging.error(e)
                messagebox.showerror(title="Error", message="Unexpected error")
                exit()

        def print_and_console(text):
            print(text)

        def Get_inventory_grid(driver,num):
            sleep(0.5)
            print_and_console("SEARCHING FOR GRID...")
            if num == 1:
                if Get_number(driver)%25 == 0 and Get_number(driver)!=0:
                    Functions.fnd(driver,"//a[@id='pagebtn_next']").click()
                    SETTINGS["IPAGE"]+=1
            invetorygrid = driver.find_elements(By.XPATH,"//div[@class='itemHolder']")
            invetorygrid[Get_number(driver)].click()
            print_and_console("GRID FOUND")
        
        def Get_number(driver):
            if SETTINGS["GRID"] == 0:
                try:
                    gems = driver.find_element(By.XPATH,"//h1[@id='iteminfo1_item_name']").text.split(" ")[1]
                    if gems == "Gems" or gems == "Gemas":
                        SETTINGS["GRID"] = 1
                    else:
                        SETTINGS["GRID"] = 0
                except IndexError:
                    SETTINGS["GRID"] = 0
            return SETTINGS["GRID"]
        
        def info():
            Clean()
            mylist.insert(END,"Sel-> Selects from the db the registres by game name, introduced in the user input")
            mylist.insert(END,"Del-> Deletes from the db the registry with the introduced id")
            mylist.insert(END,"C-> Cleans the Console")
            mylist.insert(END,"All-> Selects all registres from the db")
            mylist.insert(END,"START-> Starts selling")
            mylist.insert(END,"Restart-> Resets all values to start over")
            mylist.insert(END,"Stop-> Stops selling when finishes the actual card")
            mylist.insert(END,"Back-> Quits to the menu, please press stop before pressing this to avoid issues")
            mylist.insert(END,"ESTIMATED TIME 30m -> 250 cards (comfirmation cap)")

        def finish_sell(driver,price,name,gamename,inventory_url,Tstart):
            ##SELLING
            Get_inventory_grid(driver,0,inventory_url)
            try:
                Functions.fnd(driver,"//div[@id='iteminfo0_item_market_actions']//span[2]").click()##sell btn
            except:
                try:
                    Functions.fnd(driver,"//div[@id='iteminfo1_item_market_actions']//span[2]").click()##sell btn
                except:
                    pass
            sleep(0.5)
            inputtext = Functions.fnd(driver,"//input[@id='market_sell_buyercurrency_input']")##price input
            inputtext.send_keys(price)
            sleep(0.5)
            Functions.fnd(driver,"//a[@id='market_sell_dialog_accept']").click()##btn put for sale 
            if driver.find_element(By.XPATH,("//div[@id='market_sell_dialog_error']")).text == "You must agree to the terms of the Steam Subscriber Agreement to sell this item.":
                Functions.fnd(driver,"//input[@id='market_sell_dialog_accept_ssa']").click()##checkbox
                Functions.fnd(driver,"//a[@id='market_sell_dialog_accept']").click()##btn put for sale 
            sleep(0.5)
            Functions.fnd(driver,"//a[@id='market_sell_dialog_ok']").click()##btn ok 
            if driver.find_element(By.XPATH,("//div[@id='market_sell_dialog_error']")).text == "You already have a listing for this item pending confirmation. Please confirm or cancel the existing listing.":
                Functions.fnd(driver,"//div[@id='market_sell_dialog']//div[@class='newmodal_close']").click()##close modal
                SETTINGS["GRID"]+=1
                print_and_console("CARD ALREADY SOLD")
            else:
                sleep(0.5)
                if driver.find_element(By.XPATH,("//div[@id='market_sell_dialog_error']")).text == "You have too many listings pending confirmation. Please confirm or cancel some before attempting to list more.":
                    SETTINGS["STOP"]=True
                    Clean()
                    mylist.insert(END,"***************************************************MAX CONFIRMATIONS REACHED***********************************************")
                    mylist.insert(END,"*********************************************PLEASE CONFIRM THE CARDS AND RESTART******************************************")
                else:
                    sleep(0.5)
                    try:
                        driver.find_element(By.XPATH,"//div[@class='newmodal_buttons']//span").click()##2fa x btn 
                    except:
                        try:
                            Functions.fnd(driver,"//div[@class='newmodal_header']//div").click()
                        except:
                            SETTINGS["GRID"]-=1
                    #saving
                    SETTINGS["COUNTER"]+=1
                    SETTINGS["GRID"]+=1
                    SETTINGS["TIME"]+=round((time.time() - Tstart),2)
                    SETTINGS["PRICE"]=round(float(SETTINGS["PRICE"])+price,2)
                    lblCounter["text"]=SETTINGS["COUNTER"]
                    lblTime["text"] = SETTINGS["TIME"]
                    lblPrice["text"] = SETTINGS["PRICE"]
                    ##DB
                    connection = sqlite3.connect(SETTINGS["S_DB_FILE"])
                    cursor = connection.cursor()
                    cursor.execute('''SELECT id FROM Cards ORDER BY id DESC LIMIT 1''')
                    select = cursor.fetchall()
                    try:
                        for doc in select:
                            number = int(doc[0]+1)
                    except IndexError:
                        number = 0
                    if not "number" in locals():
                        number = 0
                    gamename = gamename.replace(" Trading Card","")
                    dt = datetime.datetime.today()
                    date = "{}-{}-{}".format(dt.day,dt.month,dt.year)
                    name = name.replace('"','')
                    cursor.execute('''INSERT INTO Cards (id, Name, Price, Percent, Game, Date) VALUES ({},"{}", {}, {}, "{}","{}")'''.format(number, name, price, str(SETTINGS["PRICE_MULTIPLIER"]).split(".")[1]+"0",gamename,date))
                    cursor.execute('''SELECT * FROM Cards ORDER BY id DESC LIMIT 1''')
                    select = cursor.fetchall()
                    for doc in select:
                        print_console("| nº{} | {} | ARS${} | {}% | {} | {} |".format(doc[0],doc[1],doc[2],doc[3],doc[4],doc[5]))
                    connection.commit()
                    cursor.close()
                    connection.close()
                    mylist.see("end")
                    #DB
                    print_and_console("SOLD")
                    sleep(0.5)


        Backbt = Button(win, text="<", fg=SETTINGS["TXT_COLOR"], cursor="hand2", bg=SETTINGS["BG_COLOR"], command=back)
        Backbt.place(x=0,y=0,width=POX_X_SPACING, height=POX_Y_SPACING)
        ###Start
        btnStart = Button(win,text="Start", command=sell_redirect,bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"])
        btnStart.place(x=POS_COL2_X,y=POS_ROW3_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        ###Quit
        btnQuit = Button(win,text="Back", command=back,bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"])
        btnQuit.place(x=POS_COL6_X,y=POS_ROW3_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        ###Stop
        btnStop = Button(win,text="Stop", command=stop,bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"])
        btnStop.place(x=POS_COL6_X,y=POS_ROW2_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        ###Restart
        btnRestart = Button(win,text="Reset", command=reset_settings,bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"])
        btnRestart.place(x=POS_COL6_X,y=POS_ROW1_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        ###info
        btnRestart = Button(win,text="i", command=info,bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"])
        btnRestart.place(x=POS_COL1_X,y=POS_ROW1_Y,width=(NORMAL_WIDTH-20)/2, height=NORMAL_HEIGTH)
        ###Buttons
        ##line
        lblLine1 = Label(win,text="", borderwidth=2, relief="groove",bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"])
        lblLine1.place(x=POS_COL1_X-4,y=POS_ROW2_Y-4,width=NORMAL_WIDTH*2+30, height=NORMAL_HEIGTH+10)
        ##CLS
        btnCls = Button(win,text="C", command=Clean,bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"])
        btnCls.place(x=POS_COL1_X,y=POS_ROW3_Y,width=(NORMAL_WIDTH-20)/2, height=NORMAL_HEIGTH)
        ##ALL
        btnAll = Button(win,text="All", command=All,bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"])
        btnAll.place(x=POS_COL1_X+60,y=POS_ROW3_Y,width=(NORMAL_WIDTH-20)/2, height=NORMAL_HEIGTH)
        ##sel
        btnsel = Button(win,text="Sel", command=Sel,bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"])
        btnsel.place(x=POS_COL1_X,y=POS_ROW2_Y,width=(NORMAL_WIDTH-20)/2, height=NORMAL_HEIGTH)
        ##del
        btndel = Button(win,text="Del", command=Del,bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"])
        btndel.place(x=POS_COL1_X+60,y=POS_ROW2_Y,width=(NORMAL_WIDTH-20)/2, height=NORMAL_HEIGTH)
        ##db input
        txtInput1=Entry(win,bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"])
        txtInput1.place(x=POS_COL2_X,y=POS_ROW2_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        ###Console
        ##scroll
        scrollbar = Scrollbar(win,bg=SETTINGS["BG_COLOR"])
        mylist = Listbox(win, yscrollcommand = scrollbar.set ,bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"])
        mylist.place(x=POS_COL1_X,y=POS_ROW4_Y,width=NORMAL_WIDTH*7, height=NORMAL_HEIGTH*6)
        info()
        scrollbar.config( command = mylist.yview )
        scrollbar.place(x=POS_COL7_X-POX_X_SPACING,y=POS_ROW4_Y,width=POX_X_SPACING, height=NORMAL_HEIGTH*6)
        ####Counter 
        ###sold
        Label1 = Label(win, text="CARDS DONE",bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"])
        Label1.place(x=POS_COL4_X,y=POS_ROW3_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        lblCounter = Label(win,text="0", borderwidth=2, relief="groove",bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"])
        lblCounter.place(x=POS_COL5_X,y=POS_ROW3_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        ###price
        Label2 = Label(win, text="CUR. TOTAL PRICE",bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"])
        Label2.place(x=POS_COL4_X,y=POS_ROW2_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        lblPrice = Label(win,text="0", borderwidth=2, relief="groove",bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"])
        lblPrice.place(x=POS_COL5_X,y=POS_ROW2_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        ##time
        Label3 = Label(win, text="TIME",bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"])
        Label3.place(x=POS_COL4_X,y=POS_ROW1_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        lblTime = Label(win,text="0", borderwidth=2, relief="groove",bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"])
        lblTime.place(x=POS_COL5_X,y=POS_ROW1_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        #FIX update cards gui
        win.mainloop()

Menus.StartM()