import configparser

config = configparser.ConfigParser()
WeekNumber = input("Week Number: ")

class FtpSettings:


    config.read('ftpConfig.ini')

    user = config['credentials']['user']
    password = config['credentials']['password']
    server = config['server']['host']

    ext = config['load']['ext']
    file_name = config['load']['file_name'] + WeekNumber + ext
    input = config['load']['input'] + file_name
    output = config['load']['output']
    ftp_input = config['load']['ftp_input']

class PathSettings:

    config.read('pathConfig.ini')
    ini_Input = config['path']['input']
    input = ini_Input + WeekNumber + "/"
    output = config['path']['output']
    ext = config['path']['ext']
    ini_FileName= config['path']['file_name']
    file_name = ini_FileName + WeekNumber + ext

class RawFiles:

    file_types = ['APP', 'APP ON LINE', 'PC BOX', 'BEEP BOX', 'NEW', 'LFC']