# Data Pipeline

## Introduction

This company used to send 5 or 6 different files each week. These are:

- `APP`
- `APP Online` (not very usual)
- `PC BOX`
- `BEEP BOX`
- `LFC`
- `NEW`

This pipeline receives raw data on ftp, downloads the file on the local server, performs transformations and outputs one file with the normalised data on the local server and the ftp server.

## Structure

The pipeline consists of the following modules:

- `load.py` where all the ftp related methods are stored under the FtpLoad class.
- `extraction.py` class `FileInput` contains all the methods related to reading and performing preliminar transformations over the dataframes
- `transformation.py` contains all related classes and methods with the transformation, normalisation and export of the files.
- `helpers.py` methods used throughout the code.
- `settings.py` contains classes that read ".ini" files* and stored all ftp and local server paths, file names, week number, extensions, etc. Will delve into this later on in the README.
- `main.py`

### What is missing?

In order to read the stored paths, .ini files that contain this information are needed in place for the pipeline to work. These should be:

- `ftpConfigTicnova.ini` contains all related paths through the ftp server
- `pathConfigTicnova.ini` which contains all related paths through the local server

The .ini files were not committed for security reasons. These will be shared in a different way.

## Raw files

In this section we will delve into the specific format of each file and how we approach the normalisation. Please bare in mind that the pictures shown below are mere **examples** and do not contain real data. The exact name of the columns have been changed as well, as this is only necessary for explaining purposes.

### Format

The partner provides files as depicted below:

![1][]

As it can be seen, it uses the first 6 columns for product data. From the 7th column onwards, it provides sales data, with the Store name on the top x intercept, matching "Quantity" and "Revenue" values on the y intercept from the left-hand side, depicting a shape similar to that of a matrix. It then provides "Total" sum of values for both "Quantity" and "Revenue" in the y-intercept from the right-hand side, and a total sum of sales per store in the bottom x-intercept.

### "NEW" type

Unfortunately, not all files are the same. The last type mentioned in the introduction ("NEW") has a slightly difference input, as depicted below:

![2][]

In this case, the difference is that the main idenfifier of the Store is in the row in which other files contain the full name of it. Then, the name of the stores are found one row below. In the code, we find a way of merging this particular case.

### "BOX" types

Contrary to the other file types, those whose name end in box provide a slightly different lay out, as depicted below:

![3][]

It can be appreciated in this picture that the order of "revenue" and "quantity" are in a different order. In all the other types, the column "Quantity" comes first, and "Revenue" afterwards. In this case, it is the opposite.

## Transformation

### initializing

To run the process you need to run `main.py`. Open the console in the location, and run the following:

```shell
python main.py
```

When running the script, there will be an input for the required week of data. This will show up as:

```shell
Week Number: 29
```

Typing the number of the week whose files we want to transform will initialize de process.

### Input

All files will be found in the local ftp. The methods associated with `load.py` loop over these file names and extract them in the local server. Then, the methods in `extraction.py` will first rename the files (by slicing over the numbers before "*_SEMANA") and store the datasets in dictionaries with "file type" ("app", "new", etc) as keys and data frames as values.

```shell
Logged XXXXXXXXXXXXXXXXX_SEMANA 29-2020 PC BOX.xlsx
Logged XXXXXXXXXXXXXXXXX_SEMANA 29-2020 LFC.xlsx
Logged XXXXXXXXXXXXXXXXX_SEMANA 29-2020 BEEP BOX.xlsx
Logged XXXXXXXXXXXXXXXXX_SEMANA 29-2020 NEW.xlsx
Logged XXXXXXXXXXXXXXXXX_SEMANA 29-2020 APP.xlsx
Successfully downloaded XXXXXXXXXXXXXXXXX_SEMANA 29-2020 PC BOX.xlsx
Successfully downloaded XXXXXXXXXXXXXXXXX_SEMANA 29-2020 LFC.xlsx
Successfully downloaded XXXXXXXXXXXXXXXXX_SEMANA 29-2020 BEEP BOX.xlsx
Successfully downloaded XXXXXXXXXXXXXXXXX_SEMANA 29-2020 NEW.xlsx
Successfully downloaded XXXXXXXXXXXXXXXXX_SEMANA 29-2020 APP.xlsx

XXXXXXXXXXXXXXXXX_SEMANA 29-2020 PC BOX.xlsx was renamed to SEMANA 29-2020 PC BOX.xlsx
XXXXXXXXXXXXXXXXX_SEMANA 29-2020 LFC.xlsx was renamed to SEMANA 29-2020 LFC.xlsx
XXXXXXXXXXXXXXXXX_SEMANA 29-2020 BEEP BOX.xlsx was renamed to SEMANA 29-2020 BEEP BOX.xlsx
XXXXXXXXXXXXXXXXX_SEMANA 29-2020 NEW.xlsx was renamed to SEMANA 29-2020 NEW.xlsx
XXXXXXXXXXXXXXXXX_SEMANA 29-2020 APP.xlsx was renamed to SEMANA 29-2020 APP.xlsx


```

