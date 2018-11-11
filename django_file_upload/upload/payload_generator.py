import re
import pandas as pd
from functools import reduce

from django.core.files.storage import default_storage


class PayloadGenerator:

    def __init__(
        self,
        input_file_path,
        sheet_name=0,
        header=None,
        skiprows=None,
        ):
        self.sheet_name = sheet_name
        self.header = header
        self.skiprows = skiprows
        self.df_rawdata = \
            # pd.read_excel(input_file_path,
            pd.read_excel(default_storage.open(input_file_path),
                          sheet_name=sheet_name, header=header,
                          skiprows=skiprows)
        self.data_dictionary = self.df_rawdata.to_dict()

    def match_strings(self, string):
        matched_indices_list = []
        for (k1, v1) in self.data_dictionary.items():
            for (k2, v2) in v1.items():
                if type(v2) == type(' ') and len(re.findall('\\b'
                        + string + '\\b', v2)) != 0:
                    matched_indices_tuple = (k2, k1)
                    matched_indices_list.append(matched_indices_tuple)
        return matched_indices_list

    def combine_payload_elements(self, dataframes_list):
        df_final = reduce(lambda left, right: pd.merge(left, right,
                          on=['session', 'unit', 'year'], how='outer'),
                          dataframes_list)
        return df_final

    def generate_final_payload(self, dataframes_list):
        final_payload = \
            self.combine_payload_elements(dataframes_list).to_dict(orient='records')
        return final_payload


class ConfirmedPayloadGenerator(PayloadGenerator):

    def __init__(
        self,
        input_file_path,
        sheet_name='Confirmed',
        header=0,
        skiprows=[0, 1, 2, 3, 5],
        ):
        super().__init__(input_file_path, sheet_name, header, skiprows)
        (self.preprocessed_dataframe, self.preprocessed_dataframe_gg) = \
            self.process_raw_dataframe()

    def row_map(self, row):
        if '7-14' in row['Machine type']:
            return '12/14GG'
        elif '3.5-7' in row['Machine type']:
            return '7GG'
        elif '6-12' in row['Machine type']:
            return '12/14GG'
        elif '2.5-5' in row['Machine type']:
            return '5GG'
        else:
            return row['Machine type']

    def process_raw_dataframe(self):
        col_list = [
            'Unnamed: 0',
            'Production Month',
            'Buyer',
            'Machine type',
            'Costing Type(HF/AUT)',
            'Actual Pcs',
            'Actual Machine',
            'Actual FOB-USD\nPost-Costing',
            'Plan Prd Minute',
            'Act VA-USD @Post-Costing',
            ]

        df = self.df_rawdata[col_list]
        df = df[df['Unnamed: 0'].isnull() == False]
        df['year'] = df['Production Month'].dt.year
        df['month'] = df['Production Month'].dt.month
        di = {'AUT U 2': 1, 'AUT U I': 1, 'SE': 0}
        df['Costing Type(HF/AUT)'] = df['Costing Type(HF/AUT)'
                ].replace(di)
        df['SAH'] = df['Plan Prd Minute'] / 60
        df['Confirmed EPM'] = df['Act VA-USD @Post-Costing'] / df['Actual Machine']
        df['Machine type'] = df['Machine type'].fillna('Missing')
        df['Machine type'] = df.apply(self.row_map, axis=1)
        machine_list = ['12/14GG', '7GG', '5GG']
        df_gg_subset = df[df['Machine type'].isin(machine_list)]
        return (df, df_gg_subset)

    def generate_monthwise_dataframe(self):
        monthwise_dataframe_col_list = [
            'Actual Machine',
            'SAH',
            'Confirmed EPM',
            'Actual FOB-USD\nPost-Costing',
            'Act VA-USD @Post-Costing',
            'Actual Pcs',
            ]
        monthwise_dataframe = \
            self.preprocessed_dataframe.groupby(['year', 'month',
                'Costing Type(HF/AUT)'
                ]).sum()[monthwise_dataframe_col_list].reset_index()

        monthwise_dataframe.columns=['year', 'session', 'unit', *monthwise_dataframe_col_list]

        return monthwise_dataframe

    def generate_month_ggwise_dataframe(self):
        month_gg_df = self.preprocessed_dataframe_gg.groupby(['year',
                'month', 'Machine type']).sum()['Actual Pcs'
                ].reset_index()
        month_gg_df['unit'] = 1
        month_gg_df.columns = ['year', 'session', 'Machine type',
                               'Actual Pcs', 'unit']
        return month_gg_df

    def generate_month_buyerwise_dataframe(self):
        month_buyer_df = self.preprocessed_dataframe.groupby(['year',
                'month', 'Costing Type(HF/AUT)', 'Buyer'
                ]).sum()['Actual Pcs'].reset_index()
        month_buyer_df.columns = ['year', 'session', 'unit', 'buyer',
                                  'Actual Pcs']
        return month_buyer_df

    def postprocess_dataframe(
        self,
        dataframe,
        col_names,
        col_names_mapper,
        ):
        dataframe = dataframe[col_names]
        processed_dataframe = dataframe.rename(columns=col_names_mapper)
        return processed_dataframe

    def generate_confirmed_dataframe_set(self):
        monthwise_dataframe = self.generate_monthwise_dataframe()
        mcdays_confirmed = \
            self.postprocess_dataframe(monthwise_dataframe, ['year',
                'session', 'unit', 'Actual Machine'],
                {'Actual Machine': 'confirmed'})
        sah_confirmed = self.postprocess_dataframe(monthwise_dataframe,
                [
            'year',
            'session',
            'unit',
            'SAH',
            'Confirmed EPM',
            'Actual FOB-USD\nPost-Costing',
            'Act VA-USD @Post-Costing',
            ], {
            'SAH': 'confirmed',
            'Confirmed EPM': 'confirmed_epm',
            'Actual FOB-USD\nPost-Costing': 'confirmed_fob',
            'Act VA-USD @Post-Costing': 'confirmed_va',
            })
        pcs_confirmed = self.postprocess_dataframe(monthwise_dataframe,
                ['year', 'session', 'unit', 'Actual Pcs'],
                {'Actual Pcs': 'confirmed'})

        month_gg_df = self.generate_month_ggwise_dataframe()
        confirmed_12 = month_gg_df[month_gg_df['Machine type']
                                   == '12/14GG']
        confirmed_7 = month_gg_df[month_gg_df['Machine type'] == '7GG']
        confirmed_5 = month_gg_df[month_gg_df['Machine type'] == '5GG']
        pcs_confirmed_12 = self.postprocess_dataframe(confirmed_12,
                ['year', 'session', 'unit', 'Actual Pcs'],
                {'Actual Pcs': 'confirmed_12'})
        pcs_confirmed_7 = self.postprocess_dataframe(confirmed_7,
                ['year', 'session', 'unit', 'Actual Pcs'],
                {'Actual Pcs': 'confirmed_7'})
        pcs_confirmed_5 = self.postprocess_dataframe(confirmed_5,
                ['year', 'session', 'unit', 'Actual Pcs'],
                {'Actual Pcs': 'confirmed_5'})

        month_buyer_df = self.generate_month_buyerwise_dataframe()
        pcs_confirmed_buyer = \
            self.postprocess_dataframe(month_buyer_df, ['year',
                'session', 'unit', 'buyer', 'Actual Pcs'],
                {'Actual Pcs': 'confirmed'})

        return (
            mcdays_confirmed,
            sah_confirmed,
            pcs_confirmed,
            pcs_confirmed_12,
            pcs_confirmed_7,
            pcs_confirmed_5,
            pcs_confirmed_buyer,
            )


