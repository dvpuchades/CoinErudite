import torch.nn as nn
from torch import optim
import numpy as np
from torch.autograd import Variable #necesario para calcular gradientes
import torch
import random


# el objetivo de Randy es proporcionar salidas aleatorias para testing


#definimos la red neuronal 
class Randy(nn.Module):
    def __init__(self):
        super(Randy,self).__init__()
        self.type = 'classifier'
        self.input_layer = nn.Linear(8,25)
        self.hidden_layer = nn.Linear(25,10)
        self.output_layer = nn.Linear(10,1)
        self.activation = nn.ReLU()

    def forward(self, input_minute):
        r = random.random()
        return torch.tensor([r])