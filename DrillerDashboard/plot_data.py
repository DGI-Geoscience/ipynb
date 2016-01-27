import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def plot_data(data_frame, from_time, to_time):
    params = ["cum_distance", "feed_rate", "wob", "pressure", "flow_rate", "rpm"]
    data_frame2 = data_frame.where(data_frame["time"] > pd.Timestamp(from_time))\
        .where(data_frame["time"] < pd.Timestamp(to_time))

    # unique_runs = pd.unique(data_frame2["run_id"].dropna())
    # frame_list = []
    # for run_id in unique_runs:
    #     df = data_frame2[(data_frame2["run_id"] == run_id)]
    #     df["delta_wob"] = np.concatenate((np.array([0]), np.diff(df["wob"])))
    #     frame_list.append(df)
    #
    # data_frame_out = pd.DataFrame(pd.concat(frame_list))
    fig, axis_array = plt.subplots(len(params), sharex=True)
    color_idx = np.linspace(0, 1, len(params))
    axis_array[0].set_title(from_time + " to " + to_time)
    for c, name, axis in zip(color_idx, params, axis_array):
        axis.plot_date(data_frame2["time"], data_frame2[name], color=plt.cm.Dark2(c), linestyle="None", marker=".")
        axis.set_ylabel(name)

    return data_frame