class BudgetPayloadGenerator(PayloadGenerator):

    def __init__(
        self,
        input_file_path,
        sheet_name='Budget',
        header=None,
        skiprows=None,
        ):
        super().__init__(input_file_path, sheet_name, header, skiprows)
        (self.matched_indices_list_total, self.year_list,
         self.month_list) = self.generate_scraper_metadata()

    def generate_scraper_metadata(self):
        matched_indices_list_total = self.match_strings('Total')
        matched_indices_list_capacity = \
            self.match_strings('Capacity Loading')
        date_list = \
            self.df_rawdata.iloc[matched_indices_list_capacity[0][0], 2:
                                 14]
        year_list = date_list.map(lambda x: x.year).tolist()
        month_list = date_list.map(lambda x: x.month).tolist()
        return (matched_indices_list_total, year_list, month_list)

    def generate_partial_payload(
        self,
        sa_row,
        auto_row,
        suffix='',
        ):
        partial_payload = list()
        for unit in [0, 1]:
            for (idx, session) in enumerate(self.month_list):
                d = {'year': self.year_list[idx], 'session': session,
                     'unit': unit}

                if unit == 0:
                    partial_payload.append({**d,
                        "budget{}".format(suffix): \
                        self.df_rawdata.iloc[self.matched_indices_list_total[sa_row][0],
                        idx+2]})
                else:
                    partial_payload.append({**d,
                        "budget{}".format(suffix): \
                        self.df_rawdata.iloc[self.matched_indices_list_total[auto_row][0],
                        idx+2]})

        return partial_payload

    def generate_budget_dataframe_set(self):
        mcdays_budget = pd.DataFrame(self.generate_partial_payload(12,
                6))
        sah_budget = pd.DataFrame(self.generate_partial_payload(9, 3))
        pcs_budget = pd.DataFrame(self.generate_partial_payload(8, 2))
        fob_budget = pd.DataFrame(self.generate_partial_payload(10, 4,
                                  '_fob'))
        va_budget = pd.DataFrame(self.generate_partial_payload(11, 5,
                                 '_va'))
        epm_budget = pd.DataFrame(self.generate_partial_payload(13, 7,
                                  '_epm'))
        return (
            mcdays_budget,
            sah_budget,
            pcs_budget,
            fob_budget,
            va_budget,
            epm_budget,
            )


