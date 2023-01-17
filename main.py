import os
try:
    import time, os , warnings, json, selenium_stealth, colorama, undetected_chromedriver, sys, random, selenium, logging, subprocess, requests, base64, getpass
    import undetected_chromedriver.v2 as uc
    from selenium import webdriver
    from selenium_stealth import stealth
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import Select
    from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, TimeoutException, ElementNotInteractableException
    from colorama import Fore, Back, Style
    from pystyle import Colors, Colorate, Center
    from datetime import datetime
    from sys import exit
    from discord_webhook import DiscordWebhook, DiscordEmbed
    from yaspin import yaspin
    from yaspin.spinners import Spinners
    from pathlib import Path
    from threading import Thread
    from pyprotector import PythonProtector
    from tools.app import app
    print(f"\n{Fore.MAGENTA}[{Fore.RESET}!{Fore.MAGENTA}] {Fore.RESET}Imports successful!")
    time.sleep(1)
except:
    print("\nImports failed! Trying to install...")
    z = "python -m pip install "; os.system('%scolorama' % (z)); os.system('%sselenium' % (z)); os.system('%sundetected-chromedriver' % (z)); os.system('%spystyle' % (z)); os.system('%sselenium-stealth' % (z)); os.system('%sdhooks' % (z)); os.system('%sPythonProtector' % (z)); os.system('%syaspin' % (z)); os.system('%sdiscord-webhook' % (z))
    print(f"\n{Fore.MAGENTA}[{Fore.RESET}!{Fore.MAGENTA}] {Fore.RESET}Imports successful!")
    time.sleep(1)

# Imports
import time, os , warnings, json, selenium_stealth, colorama, undetected_chromedriver, sys, random, selenium, logging, subprocess, requests, base64
import undetected_chromedriver.v2 as uc
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, TimeoutException, ElementNotInteractableException
from colorama import Fore, Back, Style
from pystyle import Colors, Colorate, Center
from datetime import datetime
from sys import exit
from discord_webhook import DiscordWebhook, DiscordEmbed
from yaspin import yaspin
from yaspin.spinners import Spinners
from pathlib import Path
from threading import Thread
from pyprotector import PythonProtector
from tools.app import app
###############################################MODULES###############################################

def clear(): return os.system('cls' if os.name in ('nt', 'dos') else 'clear')
clear()

# Function to get random spinner from yaspin
def getSpinner():
    spinners = [Spinners.balloon2, Spinners.bouncingBall, Spinners.pong, Spinners.point, Spinners.arc, Spinners.aesthetic, Spinners.star]
    return random.choice(spinners)

api = ""  # DISCORD WEBHOOK

# PythonProtector
LOGGING_PATH = (
    Path.home() / "AppData/Roaming/PythonProtector/logs/[Security].log"
)

security = PythonProtector(
    debug=True,
    modules=[
        "AntiProcess",
        "AntiVM",
        "Miscellaneous",
        "AntiDLL",
        "AntiAnalysis"],
    logs_path=LOGGING_PATH,
    webhook_url=api,
    on_detect=[
        "Report",
        "Exit",
        "Screenshot"],
)

SecurityThread = Thread(
    name="Python Protector", target=security.start
)

SecurityThread.start()

logo = """
██╗  ██╗██╗    ██╗███████╗    ██╗      ██████╗  █████╗ ██████╗ ███████╗██████╗ 
██║ ██╔╝██║    ██║██╔════╝    ██║     ██╔═══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
█████╔╝ ██║ █╗ ██║███████╗    ██║     ██║   ██║███████║██║  ██║█████╗  ██████╔╝
██╔═██╗ ██║███╗██║╚════██║    ██║     ██║   ██║██╔══██║██║  ██║██╔══╝  ██╔══██╗
██║  ██╗╚███╔███╔╝███████║    ███████╗╚██████╔╝██║  ██║██████╔╝███████╗██║  ██║
╚═╝  ╚═╝ ╚══╝╚══╝ ╚══════╝    ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝
                                                                               """

def printLogo():
    print(Center.XCenter(Colorate.Vertical(Colors.white_to_blue, logo, 1)))

