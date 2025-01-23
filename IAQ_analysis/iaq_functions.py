# IAQ Analysis Functions
# Zachary Delk
# Southface
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Idea: function that returns number of observation (amount of time) metric is above a healthy threshold

# - FUNCTIONS
# binary_threshold - takes in a dataframe and check metric values against a single threshold value
# outputs 1 for at or below threshold (good)
# outputs 0 for above threshold (bad)
# function returns a new dataframe
thresholds_binary = {
    "Temp" : (30,75),
    "Hum": (30,60),
    "CO2" : (0,1000),
    "PM2.5" : (0, 15)
}

def binary_threshold(data, thresholds=thresholds_binary):
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
thresholds_multi = {
    "Temp": {
        "Healthy": (68, 75),
        "Warning": (64.4, 78.8),
        "Unhealthy": (60.8, 82.4)
    },
    "Hum": {
        "Healthy": (30, 60),
        "Warning": (25, 65),
        "Unhealthy":(20, 70)
    },
    "CO2": {
        "Healthy": (0, 800),
        "Warning": (0, 1000),
        "Unhealthy": (0, 1500)
    },
    "PM2.5": {
        "Healthy": (0, 15),
        "Warning": (0, 35),
        "Unhealthy":(0, 55)
    },
    "PM10": {
        "Healthy": (0, 15),
        "Warning": (0, 35),
        "Unhealthy":(0, 55)
    }
}

def multiclass_threshold(data, thresholds=thresholds_multi):
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

# pie_plotter - takes in a muli-category classified data set and a color dictionary
# Prints out color coded Pie Charts for each metric present
# returns a frequency table for savings if needed
category_colors = {
    "Healthy": "green",
    "Warning": "yellow",
    "Unhealthy": "orange",
    "Dangerous": "red"
}
def pie_plotter(data, category_colors=category_colors):
    freq_table = data.iloc[:,1:].apply(lambda col: col.value_counts()).fillna(0).astype(int)
    for col in freq_table:
        filter_col = {k: v for k,v in freq_table[col].items() if v>0}
        
        labels = list(filter_col.keys())
        values = list(filter_col.values())
        
        colors = [category_colors[label] for label in labels]
        
        plt.pie(values,labels=labels, colors=colors,
                autopct='%1.1f%%', startangle=140)
        plt.legend(title = "Threshold Status:")
        plt.title(freq_table[col].name)
        plt.show()
    return freq_table
