

import os
import pydicom
import numpy as np
import pandas as pd
from fnmatch import fnmatch
from app.models import LabelMapping
from .normalization import clean_contour_label


# Retrieve the queryset containing the "original name" and "new name" fields
label_mappings = LabelMapping.objects.all()

# Create a DataFrame from the queryset
df = pd.DataFrame(list(label_mappings.values('original_label', 'TG263_label')))

original_names_array = df['original_label'].to_numpy()
new_names_array = df['TG263_label'].to_numpy()
csvFile_array = np.column_stack((original_names_array, new_names_array))

# print(csvFile_array)

def ROINormalization(ds, filename):
    for structure_set in ds.StructureSetROISequence:
        structure_set.ROIName = clean_contour_label(structure_set.ROIName)
        # print(structure_set.ROIName, "converted ->", clean_contour_label(structure_set.ROIName))
    ds.save_as(filename)
    


def rtstruct_label_rename(ds, csvFile_array, filename):
  orig_name=csvFile_array[:, 0]
  for i in range (len(ds.StructureSetROISequence)):
    ROI_name=ds.StructureSetROISequence[i].ROIName
    if ROI_name in orig_name:
      loc=np.where(orig_name == ROI_name)
      ds.StructureSetROISequence[i].ROIName=csvFile_array[loc, 1][0][0]

  ds.save_as(filename)


def harmonization(main_path):
    pt_id_path=[]
    pattern = "*.dcm"
    for path, subdirs, files in os.walk(main_path):
        for subdir in subdirs:
            pt_id_path.append(os.path.join(main_path, subdir))
            print(os.path.join(main_path, subdir))
  
    for i in range(len(pt_id_path)):
        path1=pt_id_path[i]+'/'
        for path, subdirs, files in os.walk(path1):
            for name in files:
                if fnmatch(name, pattern):
                    filename=os.path.join(path1, name)
                    ds = pydicom.dcmread(filename)

                    harmonization_info = {
                        "type": "Harmonization Info",
                        "Filename": filename,
                        "RTSTRUCT": "No"
                    }

                    if ds.Modality=='RTSTRUCT':
                        ROINormalization(ds, filename)
                        rtstruct_label_rename(ds, csvFile_array, filename)
                        
                    harmonization_info['RTSTRUCT'] = "Yes"
                    harmonization_info['ROINormalization'] = "Done"
                    harmonization_info['ROI Name Rename'] = "Done"
        import json
        harmonization_json_info = json.dumps(harmonization_info, indent=4)
        print(harmonization_json_info)

# main_path = "C:/Users/91889/Pictures/harmonization/New folder/media/temp"
# harmonization(main_path=main_path)

