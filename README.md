# ResGraphNet
ResGraphNet is a deep neural network used to predict time series. It effectively combines Graph Neural Network(GNN) with ResNet Module, so it has a stronger performance than traditional time series prediction methods.<br>
The paper is available in <br>

## Installation
ResGraphNet is based on [Pytorch](https://pytorch.org/docs/stable/index.html) and [Pytorch Geometric](https://pytorch-geometric.readthedocs.io/en/latest/index.html)<br>
Firstly please create a virtual environment for yourself<br>
`conda create -n your-env-name python=3.9`<br><br>
Then, there are some Python packages need to be installed<br>
`conda install pytorch torchvision torchaudio cudatoolkit=11.3`<br>
`conda install pyg -c pyg`<br>
`conda install matplotlib`<br>
`conda install statsmodels`<br>

## Training and Testing Models
The running programs based on different models is in [run](https://github.com/czw1296924847/ResGraphNet/tree/main/run),  and you can type the following command to train these models:<br>
ResGraphNet: `python run_ResGraphNet.py`<br>
RES Model: `python run_RESModel.py`<br>
GNN Model: `python run_GNNModel.py`<br>
RNN Model: `python run_RNNModel.py `<br>

## Plotting Figures
The programs in [plot](https://github.com/czw1296924847/ResGraphNet/tree/main/plot) are used to plot some figures.<br>

## Graphical User Interface (GUI)
We also provide a GUI program [run_python.py](https://github.com/czw1296924847/ResGraphNet/blob/main/gui/run_python.py) so that you can test each dataset and each network model more quickly and intuitively, as shown in the following figure:<br>

![image]([https://github.com/czw1296924847/MagInfoNet/blob/main/dataset_structure.png](https://github.com/czw1296924847/ResGraphNet/blob/main/gui/gui_example.png))
