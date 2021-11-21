from utils.csetconf import auto_start, check_updates, threads, retries, mail_access, hide_passwords, print_bad, save_bad, proxy_protocol, proxy_dupe, proxy_bad, debugging, dev_mode
from utils.colors import yellow, red, green, cyan, blue, white, magenta
from colorama import Fore, init, Style

class Details():
    global credits, announces, mark, autostart_config

    autostart_config = (f'''
{red}> {white}Auto start: {yellow}{auto_start}
{red}> {white}Check for updates: {yellow}{check_updates}
{red}> {white}Threads: {yellow}{threads}
{red}> {white}Retries: {yellow}{threads}
{red}> {white}Mail access: {yellow}{mail_access}
{red}> {white}Hide passwords: {yellow}{hide_passwords}
{red}> {white}print bad accs: {yellow}{print_bad}
{red}> {white}Save bad accs: {yellow}{save_bad}
{red}> {white}Proxy protocol: {yellow}{proxy_protocol}
{red}> {white}Proxy duplications: {yellow}{proxy_dupe}
{red}> {white}Proxy bad: {yellow}{proxy_bad}
{red}> {white}Debugging: {yellow}{debugging}
{red}> {white}Dev mode: {yellow}{dev_mode}
    ''')

    credits = (f'''
        Credits to Tails Development Team,

        Starlysh#0001 -- Half Developer, Ceo, dealing with minor changes.
        Lau#0001 -- Developer, Co-Ceo, dealing with big changes.
        decode#2634 -- Developer, Co-Ceo, dealing with intermediate changes.
    ''')

    announces = (f'''
        Whatsoever;
    ''')
Details()
