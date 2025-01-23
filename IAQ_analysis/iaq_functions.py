# IAQ Analysis Functions
# Zachary Delk
# Southface
import pandas as pd
import numpy as np

# Idea: function that returns number of observation (amount of time) metric is above a healthy threshold

# - FUNCTIONS
# binary_threshold - takes in a dataframe and check metric values against a single threshold value
# outputs 1 for at or below threshold (good)
# outputs 0 for above threshold (bad)
# function returns a new dataframe
def binary_threshold(data, thresholds):
    nested_list = []
    for col in data.columns:
        if col in thresholds:
            threshold = thresholds[col]
            val_list = []
            for i in range(len(data[col])):
                if data[col][i] >= threshold:
                    val_list.append(1)
                else:
                    val_list.append(0)
                    
            nested_list.append(val_list)


        else:
            print(f"{col} does NOT appear in thresholds")
            time_list = data[col]

    binary_thresh_df = pd.DataFrame(nested_list).T
    bin_thresh_full = pd.concat([time_list, binary_thresh_df], axis=1)

    bin_thresh_full.columns = data.columns  
    return binary_thresh_df

# multicalss_thresholds - takes in a dataframe and checks metrics against multiple threshold ranges
# 'Healthy', 'Warning', 'Unhealthy', and 'Dangerous' classifications
# 'Dangerous' is assigned if it falls outside of the provided ranges
# Dictionary Example: 
# thresholds = {
#     "Temp": {
#         "Healthy": (68, 75),
#         "Warning": (64.4, 78.8),
#         "Unhealthy": (60.8, 82.4)
#     }, ... }

def multiclass_thresholds(data, thresholds):
    nested_list = []
    for col in data.columns:
        if col in thresholds:
            col_thresholds = thresholds[col]
            val_list = []
            for value in data[col]:
                category = None
                for label, (lower, upper) in col_thresholds.items():
                    if lower <= value <= upper:
                        category = label
                        break
                    else:
                        category = "Dangerous"
                val_list.append(category)
            nested_list.append(val_list)
        else:
            id_list = data[col]
            

    classified_df = pd.DataFrame(nested_list).T
    classified_df.columns = [col for col in data.columns if col in thresholds]
    multi_class_df = pd.concat([id_list, classified_df], axis=1)

    return multi_class_df