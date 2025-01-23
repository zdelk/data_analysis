# IAQ Analysis Functions
# Zachary Delk
# Southface
import pandas as pd
import numpy as np

# Idea: function that returns number of observation (amount of time) metric is above a healthy threshold
def binary_threshold(data, thresholds):
    nested_list = []
    for col in data.columns:
        if col in thresholds:
            threshold = thresholds[col]
            val_list = []
            for i in range(len(data[col])):
                if data[col][i] > threshold:
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