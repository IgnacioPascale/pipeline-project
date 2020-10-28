from os import listdir
from os.path import isfile, join #, isdir
import re

def nameTrimmer(file): #Trim file names to only file type
    file = file.lstrip('SEMANA ').rstrip(' .xlsx')
    file = re.sub(r'\d+', '', file).lstrip(' - ')

    return file

def listFiles(path): # List all files in a certain directory
    file_names = [x for x in listdir(path) if isfile(join(path, x))] #list of all folders
    try:
        file_names.remove('.DS_Store') # This is self-generated for some reason. Remove it from list.
    except:
        pass

    return file_names
