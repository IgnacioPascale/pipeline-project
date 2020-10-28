import configparser

config = configparser.ConfigParser()
WeekNumber = input("Week Number: ")

class ftpSettings():

    def __init__(self):
        pass
    config.read('ftpConfig.ini')

    user = config['credentials']['user']
    password = config['credentials']['password']
    server = config['server']['host']

    Ext = config['load']['ext']
    FileName = config['load']['file_name']+WeekNumber+Ext
    Input = config['load']['input'] + FileName
    Output = config['load']['output']

class pathSettings():
    def __init__(self):
        pass

    config.read('pathConfig.ini')
    ini_Input =config['path']['input']
    Input = ini_Input+ WeekNumber + "/"
    Output =config['path']['output']
    Ext = config['path']['ext']
    ini_FileName= config['path']['file_name']
    FileName = ini_FileName+WeekNumber+Ext
