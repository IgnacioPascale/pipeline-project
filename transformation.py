# basic lib
import pandas as pd

class transform():
    def __init__(self):
        pass
    
    def preSet(self,df):
        """
        preSet will establish the preliminar settings for each dataframe.
        It receives a dataframe and returns the transformed version of it. 
        Since the "File Reader" already standardized all the datasets in the dict, the methodology will be the same for each of them.

        """
        df.drop(df.head(2).index, inplace=True) # delete first 2 rows
        df.drop(df.tail(1).index, inplace=True) # delete last row
        df = df.iloc[:,0:len(df.columns)-3] # delete last 3 columns
        # Some files only provide one store every 2 columns. We need the names in both columns.
        df.iloc[0,:] = df.iloc[0,:].fillna(method='ffill')

        return df

    def prepFile(self, df):
        """
        prep will contain all columns with sale info and the third column which contains PARTNER_PRODUCT_CODE

        """
        df = pd.concat([df.iloc[:,2], df.iloc[:,6:len(df.columns)]], axis=1)
        df.iloc[0,0] = 'PARTNER_PRODUCT_CODE' # Set_Value is deprecated 15/05
    
        df.columns = df.iloc[0,:].tolist() # Rename columns
        df.drop(df.head(2).index, inplace=True) # Eliminate first 2 rows
        df = df.fillna("") # Convert all "NaN" into blank spaces

        return df

    def getDetail(self,df):

        df.columns = ['CATEGORY_LEVEL_1','CATEGORY_LEVEL_2','PARTNER_PRODUCT_CODE','PRODUCT_NAME','MANUFACTURER_PART_NUMBER','BRAND_CODE','TYPE']
        df.drop(df.head(2).index, inplace=True) #Eliminate first 2 rows
        df.iloc[:,0:2] = df.iloc[:,0:2].fillna(method='ffill') # Fill gaps in cat columns
        # Make sure there are no extra product codes ruining our script
        df = df.drop_duplicates(subset='PARTNER_PRODUCT_CODE',keep='first')
        
        return df

    def setPrice(self,df):
        df = df.set_index(df.columns[0])
        df = df.stack().reset_index() # Stack() will normalize the frame
        df.columns = ['PARTNER_PRODUCT_CODE','STORES','SALES_REVENUE']

        return df

    def setUnit(self,df):
        df = df.set_index(df.columns[0])
        df = df.stack().reset_index()
        df.columns = ['PARTNER_PRODUCT_CODE','STORES','SALES_QUANTITY']

        return df


    def stores(self,pricing, units, column_numbers):
        # Merge dataframes
        df = pd.concat([pricing,units], join='inner', axis = 1)
            # Columns 3 and 4 will be repeated and we don't want them there. 
            ##Since they have the same name as columns 1 and 2, we need to eliminate them in an unthordoxed way.
             ## That is using.iloc with a list that does not cotain those columns
        column_numbers = [x for x in range(df.shape[1])]  # list of columns' integer indices
        column_numbers.remove(3)
        column_numbers.remove(4)
            # We will also eliminate empty spaces
        df = df[df['SALES_REVENUE']!=""].iloc[:, column_numbers]

        return df

    def getLastColumn(self, df):
        lastColumn = df.iloc[:,len(df.columns)-1]

        return lastColumn


    def showResults(self,df):
        df = df.loc[:,['TYPE','SALES_QUANTITY','SALES_REVENUE']].groupby('TYPE').sum()
        print(df)
    
    def dictToFrame(self, dictionary):
        df = pd.concat(dictionary[i] for i in dictionary.keys())
        return df
   

    def transformFiles(self, dframes):

        """
        transformFiles will perform the transformation process.
        This function will utilize the previously mentioned methods.
        It receives a dictionary with filenames as keys and dataframes as values.
        It will return a complete dataFrame with the normalized data.
        """

        details = dict()
        prep = dict()
        pricing = dict()
        units = dict()
        stores_pp = dict()
        column_numbers = dict()
        final = dict()
        types = dict()


        for k in dframes.keys():
        # Preliminar settings

            print("transforming...", k)
            # Save "type" column for further merge with details
            # This column is eliminated when using preSet
            types[k] = dframes[k].iloc[:,len(dframes[k].columns)-1]
            # Establish preliminar settings to standardize the datasets.

            dframes[k] = self.preSet(dframes[k])

            # From here there will be a bifurcation in datasets:
            #       Details: with product data
            #       Prep: with sales data in both units and revenue.

            # In details:
            #       - merge type column with the rest
            #       - apply "details" transformation
            details[k] = pd.concat([dframes[k].iloc[:,0:6], types[k]],axis=1)
            details[k] = self.getDetail(details[k])

            # In Prep:
            #       - apply "prep" transformation
            #       - apply both units and price transformation and bifurcate again in 2 different dataFrames.
            prep[k] = self.prepFile(dframes[k])

            # "BOX" files will have Rev,Qty and so on
            # The rest will have Qty,Rev and so on.

            if k.endswith("BOX"):
                units[k] = prep[k].iloc[:,0:len(prep[k].columns):2] # Starting from the first column, take each column every 2 columns
                pricing[k] = pd.concat([prep[k].iloc[:,0], prep[k].iloc[:,1:len(prep[k].columns):2]], axis=1)
            else:
                pricing[k] = prep[k].iloc[:,0:len(prep[k].columns):2]
                units[k] = pd.concat([prep[k].iloc[:,0], prep[k].iloc[:,1:len(prep[k].columns):2]], axis=1) # Starting from the 2nd column, take each column every 2 columns. Also add the PARTNER_PRODUCT_CODE

            pricing[k] = self.setPrice(pricing[k])
            units[k] = self.setUnit(units[k])


            # Merge dataframes
            stores_pp[k] = pd.concat([pricing[k],units[k]], join='inner', axis = 1)
            column_numbers[k] = [x for x in range(stores_pp[k].shape[1])]  # list of columns' integer indices
            column_numbers[k].remove(3)
            column_numbers[k].remove(4)
            stores_pp[k] = stores_pp[k][stores_pp[k]['SALES_REVENUE']!=""].iloc[:, column_numbers[k]]

            #stores_pp[k] =self.stores(pricing[k],units[k],column_numbers[k])

        # Final merge
            final[k] = pd.merge(details[k], stores_pp[k], how='inner', on='PARTNER_PRODUCT_CODE')
        
        
        week = self.dictToFrame(final)

        return week

class export():
    def __init__(self):
        pass

    def exportData(self,df,Output,FileName):
        df.to_csv(Output+FileName,index=False, decimal=".", sep='|')
        print(FileName,'was succesfully exported to', Output)
