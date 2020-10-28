import ftplib
from settings import ftpSettings

class ftpLoad():
    def __init__(self):
        pass

    def loadFile(self,server,user,password,Input,Output,FileName):
        with open(Input, "rb") as file:

            ftp = ftplib.FTP(server)
            ftp.login(user,password)
            ftp.cwd(Output)

            try:
                ftp.storbinary("STOR " + FileName, file)
                print(FileName,"was loaded successfully on", Output)
            except:
                print('Could not upload', FileName)
                pass
            ftp.quit()
            file.close()

