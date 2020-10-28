from settings import pathSettings, ftpSettings
from extraction import fileInput
from transformation import transform, export
from load import ftpLoad

if __name__ == "__main__":
    dframes = fileInput().rawfileReader(pathSettings.Input)
    results = transform().transformFiles(dframes)
    transform().showResults(results)
    export().exportData(results,pathSettings.Output,pathSettings.FileName)
    ftpLoad().loadFile(ftpSettings.server,ftpSettings.user,ftpSettings.password,ftpSettings.Input,ftpSettings.Output,ftpSettings.FileName)
