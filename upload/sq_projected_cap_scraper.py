import ntpath
import os
import pandas as pd
from django.conf import settings
from django.core.files import File

from upload.models import FileDownload


def match_strings(d, string):
    mylist = []
    for k1, v1 in d.items():
        for k2, v2 in v1.items():
            if type(v2) == type(" ") and v2.find(string) != -1:
                mytuple = (k2, k1)
                mylist.append(mytuple)
    return mylist


def process_file():
    input_file_path = f"{settings.MEDIA_ROOT}/uploads/U2-master_knitting_plan-8th_Feb_uBJbqqP.xlsx"

    file_save_path = f"{settings.MEDIA_ROOT}/downloads"

    if not os.path.exists(f"{settings.MEDIA_ROOT}/downloads"):
        os.makedirs(file_save_path, exist_ok=True)

    file_name = "Confirmed Loading - SQCL-2.xlsx"

    final_path = os.path.join(file_save_path, file_name)

    excel_file = pd.ExcelFile(input_file_path)

    if "Auto plan . (2)" in excel_file.sheet_names or "semi-auto plan ." in excel_file.sheet_names:
        df1 = pd.read_excel(input_file_path, sheet_name="Auto plan . (2)", header=None)
        df2 = pd.read_excel(input_file_path, sheet_name="semi-auto plan .", header=None)
        d1 = df1.to_dict()
        d2 = df2.to_dict()
        mylist_of_tuples1 = match_strings(d1, "Target")
        mylist_of_tuples2 = match_strings(d2, "Target")
        df_out1 = pd.DataFrame()
        df_out2 = pd.DataFrame()

        for i in range(len(mylist_of_tuples1)):
            df_first_col1 = df1[0]
            df_first_col_slice1 = df_first_col1.iloc[df_first_col1[df_first_col1 == "Month"].index[0]:]
            df_first_col_slice1.dropna(inplace=True)
            prod_month_list1 = list(set(df_first_col_slice1[1:]))
            machine_days_list1 = []
            pcs_list1 = []
            sah_list1 = []

            for month in prod_month_list1:
                df_month1 = df1[df1[0] == month]
                df_month1 = df_month1.fillna(0)
                machine_days_list1.append(sum(df_month1[mylist_of_tuples1[i][1] - 1]))
                pcs_list1.append(sum(df_month1[mylist_of_tuples1[i][1] + 1]))
                sah_list1.append(sum(df_month1[mylist_of_tuples1[i][1] + 3]))

            if i < len(mylist_of_tuples1) - 1 and mylist_of_tuples1[i + 1][1] - mylist_of_tuples1[i][1] >= 6:
                df_temp1 = {'Prod Month': prod_month_list1,
                            'Buyer': [df1.iloc[mylist_of_tuples1[i][0] - 2, mylist_of_tuples1[i][1] - 1] for j in
                                      range(len(prod_month_list1))],
                            'Style': [df1.iloc[mylist_of_tuples1[i][0] - 1, mylist_of_tuples1[i][1] - 1] for j in
                                      range(len(prod_month_list1))],
                            'Machine Type': [df1.iloc[mylist_of_tuples1[i][0] - 4, mylist_of_tuples1[i][1] - 1] for j in
                                             range(len(prod_month_list1))],
                            'Machine Days': machine_days_list1,
                            'Pcs': pcs_list1,
                            'SAH': sah_list1}
                df_temp1 = pd.DataFrame(df_temp1)
                df_out1 = pd.concat([df_out1, df_temp1], axis=0)

        df_temp1 = {'Prod Month': prod_month_list1,
                    'Buyer': [df1.iloc[mylist_of_tuples1[-1][0] - 2, mylist_of_tuples1[-1][1] - 1] for j in
                              range(len(prod_month_list1))],
                    'Style': [df1.iloc[mylist_of_tuples1[-1][0] - 1, mylist_of_tuples1[-1][1] - 1] for j in
                              range(len(prod_month_list1))],
                    'Machine Type': [df1.iloc[mylist_of_tuples1[-1][0] - 4, mylist_of_tuples1[-1][1] - 1] for j in
                                     range(len(prod_month_list1))],
                    'Machine Days': machine_days_list1,
                    'Pcs': pcs_list1,
                    'SAH': sah_list1}

        df_temp1 = pd.DataFrame(df_temp1)
        df_out1 = pd.concat([df_out1, df_temp1], axis=0)
        df_out1.to_excel("Confirmed Loading - Auto.xlsx",
                         columns=['Prod Month', 'Buyer', 'Style', 'Machine Type', 'Machine Days', 'Pcs', 'SAH'],
                         index=None)

        for i in range(len(mylist_of_tuples2)):
            df_first_col2 = df2[0]
            df_first_col_slice2 = df_first_col2.iloc[df_first_col2[df_first_col2 == "Month"].index[0]:]
            df_first_col_slice2.dropna(inplace=True)
            prod_month_list2 = list(set(df_first_col_slice2[1:]))
            machine_days_list2 = []
            pcs_list2 = []
            sah_list2 = []

            for month in prod_month_list2:
                df_month2 = df2[df2[0] == month]
                df_month2 = df_month2.fillna(0)
                machine_days_list2.append(sum(df_month2[mylist_of_tuples2[i][1] - 1]))
                pcs_list2.append(sum(df_month2[mylist_of_tuples2[i][1] + 1]))
                sah_list2.append(sum(df_month2[mylist_of_tuples2[i][1] + 3]))

            if i < len(mylist_of_tuples2) - 1 and mylist_of_tuples2[i + 1][1] - mylist_of_tuples2[i][1] >= 6:
                df_temp2 = {'Prod Month': prod_month_list2,
                            'Buyer': [df2.iloc[mylist_of_tuples2[i][0] - 2, mylist_of_tuples2[i][1] - 1] for j in
                                      range(len(prod_month_list2))],
                            'Style': [df2.iloc[mylist_of_tuples2[i][0] - 1, mylist_of_tuples2[i][1] - 1] for j in
                                      range(len(prod_month_list2))],
                            'Machine Type': [df2.iloc[mylist_of_tuples2[i][0] - 3, mylist_of_tuples2[i][1] - 1] for j in
                                             range(len(prod_month_list2))],
                            'Machine Days': machine_days_list2,
                            'Pcs': pcs_list2,
                            'SAH': sah_list2}
                df_temp2 = pd.DataFrame(df_temp2)
                df_out2 = pd.concat([df_out2, df_temp2], axis=0)

        df_temp2 = {'Prod Month': prod_month_list2,
                    'Buyer': [df2.iloc[mylist_of_tuples2[-1][0] - 2, mylist_of_tuples2[-1][1] - 1] for j in
                              range(len(prod_month_list2))],
                    'Style': [df2.iloc[mylist_of_tuples2[-1][0] - 1, mylist_of_tuples2[-1][1] - 1] for j in
                              range(len(prod_month_list2))],
                    'Machine Type': [df2.iloc[mylist_of_tuples2[-1][0] - 3, mylist_of_tuples2[-1][1] - 1] for j in
                                     range(len(prod_month_list2))],
                    'Machine Days': machine_days_list2,
                    'Pcs': pcs_list2,
                    'SAH': sah_list2}

        df_temp2 = pd.DataFrame(df_temp2)
        df_out2 = pd.concat([df_out2, df_temp2], axis=0)
        df_out2.to_excel("Confirmed Loading - Semi Auto.xlsx",
                         columns=['Prod Month', 'Buyer', 'Style', 'Machine Type', 'Machine Days', 'Pcs', 'SAH'],
                         index=None)

    else:
        df = pd.read_excel(input_file_path, sheet_name="M PLAN ", header=None)
        d = df.to_dict()
        mylist_of_tuples = match_strings(d, "Target")
        df_out = pd.DataFrame()

        for i in range(len(mylist_of_tuples)):
            df_first_col = df[0]
            df_first_col_slice = df_first_col.iloc[df_first_col[df_first_col == "Month"].index[0]:]
            df_first_col_slice.dropna(inplace=True)
            prod_month_list = list(set(df_first_col_slice[1:]))
            machine_days_list = []
            pcs_list = []
            sah_list = []

            for month in prod_month_list:
                df_month = df[df[0] == month]
                df_month = df_month.fillna(0)
                machine_days_list.append(sum(df_month[mylist_of_tuples[i][1] - 1]))
                pcs_list.append(sum(df_month[mylist_of_tuples[i][1] + 1]))
                sah_list.append(sum(df_month[mylist_of_tuples[i][1] + 3]))

            if i < len(mylist_of_tuples) - 1 and mylist_of_tuples[i + 1][1] - mylist_of_tuples[i][1] >= 6:
                df_temp = {'Prod Month': prod_month_list,
                           'Buyer': [df.iloc[mylist_of_tuples[i][0] - 2, mylist_of_tuples[i][1] - 1] for j in
                                     range(len(prod_month_list))],
                           'Style': [df.iloc[mylist_of_tuples[i][0] - 1, mylist_of_tuples[i][1] - 1] for j in
                                     range(len(prod_month_list))],
                           'Machine Type': [df.iloc[mylist_of_tuples[i][0] - 5, mylist_of_tuples[i][1] - 1] for j in
                                            range(len(prod_month_list))],
                           'Machine Days': machine_days_list,
                           'Pcs': pcs_list,
                           'SAH': sah_list}
                df_temp = pd.DataFrame(df_temp)
                df_out = pd.concat([df_out, df_temp], axis=0)

        df_temp = {'Prod Month': prod_month_list,
                   'Buyer': [df.iloc[mylist_of_tuples[-1][0] - 2, mylist_of_tuples[-1][1] - 1] for j in
                             range(len(prod_month_list))],
                   'Style': [df.iloc[mylist_of_tuples[-1][0] - 1, mylist_of_tuples[-1][1] - 1] for j in
                             range(len(prod_month_list))],
                   'Machine Type': [df.iloc[mylist_of_tuples[-1][0] - 5, mylist_of_tuples[-1][1] - 1] for j in
                                    range(len(prod_month_list))],
                   'Machine Days': machine_days_list,
                   'Pcs': pcs_list,
                   'SAH': sah_list}

        df_temp = pd.DataFrame(df_temp)
        df_out = pd.concat([df_out, df_temp], axis=0)

        df_out.to_excel(final_path,
                        columns=['Prod Month', 'Buyer', 'Style', 'Machine Type', 'Machine Days', 'Pcs', 'SAH'],
                        index=None)

        with open(final_path, 'rb') as f:
            output_file = FileDownload()
            output_file.file_field.save(name=file_name, content=File(f))