### Process

The process consists on a single transformation procedure that will loop over the dictionary containing all data frames.

1. Establish preliminar settings to standardise the datasets
2. Bifurcate the process:
   1. Details: data set with product data (First 6 columns)
   2. Prep: data set with sales data in both units and revenue. (Column 7 until column N)

### Details

1. Get Type column (last column) from the dataset.
2. Get first 6 columns (details) and merge with type
3. Apply `get_detail` method. This will perform all required transformations for this part of the dataset

### Prep

1. Apply `prep_file` method. This will perform all required transformations for this part of the dataset
2. Set Quantity and Revenue columns. If the key ends with "BOX", we know the Revenue comes first and quantity after. If not, it's the opposite. We will have 2  different datasets (pricing and units)
3. Concat these dataframes and remove unnecessary columns and Null values.

### Final Merge

1. Merge details and prep data frames and we get the final and normalised data frame.
2. Save the data frames into a dictionary similar to the starting one.

### Output

Once the transformation is done, the method `export_data` in `extraction.py` will place the final file in the local server. Soon after, the method `load_file` will upload the final file in the ftp server.

This is what the process looks like on the shell

```shell
Logged SEMANA 29-2020 APP.xlsx
Logged SEMANA 29-2020 BEEP BOX.xlsx
Logged SEMANA 29-2020 LFC.xlsx
Logged SEMANA 29-2020 NEW.xlsx
Logged SEMANA 29-2020 PC BOX.xlsx

transforming... APP
transforming... BEEP BOX
transforming... LFC
transforming... NEW
transforming... PC BOX

xxxx.csv was succesfully exported to //.../transformed/
xxxx.csv was loaded successfully on ftp /.../transformed/
```

## Quality Check

The method `quality_check(final_df)` will deliver a comparison between the summary of the units and revenue between the rawfiles and the normalised output. It will show up as follows:

```shell
-----------
APP Quality Check - Week:  29
          File   Units        Revenue
0     Original  XXXX            XXXX
1  Transformed  YYYY            YYYY
------------
PC BOX Quality Check - Week:  29
          File   Units        Revenue
0     Original  XXXX            XXXX
1  Transformed  YYYY            YYYY
------------
BEEP BOX Quality Check - Week:  29
          File   Units        Revenue
0     Original  XXXX            XXXX
1  Transformed  YYYY            YYYY
------------
NEW Quality Check - Week:  29
          File   Units        Revenue
0     Original  XXXX            XXXX
1  Transformed  YYYY            YYYY
------------
LFC Quality Check - Week:  29
          File   Units        Revenue
0     Original  XXXX            XXXX
1  Transformed  YYYY            YYYY

```

## Potential issues

It is likely that, in some occasions, the QC won't find matches between the raw files (original) and the normalised files (transformed).

After thorough checking, it was found that the data provided by the partner is not always accurate: in some cases, **they do not sum the units/revenue correctly** in their excel files.

That being said, if there is a mismatch between the raw file and the transformed file, bare in mind that most likely the partner's file will have this issue. But it's always worth checking.


[1]: https://i.ibb.co/3rkDSRn/Captura-de-pantalla-2020-08-07-a-las-12-27-12.png
[2]: https://i.ibb.co/0jfqBXF/Captura-de-pantalla-2020-08-07-a-las-12-27-31.png
[3]: https://i.ibb.co/VgJ9QP5/Captura-de-pantalla-2020-08-07-a-las-12-27-40.png
