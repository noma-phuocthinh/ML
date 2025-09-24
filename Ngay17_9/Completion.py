from numpy import nan as NA
import pandas as pd
data = pd.DataFrame([[1,6.5,3],
                     [1,NA,NA],
                     [NA,NA,NA],
                    [NA,6.5,3]])

"""
1. Completion - Có các dữ liệu, lọc dữ liệu bị thiếu:
 - Lọc dữ liệu bị thiếu (Filtering out missing data)
 - Điền dữ liệu còn thiếu (Filling in missing data)
"""
#%% - Filtering out
print(data)
cleaned = data.dropna()
print(cleaned)
cleaned2 = data.dropna(how='all')
#%% Filling in
print("-"*20)
cleaned3 = data.fillna(data.mean())
print(cleaned3)
