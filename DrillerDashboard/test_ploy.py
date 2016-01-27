
import pandas as pd
import numpy as np
import plot_data as plt

file_name = "kma-1_drillers_dashboard_data.csv"

df = pd.read_csv(file_name, parse_dates=["time"], index_col="time")
df2 = df.reindex(pd.date_range(start=min(df.index), end=max(df.index), freq="s"))
df2["delta_wob"] = pd.concat(np.concatenate((np.array([0]), np.diff(df2["wob"]))))

time_start1 = "2015-11-06 01:00:00"
time_end1 = "2015-11-06 04:00:00"
df1 = plt.plot_data(df, time_start1, time_end1)
df1.describe()