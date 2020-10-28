from settings import pathSettings, ftpSettings
from ticnovaExtraction import fileInput
from ticnovaTransformation import transform, export
from ticnovaLoad import ftpLoad

if __name__ == "__main__":
    dframes = fileInput().rawfileReader(pathSettings.Input)
    results = transform().transformFiles(dframes)
    transform().showResults(results)
    export().exportData(results,pathSettings.Output,pathSettings.FileName)
    ftpLoad().loadFile(ftpSettings.server,ftpSettings.user,ftpSettings.password,ftpSettings.Input,ftpSettings.Output,ftpSettings.FileName)
