import torch.nn as nn
from torch import optim
import numpy as np
from torch.autograd import Variable #necesario para calcular gradientes
import torch
import random


# el objetivo de Rick


#definimos la red neuronal 
class Rick(nn.Module):
    def __init__(self):
        super(Rick,self).__init__()
        self.type = 'classifier'
        self.layer = nn.Linear(1, 1)
        self.activation = nn.ReLU()

    def forward(self, input_minute):
        r = input_minute.minute_list[4] / input_minute.minute_list[0]
        if r >= 1:
            return torch.tensor([1])
        else:
            return torch.tensor([0])