class ReservationsPayloadGenerator(PayloadGenerator):

    def __init__(
        self,
        input_file_path,
        sheet_name='Reservations',
        header=0,
        skiprows=None,
        ):
        super().__init__(input_file_path, sheet_name, header, skiprows)
        (
            self.matched_indices_list_semiauto,
            self.matched_indices_list_auto,
            self.matched_indices_list_12by14gg,
            self.matched_indices_list_7gg,
            self.matched_indices_list_5gg,
            self.year_list,
            self.month_list,
            ) = self.generate_scraper_metadata()

    def generate_scraper_metadata(self):
        matched_indices_list_semiauto = self.match_strings('SA')
        matched_indices_list_auto = self.match_strings('Auto')
        matched_indices_list_12by14gg = self.match_strings('12gg')
        matched_indices_list_7gg = self.match_strings('7gg')
        matched_indices_list_5gg = self.match_strings('5gg')
        matched_indices_list_style = self.match_strings('Style')
        date_list = \
            self.df_rawdata.iloc[matched_indices_list_style[0][0], 2:14]
        year_list = date_list.map(lambda x: x.year).tolist()
        month_list = date_list.map(lambda x: x.month).tolist()
        return (
            matched_indices_list_semiauto,
            matched_indices_list_auto,
            matched_indices_list_12by14gg,
            matched_indices_list_7gg,
            matched_indices_list_5gg,
            year_list,
            month_list,
            )

    def generate_partial_payload(
        self,
        sa_row,
        auto_row,
        col_idx,
        suffix='',
        ):
        partial_payload = list()

        for unit in [0, 1]:
            for (idx, session) in enumerate(self.month_list):
                d = {'year': self.year_list[idx], 'session': session,
                     'unit': unit}

                if unit == 0:
                    partial_payload.append({**d, "reservations{}".format(suffix): \
                        self.df_rawdata.iloc[self.matched_indices_list_semiauto[sa_row][0],
                        col_idx+idx]})
                else:
                    partial_payload.append({**d, "reservations{}".format(suffix): \
                        self.df_rawdata.iloc[self.matched_indices_list_auto[auto_row][0],
                        col_idx+idx]})

        return partial_payload

    def generate_partial_ggwise_payload(
        self,
        matched_indices_list_gg,
        auto_row,
        col_idx,
        suffix='',
        ):
        partial_ggwise_payload = list()
        unit = 1
        for (idx, session) in enumerate(self.month_list):
            partial_ggwise_payload.append({
                'year': self.year_list[idx],
                'session': session,
                'unit': unit,
                'reservations{}'.format(suffix): \
                        self.df_rawdata.iloc[matched_indices_list_gg[auto_row][0],
                        col_idx + idx],
                })
        return partial_ggwise_payload

    def generate_reservations_dataframe_set(self):
        mcdays_resv = \
            pd.DataFrame(self.generate_partial_payload(sa_row=-1,
                         auto_row=0, col_idx=15))
        sah_resv = \
            pd.DataFrame(self.generate_partial_payload(sa_row=-1,
                         auto_row=0, col_idx=28))
        pcs_resv = \
            pd.DataFrame(self.generate_partial_payload(sa_row=-1,
                         auto_row=0, col_idx=2))
        reservations_12 = \
            pd.DataFrame(self.generate_partial_ggwise_payload(self.matched_indices_list_12by14gg,
                         auto_row=-1, col_idx=2, suffix='_12'))
        reservations_7 = \
            pd.DataFrame(self.generate_partial_ggwise_payload(self.matched_indices_list_7gg,
                         auto_row=-1, col_idx=2, suffix='_7'))
        reservations_5 = \
            pd.DataFrame(self.generate_partial_ggwise_payload(self.matched_indices_list_5gg,
                         auto_row=-1, col_idx=2, suffix='_5'))
        return (
            mcdays_resv,
            sah_resv,
            pcs_resv,
            reservations_12,
            reservations_7,
            reservations_5,
            )