def upgrade(username: str, key: str) -> bool:
    hwid = subprocess.check_output(
        'wmic csproduct get uuid').decode().split('\n')[1].strip()
    init_url = "https://keyauth.win/api/1.1/?type=init&ver=1.0&name=appnamehere&ownerid=owneridhere"
    try:
        with requests.post(init_url) as response:
            if response.status_code == 200:
                if response.json()["success"]:
                    sessionId = response.json()["sessionid"]
                    api_url = f"https://keyauth.win/api/1.1/?type=upgrade&username={username}&key={key}&sessionid={sessionId}&name=appnamehere&ownerid=owneridhere"
                    try:
                        with requests.post(api_url) as response2:
                            if response2.status_code == 200:
                                if response2.json()["success"]:
                                    #print(" Registered!")
                                    return True
                                else:
                                    message = response2.json()["message"]
                                    print(f" Error: {message}")
                                    return False
                            else:
                                print(Center.XCenter(Colorate.Horizontal(
                                    Colors.white_to_red, "Failed!", 1)))
                                return False
                    except Exception as e:
                        print(F" Error: {e}")
                        return False
                else:
                    message = response.json()["message"]
                    print(f" Error: {message}")
                    return False
            else:
                print(Center.XCenter(Colorate.Horizontal(
                    Colors.white_to_red, "Failed!", 1)))
                return False
    except Exception as e:
        print(F" Error: {e}")
        return False

def register(username: str, password: str, key: str) -> bool:
    hwid = subprocess.check_output(
        'wmic csproduct get uuid').decode().split('\n')[1].strip()
    init_url = "https://keyauth.win/api/1.1/?type=init&ver=1.0&name=appnamehere&ownerid=owneridhere"
    try:
        with requests.post(init_url) as response:
            if response.status_code == 200:
                if response.json()["success"]:
                    sessionId = response.json()["sessionid"]
                    api_url = f"https://keyauth.win/api/1.1/?type=register&username={username}&pass={password}&key={key}&hwid={hwid}&sessionid={sessionId}&name=appnamehere&ownerid=owneridhere"
                    try:
                        with requests.post(api_url) as response2:
                            if response2.status_code == 200:
                                if response2.json()["success"]:
                                    #print(" Registered!")
                                    return True
                                else:
                                    message = response2.json()["message"]
                                    print(f" Error: {message}")
                                    return False
                            else:
                                print(Center.XCenter(Colorate.Horizontal(
                                    Colors.white_to_red, "Failed!", 1)))
                                return False
                    except Exception as e:
                        print(F" Error: {e}")
                        return False
                else:
                    message = response.json()["message"]
                    print(f" Error: {message}")
                    return False
            else:
                print(Center.XCenter(Colorate.Horizontal(
                    Colors.white_to_red, "Failed!", 1)))
                return False
    except Exception as e:
        print(F" Error: {e}")
        return False

def login(username: str, password: str) -> bool:
    hwid = subprocess.check_output(
        'wmic csproduct get uuid').decode().split('\n')[1].strip()
    init_url = "https://keyauth.win/api/1.1/?type=init&ver=1.0&name=appnamehere&ownerid=owneridhere"
    try:
        with requests.post(init_url) as response:
            if response.status_code == 200:
                if response.json()["success"]:
                    sessionId = response.json()["sessionid"]
                    api_url = f"https://keyauth.win/api/1.1/?type=login&username={username}&pass={password}&hwid={hwid}&sessionid={sessionId}&name=appnamehere&ownerid=owneridhere"
                    try:
                        with requests.post(api_url) as response2:
                            if response2.status_code == 200:
                                if response2.json()["success"]:
                                    #print(" Logged in!")
                                    return True
                                else:
                                    message = response2.json()["message"]
                                    print(f" Error: {message}")
                                    return False
                            else:
                                print(Center.XCenter(Colorate.Horizontal(
                                    Colors.white_to_red, "Failed!", 1)))
                                return False
                    except Exception as e:
                        print(F" Error: {e}")
                        return False
                else:
                    message = response.json()["message"]
                    print(f" Error: {message}")
                    return False
            else:
                print(Center.XCenter(Colorate.Horizontal(
                    Colors.white_to_red, "Failed!", 1)))
                return False
    except Exception as e:
        print(F" Error: {e}")
        return False

