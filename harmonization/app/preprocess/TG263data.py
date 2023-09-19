
# TG263 Data Upload

import pandas as pd
from app.models import TG263Data

def tg263_data_upload(path):
    df = pd.read_csv(path)
    for index, row in df.iterrows():
        my_model = TG263Data(
            Target_Type=row['Target Type'],
            Major_Category=row['Major Category'],
            Minor_Category=row['Minor Category'],
            Anatomic_Group=row['Anatomic Group'],
            TG263_Primary_Name=row['TG263-Primary Name'],
            TG263_Reverse_Order_Name=row['TG-263-Reverse Order Name'],
            Description=row['Description'],
            FMAID=row['FMAID'],
        )
        my_model.save()

path = "C:/Users/91889/Pictures/django app/app/preprocess/TG263_Nomenclature.csv"

def TG263_data():
    from ..models import TG263Data
    from app.preprocess.TG263data import tg263_data_upload
    if TG263Data.objects.count() == 0:
        tg263_data_upload(path=path)
        print('TG263Data Data upload successful.')
    else:
        print('TG263Data Data already exists.')