import pandas as pd
from helpers import listFiles, nameTrimmer
from settings import pathSettings

class fileInput():

    def __init__(self):
        pass

    def newPreliminarSettings(self, df):
        """
    NEW type has different settings, and therefore cannot be standardized alongside the other datasets.
    We will merge rows 0 and 2, and leave 2 rows before the start of the data.
        """
        index = [x for x in range(df.shape[0])]  # list of columns' integer indices
        index.remove(2)
        index.insert(0,2)
        df = df.reindex(index).reset_index(drop=True)
        for i in df.columns[6:].to_list():
            df.loc[2,i] = str(df.loc[2,i]) + " - " + str(df.loc[0,i])  # Merge rows

            return df

    def rawfileReader(self,Input):
        """
    rawfileReader will iterate over the raw files in each folder, perform each file's transformation and return a dict with
    all the datasets names of that specific week as keys. The values will be the dataframes.

    Args

    week_no: Input integer of the week to transform
    folder_input: Location of raw files. Since the script is iterating over files in folder, only the folder is defined
    mypath: Rawfile folder locationm
    le: empty dictionary
        """
        datasets = dict()

        file_names = listFiles(Input)
        for file in file_names:
            print("Logged", file)

            dataframe = pd.read_excel(pathSettings.Input+file, decimal=',')
            file_type = nameTrimmer(file) #Regex for Type column

            datasets[file_type] = dataframe # Store in "le" dict
            datasets[file_type]['TYPE'] = file_type # Set "TYPE" column as brand type

            if file_type.endswith("NEW"):
                self.newPreliminarSettings(datasets[file_type]) # NEW will need different settings

        # Now all files should be in the same format to start the transformation.
        # We will store them in a dict.
        dframes = {k:pd.DataFrame(v) for k,v in datasets.items()}

        return dframes