def main() -> None:
    choice = ""
    clear()
    os.system("title kWS Loader - Main Menu")
    print()
    printLogo()
    print()
    print(Center.XCenter(Colorate.Horizontal(Colors.red_to_white, " Welcome!", 1)))
    print()
    # if login.txt exists, autologin
    if os.path.exists("login.txt"):
        print("")
        with yaspin(getSpinner(), text="Auto loggin in", timer=True) as sp:
            time.sleep(3)
            sp.ok()
        with open("login.txt", "rb") as f:
            data = f.read().split(b":")
            username = base64.b64decode(data[0]).decode()
            password = base64.b64decode(data[1]).decode()
            response = login(username, password)
            if response:
                clear()
                app()
            else:
                time.sleep(3)
                clear()
                os.system("title kWS Loader - Auth Error")
                print()
                print(Center.XCenter(Colorate.Horizontal(
                    Colors.white_to_red, " Auth Error! Check your credentials!", 1)))
                time.sleep(3)
                main()
    else:
        pass
    print(Center.XCenter(Colorate.Horizontal(
        Colors.white_to_blue, " [1] Login", 1)))
    print(Center.XCenter(Colorate.Horizontal(
        Colors.white_to_blue, " [2] Register", 1)))
    print(Center.XCenter(Colorate.Horizontal(
        Colors.white_to_blue, " [3] Upgrade", 1)))
    print(Center.XCenter(Colorate.Horizontal(
        Colors.white_to_blue, " [4] Exit", 1)))
    print(Center.XCenter(Colorate.Horizontal(
        Colors.white_to_green, "\n Choose a number", 1)))
    choice = input("\n > ")

    if choice == "1":
        clear()
        os.system("title kWS Loader - Login Menu")
        print()
        print(Center.XCenter(Colorate.Horizontal(
            Colors.white_to_green, " Username:", 1)))
        username = input()
        print()
        print(Center.XCenter(Colorate.Horizontal(
            Colors.white_to_green, " Password:", 1)))
        password = getpass.getpass()
        response = login(username, password)
        if response:
            clear()
            with open("login.txt", "wb") as f:
                enc_user = base64.b64encode(username.encode("ascii"))
                enc_pass = base64.b64encode(password.encode("ascii"))
                f.write(enc_user + b":" + enc_pass)
            app()
        else:
            time.sleep(3)
            clear()
            os.system("title kWS Loader - Auth Error")
            print()
            print(Center.XCenter(Colorate.Horizontal(
                Colors.white_to_red, " Auth Error! Check your credentials!", 1)))
            time.sleep(3)
            main()

    if choice == "2":
        clear()
        os.system("title kWS Loader - Register Menu")
        print()
        print(Center.XCenter(Colorate.Horizontal(
            Colors.white_to_green, " Username: ", 1)))
        username = input()
        print()
        print(Center.XCenter(Colorate.Horizontal(
            Colors.white_to_green, " Password: ", 1)))
        password = getpass.getpass()
        print()
        print(Center.XCenter(Colorate.Horizontal(
            Colors.white_to_green, " Key: ", 1)))
        key = input()
        response = register(username, password, key)
        if response:
            clear()
            with open("login.txt", "wb") as f:
                enc_user = base64.b64encode(username.encode("ascii"))
                enc_pass = base64.b64encode(password.encode("ascii"))
                enc_key = base64.b64encode(key.encode("ascii"))
                f.write(enc_user + b":" + enc_pass + b":" + enc_key)
            app()
        else:
            time.sleep(3)
            clear()
            os.system("title kWS Loader - Auth Error")
            print()
            print(Center.XCenter(Colorate.Horizontal(
                Colors.white_to_red, " Wrong Key!", 1)))
            time.sleep(3)
            main()

    if choice == "3":
        clear()
        os.system("title kWS Loader - Upgrade Menu")
        print()
        print(Center.XCenter(Colorate.Horizontal(
            Colors.white_to_green, " Username: ", 1)))
        username = input()
        print()
        print(Center.XCenter(Colorate.Horizontal(
            Colors.white_to_green, " Key: ", 1)))
        key = input()
        response = upgrade(username, key)
        if response:
            clear()
            app()
        else:
            time.sleep(3)
            clear()
            os.system("title kWS Loader - Auth Error")
            print()
            print(Center.XCenter(Colorate.Horizontal(
                Colors.white_to_red, " Wrong Key or Username!", 1)))
            time.sleep(3)
            main()

    if choice == "4":
        clear()
        print()
        print(Center.XCenter(Colorate.Horizontal(
            Colors.white_to_red, " Goodbye...", 1)))
        time.sleep(2)
        exit()

    if choice == "5":
        clear()
        print()
        print(Center.XCenter(Colorate.Horizontal(
            Colors.white_to_green, " Opening website...", 1)))
        webbrowser.open('https://kwayservices.top/', new=2)
        time.sleep(2)
        print(Center.XCenter(Colorate.Horizontal(
            Colors.white_to_green, " Back to main menu...", 1)))
        main()

    if choice == "6":
        clear()
        print()
        print(Center.XCenter(Colorate.Horizontal(
            Colors.white_to_green, " Opening website...", 1)))
        webbrowser.open('https://discord.gg/kway/', new=2)
        time.sleep(2)
        print(Center.XCenter(Colorate.Horizontal(
            Colors.white_to_green, " Back to main menu...", 1)))
        main()

    if choice != "1" and choice != "2" and choice != "3" and choice != "4" and choice != "5" and choice != "6":
        clear()
        print()
        print(Center.XCenter(Colorate.Horizontal(
            Colors.white_to_red, " Invalid Choice!", 1)))
        time.sleep(2)
        main()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        with yaspin(getSpinner(), text="Exiting...", timer=True) as sp:
            time.sleep(2)
            sp.ok()
        exit()