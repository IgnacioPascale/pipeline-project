from settings import *
from extraction import FileInput
from transformation import Transform, Export
from load import FtpLoad
from quality_check import QualityCheck as qc

if __name__ == "__main__":

    # Slice lines and download files from ftp
    lines = FtpLoad().get_lines(FtpSettings.ftp_input)
    download = FtpLoad().slice(lines, WeekNumber)

    for i in download:
        FtpLoad().download_file(i, FtpSettings.ftp_input, PathSettings.ini_Input, WeekNumber)

    # Rename files
    FtpLoad().rename_files(PathSettings.ini_Input, WeekNumber)

    # Transform files
    dframes = FileInput().rawfile_reader(PathSettings.input)
    results = Transform().transform_files(dframes)

    # Quality Check
    qc().show_summary(results)

    # Export results
    Export().export_data(results, PathSettings.output, PathSettings.file_name)
    FtpLoad().load_file(FtpSettings.input, FtpSettings.output, FtpSettings.file_name)
