class Config:
    global auto_start, check_updates, threads, retries, mail_access, hide_passwords, print_bad, save_bad, proxy_type, proxy_dupe, proxy_bad, debugging, dev_mode
    f = str(open('./config.conf', 'r', encoding="UTF-8", errors="ignore").readlines()).strip()

    auto_start = f.split("auto_start: ")[1].split("'")[0][:-2]
    check_updates = f.split("check_updates: ")[1].split("'")[0][:-2]
    threads = f.split("threads: ")[1].split("'")[0][:-2]
    retries = f.split("retries: ")[1].split("'")[0][:-2]
    mail_access = f.split("mail_access: ")[1].split("'")[0][:-2]
    hide_passwords = f.split("hide_passwords: ")[1].split("'")[0][:-2]
    print_bad = f.split("print_bad: ")[1].split("'")[0][:-2]
    save_bad = f.split("save_bad: ")[1].split("'")[0][:-2]
    proxy = f.split("proxy: ")[1].split("'")[0][:-2]
    proxy_type = f.split("proxy_type: ")[1].split("'")[0]
    proxy_dupe = f.split("proxy_duplicates: ")[1].split("'")[0][:-2]
    proxy_bad = f.split("proxy_bad_remove: ")[1].split("'")[0][:-2]
    debugging = f.split("debugging: ")[1].split("'")[0][:-2]
    dev_mode = f.split("dev_mode: ")[1].split("'")[0]
Config()