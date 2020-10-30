from settings import *
import pandas as pd

class QualityCheck:

    file_types = ['APP','APP ON LINE','PC BOX','BEEP BOX','NEW','LFC']

    def read_files(self, file_types, path, week_no):

        df_dict = dict()
        for i in file_types:
            try:
                df = pd.read_excel(path + "/SEMANA " + week_no + "-2020 " + i + ".xlsx", decimal=',')
                df_dict[i] = df
                pass

            except:
                pass

        return df_dict

    def column_numbers(self, df):

        column_numbers = [x for x in range(df.shape[1])]
        return column_numbers

    def row_numbers(self, df):

        row_numbers = [y for y in range(df.shape[0])]
        return row_numbers

    def show_summary(self, final_df):

        dframes = self.read_files(self.file_types, PathSettings.input, WeekNumber)
        for i in list(dframes.keys()):

            index = self.row_numbers(dframes[i])
            column_numbers = self.column_numbers(dframes[i])

            try:
                print('------------')
                print(i, "Quality Check - Week: ", WeekNumber)

                # Get either revenue or quantity in raw files
                x = dframes[i].iloc[len(index)-1, len(column_numbers)-2]
                y = dframes[i].iloc[len(index)-1, len(column_numbers)-1]

                units_tr = final_df[final_df['TYPE'] == i].loc[:, ['SALES_QUANTITY']].sum().tolist()[0]
                rev_tr = final_df[final_df['TYPE'] == i].loc[:, ['SALES_REVENUE']].sum().tolist()[0]

                if i.endswith("BOX"):
                    units_or = y
                    rev_or = x
                else:
                    units_or = x
                    rev_or = y

                result = {"File": ["Original", "Transformed"], "Units": [units_or, units_tr], "Revenue": [rev_or, rev_tr]}
                df = pd.DataFrame(data=result)
                print(df)

            except:

                print('Could not find', i)
                pass