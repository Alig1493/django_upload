import os
import pandas as pd
# from django.conf import settings
# from django.core.files import File

# from django.core.files.storage import default_storage

# from django.utils.dateparse import parse_date
# from django.utils.datetime_safe import datetime

# from .models import FileDownload
from django_file_upload.capacity.models import MachineDay, SAH, Pcs, GGPcs
from django_file_upload.upload.utils import insert_data
from .payload_generator import PayloadGenerator, \
    ConfirmedPayloadGenerator, BudgetPayloadGenerator, \
    ReservationsPayloadGenerator, ProjectionsPayloadGenerator


def process_file(input_file_path, input_file_date):

    # input_file_path = f"{}/uploads/U2-master_knitting_plan-8th_Feb_uBJbqqP.xlsx"
    # input_file_path = input_file_path.file_field.name

# NOTE: not sure whether file_save_path is required anymore since we would be adding data directly to db and to an endpoint

    # file_save_path = f"{settings.MEDIA_ROOT}/downloads"
    #
    # if not os.path.exists(f"{settings.MEDIA_ROOT}/downloads"):
    #     os.makedirs(file_save_path, exist_ok=True)

    budget_payload_generator = BudgetPayloadGenerator(input_file_path)
    reservations_payload_generator = \
        ReservationsPayloadGenerator(input_file_path)
    projections_payload_generator = \
        ProjectionsPayloadGenerator(input_file_path)
    confirmed_payload_generator = \
        ConfirmedPayloadGenerator(input_file_path)
    payload_generator = PayloadGenerator(input_file_path)

    (
        mcdays_budget,
        sah_budget,
        pcs_budget,
        fob_budget,
        va_budget,
        epm_budget,
        ) = budget_payload_generator.generate_budget_dataframe_set()
    (
        mcdays_resv,
        sah_resv,
        pcs_resv,
        reservations_12,
        reservations_7,
        reservations_5,
        ) = \
            reservations_payload_generator.generate_reservations_dataframe_set()
    (
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
        ) = \
            projections_payload_generator.generate_projections_dataframe_set()
    (
        mcdays_confirmed,
        sah_confirmed,
        pcs_confirmed,
        pcs_confirmed_12,
        pcs_confirmed_7,
        pcs_confirmed_5,
        pcs_confirmed_buyer,
        ) = \
            confirmed_payload_generator.generate_confirmed_dataframe_set()

    machine_day_dataframes_list = [mcdays_budget, mcdays_resv,
                                   mcdays_proj, mcdays_open,
                                   mcdays_confirmed]
    sah_dataframes_list = [
        sah_budget,
        sah_resv,
        sah_proj,
        sah_open,
        fob_budget,
        va_budget,
        epm_budget,
        sah_confirmed,
        ]
    pcs_dataframes_list = [pcs_budget, pcs_resv, pcs_proj, pcs_open,
                           pcs_confirmed]
    gg_pcs_dataframes_list = [
        reservations_12,
        reservations_7,
        reservations_5,
        projections_12,
        projections_7,
        projections_5,
        open_12,
        open_7,
        open_5,
        pcs_confirmed_12,
        pcs_confirmed_7,
        pcs_confirmed_5,
        ]

# TODO: add these payload data to your django db and to our analytics endpoints
# TODO: the buyerwise model needs to be changed as discussed (see note django_file_upload/confirmation/models.py)
    machine_day_payload = payload_generator.generate_final_payload(machine_day_dataframes_list)
    # print("Machine day payload: ", machine_day_payload)
    insert_data(MachineDay, machine_day_payload)
    # print("===========================================")
    sah_payload = payload_generator.generate_final_payload(sah_dataframes_list)
    # print("SAH payload: ", sah_payload)
    insert_data(SAH, sah_payload)
    # print("===========================================")
    pcs_payload = payload_generator.generate_final_payload(pcs_dataframes_list)
    # print("PCS Payload", pcs_payload)
    insert_data(Pcs, pcs_payload)
    # print("===========================================")
    gg_pcs_payload = payload_generator.generate_final_payload(gg_pcs_dataframes_list)
    # print("GG pcs payload: ", gg_pcs_payload)
    insert_data(GGPcs, gg_pcs_payload)
    # print("===========================================")
    buyer_wise_payload = pcs_confirmed_buyer
    # print(type(buyer_wise_payload))
    # print("Buyer wise: ", buyer_wise_payload.to_dict(orient='records'))

# TODO: Not sure whether any files are being stored on each upload. If stored, then delete the file at the end.

#     print(pd.DataFrame(machine_day_payload).head(20))
#     print(pd.DataFrame(sah_payload).head(20))
#     print(pd.DataFrame(pcs_payload).head(20))
#     print(pd.DataFrame(gg_pcs_payload).head(20))
#     print(pd.DataFrame(buyer_wise_payload).head(20))
#
# if __name__ == '__main__':
#     input_file_path = "./dashboard+data-1017'18 (new).xlsx"
#     process_file(input_file_path, 'asd')
