import os, configparser,requests

config = configparser.ConfigParser()
config.read('../config.conf')

githubVersion = requests.get("https://raw.githubusercontent.com/HoneycubeYay/TailsChecker/beta/utils/version")
version = githubVersion.text.replace("\n","")

with open('./version', 'w') as file:
    file.write(version)

with open('../tails.py', 'w') as file:
    file.write(file)

os.system('python ../tails.py')
