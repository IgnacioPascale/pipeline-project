import ftplib
from settings import *
import os
import re
from helpers import *

class FtpLoad:
    def __init__(self):
        pass

    def connect(self):
        ftp = ftplib.FTP(FtpSettings.server)
        ftp.login(FtpSettings.user, FtpSettings.password)

        return ftp

    def get_lines(self, ftp_dir):

        lines = list()

        try:
            ftp = self.connect()
            ftp.dir(ftp_dir, lines.append)
        except:
            print('Could not log directory', ftp_dir)
            pass

        return lines

    def slice(self, lines, week_no):

        file_type = ["APP", "NEW", "BEEP BOX", "LFC", "PC BOX", "APP ONLINE"]
        download = []

        for i in lines:
            for t in file_type:

                asd = re.compile("[0-9]+_SEMANA " + week_no + "-2020 " + t + ".xlsx")

                try:
                    file = asd.findall(i)[0]
                    download.append(file)
                    print("Logged", file)

                except:
                    pass

        return download


    def download_file(self, file_name, ftp_dir, dir_local,week):
        ftp = self.connect()
        ftp.cwd(ftp_dir)

        if not os.path.exists(dir_local+week):
            os.makedirs(dir_local+week)

        with open(file_name, "wb") as file:
            try:
                frame = ftp.retrbinary("RETR " + file_name,
                                       open(dir_local+week + "//" + file_name, 'wb').write)
                print('Successfully downloaded', file_name)
            except:
                print('Could not download', file_name)

    def load_file(self, input, output, file_name):
        with open(input, "rb") as file:

            ftp = self.connect()
            ftp.cwd(output)

            try:
                ftp.storbinary("STOR " + file_name, file)
                print(file_name,"was loaded successfully on", output)
            except:
                print('Could not upload', file_name)
                pass
            ftp.quit()
            file.close()

    def rename_files(self, local_dir, week_no):
        files = list_files(local_dir + week_no)
        file_type = ["APP", "NEW", "BEEP BOX", "LFC", "PC BOX", "APP ONLINE"]

        for f in files:
            for t in file_type:
                regex = re.compile("[0-9]+_(SEMANA " + week_no + "-2020 " + t + ".xlsx)")

                try:
                    new_name = regex.findall(f)[0]
                    os.rename(local_dir + week_no + "/" + f, local_dir + week_no + "/" + new_name)
                    print(f, "was renamed to", new_name)

                except:
                    pass