import os, configparser,requests

config = configparser.ConfigParser()
config.read('../config.conf')

githubVersion = requests.get("https://raw.githubusercontent.com/YuuKomoe/TailsChecker/main/utils/version")
version = githubVersion.text.replace("\n","")

with open('./version', 'w') as file:
    file.write(version)

with open('../tails.py', 'w') as file:
    file.write(file)

# os.rename('../tails.py','old_tails.py')
# os.rename('../tails_new','tails.py')

# if os.path.isfile('../old_tails.py'):
#     os.remove('../old_tails.py')

# with open ('../config.tails', 'w') as file:
#    config.write(file)

os.system('python ../tails.py')