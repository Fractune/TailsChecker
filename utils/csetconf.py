class Config:
    global auto_start, check_updates, threads, retries, mail_access, hide_passwords, print_bad, save_bad, proxy_protocol, proxy_dupe, proxy_bad, debugging, dev_mode
    f = str(open('./config.conf', 'r', encoding="UTF-8", errors="ignore").readlines()).strip()

    auto_start = f.split("auto_start: ")[1].split("'")[0][:-2]
    if auto_start == "true":
        auto_start = True
    else: 
        auto_Start = False
    check_updates = f.split("check_updates: ")[1].split("'")[0][:-2]
    if check_updates == "true":
        check_updates = True
    else:
        check_updates = False
    threads = f.split("threads: ")[1].split("'")[0][:-2]
    retries = f.split("retries: ")[1].split("'")[0][:-2]
    mail_access = f.split("mail_access: ")[1].split("'")[0][:-2]
    if mail_access == "true":
        mail_access = True
    else:
        mail_access = False
    hide_passwords = f.split("hide_passwords: ")[1].split("'")[0][:-2]
    if hide_passwords == "true":
        hide_passwords = True
    else:
        hide_pwds = False
    print_bad = f.split("print_bad: ")[1].split("'")[0][:-2]
    if print_bad == "true":
        print_bad = True
    else:
        print_bad = False
    save_bad = f.split("save_bad: ")[1].split("'")[0][:-2]
    if save_bad == "true":
        save_bad = True
    else:
        save_bad = False
    proxy = f.split("proxy: ")[1].split("'")[0][:-2]
    if proxy == "true":
        proxy = True
    else:
        proxy = False
    proxy_protocol = f.split("proxy_protocol: ")[1].split("'")[0][:-2]
    proxy_dupe = f.split("proxy_duplicates: ")[1].split("'")[0][:-2]
    if proxy_dupe == "true":
        proxy_dupe = True
    else:
        proxy_dupe = False
    proxy_bad = f.split("proxy_bad_remove: ")[1].split("'")[0][:-2]
    if proxy_bad == "true":
        proxy_bad = True
    else:
        proxy_bad = False
    debugging = f.split("debugging: ")[1].split("'")[0][:-2]
    if debugging == "true":
        debugging = True
    else:
        debugging = False
    dev_mode = f.split("dev_mode: ")[1].split("'")[0]
    if dev_mode == "true":
        dev_mode = True
    else:
        dev_mode = False
Config()