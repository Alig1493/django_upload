import re
import pandas as pd


class PayloadGenerator():

    def __init__(self, input_file_path, sheet_name):
        input_file_path = self.input_file_path
        excel_file = pd.ExcelFile(input_file_path)
        sheet_name = self.sheet_name

    def match_strings(data_dictionary, string):
        matched_indices_list = []
        for k1,v1 in data_dictionary.items():
            for k2,v2 in v1.items():
                if type(v2) == type(" ") and len(re.findall('\\b'+string+'\\b', v2)) != 0:
                    matched_indices_tuple = (k2,k1)
                    matched_indices_list.append(matched_indices_tuple)
        return matched_indices_list

    def read_dataframe(sheet_name):
        if sheet_name in excel_file.sheet_names:
            df_rawdata = pd.read_excel(input_file_path, sheet_name = sheet_name, header=None)
            return df_rawdata

    def generate_scraper_metadata(sheet_name):
        df_rawdata = read_dataframe(sheet_name)
        data_dictionary = df_rawdata.to_dict()
        if sheet_name == "Budget":
            return generate_budget_scraper_metadata(df_rawdata, data_dictionary)
        elif sheet_name == "Reservations":
            return generate_reservations_scraper_metadata(df_rawdata, data_dictionary)
        elif sheet_name == "Projections":
            return generate_projections_scraper_metadata(df_rawdata, data_dictionary)

    def generate_budget_scraper_metadata(df_rawdata, data_dictionary):
        matched_indices_list_total = match_strings(data_dictionary, "Total")
        matched_indices_list_capacity = match_strings(data_dictionary, "Capacity Loading")
        date_list = df_rawdata.iloc[matched_indices_list_capacity[0][0],2:14]
        year_list = date_list.map(lambda x: x.year).tolist()
        month_list = date_list.map(lambda x: x.month).tolist()
        return matched_indices_list_total,
                matched_indices_list_capacity,
                year_list,
                month_list

    def generate_reservations_scraper_metadata(df_rawdata, data_dictionary):
        matched_indices_list_semiauto = match_strings(data_dictionary,"SA")
        matched_indices_list_auto = match_strings(data_dictionary,"Auto")
        matched_indices_list_12by14gg = match_strings(data_dictionary,"12gg")
        matched_indices_list_7gg = match_strings(data_dictionary,"7gg")
        matched_indices_list_5gg = match_strings(data_dictionary,"5gg")
        matched_indices_list_style = match_strings(data_dictionary, "Style")
        date_list = df_rawdata.iloc[matched_indices_list_style[0][0],2:14]
        year_list = date_list.map(lambda x: x.year).tolist()
        month_list = date_list.map(lambda x: x.month).tolist()
        return matched_indices_list_semiauto,
                matched_indices_list_auto,
                matched_indices_list_12by14gg,
                matched_indices_list_7gg,
                matched_indices_list_5gg,
                matched_indices_list_style,
                year_list,
                month_list

    def generate_projections_scraper_metadata(df_rawdata, data_dictionary):
        matched_indices_list_open = match_strings(data_dictionary,"OPENING")
        matched_indices_list_ttl = match_strings(data_dictionary,"TTL")
        open_list = []
        for item in matched_indices_list_open:
            open_list.append(df_rawdata.iloc[item[0]+1,1])
        year_list = [x.year for x in open_list]
        month_list = [x.month for x in open_list]
        return matched_indices_list_open,
                matched_indices_list_ttl,
                year_list,
                month_list

    def generate_partial_payload(core_payload_data_tuple, year_list, month_list, row_name, suffix=""):
        partial_payload = list()
        for unit in [0, 1]:
            for idx, session in enumerate(month_list):
                d={'year': year_list[idx],
                   'session': session,
                   'unit': unit}
                if unit == 0:
                    partial_payload.append({**d,
                                           "{}{}".format(row_name, suffix): core_payload_data_tuple[0]})
                else:
                    partial_payload.append({**d,
                                           "{}{}".format(row_name, suffix): core_payload_data_tuple[1]})
        return partial_payload

    def generate_partial_ggwise_payload(core_payload_data_tuple, year_list, month_list, row_name, suffix=""):
        partial_ggwise_payload = list()
        unit=1
        for idx, session in enumerate(month_list):
            partial_ggwise_payload.append({'year': year_list[idx],
               'session': session,
               'unit': unit,
                "{}{}".format(row_name, suffix): core_payload_data_tuple[0]})
        return partial_ggwise_payload
