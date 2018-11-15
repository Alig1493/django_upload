from math import isnan


def insert_data(model, payload):

    for value in payload:
        cleaned_dict = {k: value[k] for k in value if (isinstance(value[k], float) or
                                                       isinstance(value[k], int)) and not isnan(value[k])}
        print("Cleaned dict: ", cleaned_dict)
        model.objects.create(**cleaned_dict)
