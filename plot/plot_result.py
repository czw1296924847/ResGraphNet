"""
plot the result on different models, in spiral graph
"""
import matplotlib.pyplot as plt
import numpy as np
import sys
import os.path as osp
import os
sys.path.append("..")
import func.cal as cal


def select_result(model, ts_name, data_style, style=None):
    model_list = ["ResGraphNet", "RESModel", "GNNModel", "RNNModel", "MLModel", "ARIMA", "SARIMAX"]
    if style is None:
        x_name = "{}_true".format(data_style)
    else:
        x_name = "{}_predict_{}".format(data_style, style)
    if model in model_list:
        x_address = osp.join("../result/{}/{}".format(ts_name, model), x_name + ".npy")
    else:
        raise TypeError("Unknown type of model!")
    x = np.load(x_address)
    return x, x_name

data_style = "test"             # Select training set ("train") or test set ("test")
ts_name = "HadCRUT5_global"            # Select time series already processed

model_all = ["ResGraphNet", "RESModel", "GNNModel", "RNNModel", "MLModel", "ARIMA", "SARIMAX"]
model = "MLModel"               # Select Model Style

gnn_style_all = ["GraphSage", "GCN", "GIN", "UniMP"]
rnn_style_all = ["LSTM", "GRU"]
ml_style_all = ["forest", "linear"]
style = "linear"                   # Select Model Style Further

graph_address = osp.join("../graph", ts_name)       # the address of saving figures
if not(osp.exists(graph_address)):
    os.makedirs(graph_address)

x, x_name = select_result(model, ts_name, data_style=data_style, style=style)

cal.plot_spiral(x)                  # Draw the curve according to the spiral diagram
plt.savefig(osp.join(graph_address, x_name + ".png"))

print()
plt.show()
print()
