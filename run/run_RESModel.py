"""
Testing RES Model
"""
import numpy as np
import pandas as pd
import torch
import os
import os.path as osp
import matplotlib.pyplot as plt
import datetime

import sys
sys.path.append("..")
import func.cal as cal
from torch.utils.data import DataLoader


device = "cuda:1" if torch.cuda.is_available() else "cpu"
l_x = 60                   # Data sequence length
l_y = 1                    # Label sequence length
lr = 0.0001                  # Gnn Learning rate
weight_decay = 5e-4
epochs = 200
hidden_dim = 64
batch_size = 32
save_fig = True                  # Whether to save picture
save_txt = False                  # Whether to save txt
save_np = True                  # Whether to save np file
save_model = True               # Whether to save network model
ratio_train = 0.5               # Proportion of training datasets
fig_size = (16, 12)
ts_name_all = ["HadCRUT5", "temp_month", "temp_year"]
ts_name_folder = "HadCRUT5"    # Name of the folder where the data resides
ts_name = "HadCRUT5_global"       # Name of the selected time series
iv = 1                          # sampling interval, used for plotting curves
way = "mean"                    # The style of plot curves of real data and predict results

x_address = osp.join("../datasets", ts_name_folder, ts_name + ".npy")
x = np.load(x_address)
num = x.shape[0]                # The length of time series

result_address = osp.join("../result", ts_name, "RESModel")
if not(osp.exists(result_address)):
    os.makedirs(result_address)

num_train = int(ratio_train * num)
data_train, data_test = x[:num_train], x[num_train:num]     # get training dataset and test dataset

# Using RESModel to predict time series
start_time = datetime.datetime.now()
print("\nRunning, RESModel")
x_train, y_train = cal.create_inout_sequences(data_train, l_x, l_y, style="arr")
x_test, y_test = cal.create_inout_sequences(data_test, l_x, l_y, style="arr")

train_dataset = cal.MyData(x_train, y_train)
test_dataset = cal.MyData(x_test, y_test)
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=False)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

model = cal.RESModel(hidden_dim, l_y, l_x).to(device)
criterion = torch.nn.MSELoss().to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=weight_decay)

for epoch in range(epochs):
    loss_train_all, loss_test_all = 0, 0
    train_true, train_predict, test_true, test_predict = [], [], [], []
    for idx, (x_train, y_train) in enumerate(train_loader):
        x_train, y_train = x_train.to(device), y_train.to(device)
        optimizer.zero_grad()
        output_train = model(x_train)
        loss_train = criterion(output_train, y_train)
        loss_train.backward()
        optimizer.step()
        loss_train_all = loss_train_all + loss_train.item()

        train_predict_one = output_train.detach().cpu().numpy()[:, -1]
        train_true_one = y_train.detach().cpu().numpy()[:, -1]
        if idx == 0:
            train_true = train_true_one
            train_predict = train_predict_one
        else:
            train_true = np.concatenate((train_true, train_true_one), axis=0)
            train_predict = np.concatenate((train_predict, train_predict_one), axis=0)

    for idx, (x_test, y_test) in enumerate(test_loader):
        x_test, y_test = x_test.to(device), y_test.to(device)
        output_test = model(x_test)
        loss_test = criterion(output_test, y_test)
        loss_test_all = loss_test_all + loss_test.item()

        test_predict_one = output_test.detach().cpu().numpy()[:, -1]
        test_true_one = y_test.detach().cpu().numpy()[:, -1]
        if idx == 0:
            test_true = test_true_one
            test_predict = test_predict_one
        else:
            test_true = np.concatenate((test_true, test_true_one), axis=0)
            test_predict = np.concatenate((test_predict, test_predict_one), axis=0)

    r2_train = cal.get_r2_score(train_predict, train_true, axis=1)
    r2_test = cal.get_r2_score(test_predict, test_true, axis=1)
    print("Epoch: {:04d}  Loss_Train: {:.7f}  Loss_Test: {:.7f}  R2_Train: {:.7f}  R2_Test: {:.7f}".
          format(epoch, loss_train_all, loss_test_all, r2_train, r2_test))

end_time = datetime.datetime.now()
run_time = end_time - start_time              # The running time of program

e_res = test_true - test_predict
cal.plot_distribute(e_res, 40, 4, x_name="e")
if save_fig:
    plt.savefig(osp.join(result_address, ts_name + "_RESModel_error_distribution.png"))

cal.plot_result(train_true, test_true, train_predict, test_predict, iv, way, fig_size)
if save_fig:
    plt.savefig(osp.join(result_address, ts_name + "_RESModel.png"))

if save_model:
    torch.save(model, osp.join(result_address, "RESModel.pkl"))
if save_np:
    np.save(osp.join(result_address, "train_true.npy"), train_true)
    np.save(osp.join(result_address, "test_true.npy"), test_true)
    np.save(osp.join(result_address, "train_predict_RESModel.npy"), train_predict)
    np.save(osp.join(result_address, "test_predict_RESModel.npy"), test_predict)

print("RESModel: R2_Train: {:.6f}  R2_Test: {:.6f}".format(r2_train, r2_test))

# The output results of each model are appended to the file
if save_txt:
    info_txt_address = osp.join(result_address, "RESModel_result.txt")  # txt file address for saving parameter information
    info_df_address = osp.join(result_address, "RESModel_result.csv")  # csv file address for saving parameter information
    f = open(info_txt_address, 'a')
    if osp.getsize(info_txt_address) == 0:    # add the name of each feature in the first line of the text
        f.write("r2_test r2_train run_time l_x l_y hidden_dim lr epochs\n")
    f.write(str(r2_test) + " ")
    f.write(str(r2_train) + " ")
    f.write(str(run_time) + " ")
    f.write(str(l_x) + " ")
    f.write(str(l_y) + " ")
    f.write(str(hidden_dim) + " ")
    f.write(str(lr) + " ")
    f.write(str(epochs) + " ")

    f.write("\n")                           # Prepare for next running
    f.close()                               # close file

    info = np.loadtxt(info_txt_address, dtype=str)
    columns = info[0, :].tolist()
    values = info[1:, :]
    info_df = pd.DataFrame(values, columns=columns)
    info_df.to_csv(info_df_address)


print()
plt.show()
print()