class ProjectionsPayloadGenerator(PayloadGenerator):

    def __init__(
        self,
        input_file_path,
        sheet_name='Projections',
        header=None,
        skiprows=None,
        ):
        super().__init__(input_file_path, sheet_name, header, skiprows)
        (self.matched_indices_list_open, self.matched_indices_list_ttl,
         self.year_list, self.month_list) = \
            self.generate_scraper_metadata()

    def generate_scraper_metadata(self):
        matched_indices_list_open = self.match_strings('OPENING')
        matched_indices_list_ttl = self.match_strings('TTL')
        open_list = []
        for item in matched_indices_list_open:
            open_list.append(self.df_rawdata.iloc[item[0] + 1, 1])
        year_list = [x.year for x in open_list]
        month_list = [x.month for x in open_list]
        return (matched_indices_list_open, matched_indices_list_ttl,
                year_list, month_list)

    def generate_partial_payload(
        self,
        matched_indices_list,
        col_idx_sa,
        col_idx_a_start,
        col_idx_a_end,
        row_name,
        suffix='',
        ):
        partial_payload = list()

        for unit in [0, 1]:
            for (idx, session) in enumerate(self.month_list):
                d = {'year': self.year_list[idx], 'session': session,
                     'unit': unit}

                if unit == 0:
                    partial_payload.append({**d, '{}{}'.format(row_name, suffix): \
                        self.df_rawdata.iloc[matched_indices_list[idx][0], col_idx_sa]})
                else:
                    partial_payload.append({**d, '{}{}'.format(row_name, suffix): \
                    self.df_rawdata.iloc[matched_indices_list[idx][0],
                    col_idx_a_start:col_idx_a_end].sum()})

        return partial_payload

    def generate_partial_ggwise_payload(
        self,
        matched_indices_list,
        col_idx,
        row_name,
        suffix='',
        ):
        partial_ggwise_payload = list()
        unit = 1
        for (idx, session) in enumerate(self.month_list):
            partial_ggwise_payload.append({
                'year': self.year_list[idx],
                'session': session,
                'unit': unit,
                '{}{}'.format(row_name,
                              suffix): self.df_rawdata.iloc[matched_indices_list[idx][0],
                        col_idx],
                })
        return partial_ggwise_payload

    def generate_projections_dataframe_set(self):
        pcs_open = \
            pd.DataFrame(self.generate_partial_payload(self.matched_indices_list_open,
                         col_idx_sa=2, col_idx_a_start=3,
                         col_idx_a_end=6, row_name='open'))
        mcdays_open = \
            pd.DataFrame(self.generate_partial_payload(self.matched_indices_list_open,
                         col_idx_sa=13, col_idx_a_start=14,
                         col_idx_a_end=17, row_name='open'))
        sah_open = \
            pd.DataFrame(self.generate_partial_payload(self.matched_indices_list_open,
                         col_idx_sa=23, col_idx_a_start=24,
                         col_idx_a_end=27, row_name='open'))
        open_12 = \
            pd.DataFrame(self.generate_partial_ggwise_payload(self.matched_indices_list_open,
                         col_idx=3, row_name='open', suffix='_12'))
        open_7 = \
            pd.DataFrame(self.generate_partial_ggwise_payload(self.matched_indices_list_open,
                         col_idx=4, row_name='open', suffix='_7'))
        open_5 = \
            pd.DataFrame(self.generate_partial_ggwise_payload(self.matched_indices_list_open,
                         col_idx=5, row_name='open', suffix='_5'))

        pcs_proj = \
            pd.DataFrame(self.generate_partial_payload(self.matched_indices_list_ttl,
                         col_idx_sa=2, col_idx_a_start=3,
                         col_idx_a_end=6, row_name='projections'))
        mcdays_proj = \
            pd.DataFrame(self.generate_partial_payload(self.matched_indices_list_ttl,
                         col_idx_sa=13, col_idx_a_start=14,
                         col_idx_a_end=17, row_name='projections'))
        sah_proj = \
            pd.DataFrame(self.generate_partial_payload(self.matched_indices_list_ttl,
                         col_idx_sa=23, col_idx_a_start=24,
                         col_idx_a_end=27, row_name='projections'))
        projections_12 = \
            pd.DataFrame(self.generate_partial_ggwise_payload(self.matched_indices_list_ttl,
                         col_idx=3, row_name='projections', suffix='_12'))
        projections_7 = \
            pd.DataFrame(self.generate_partial_ggwise_payload(self.matched_indices_list_ttl,
                         col_idx=4, row_name='projections', suffix='_7'))
        projections_5 = \
            pd.DataFrame(self.generate_partial_ggwise_payload(self.matched_indices_list_ttl,
                         col_idx=5, row_name='projections', suffix='_5'))

        return (
            pcs_open,
            mcdays_open,
            sah_open,
            open_12,
            open_7,
            open_5,
            pcs_proj,
            mcdays_proj,
            sah_proj,
            projections_12,
            projections_7,
            projections_5,
            )
