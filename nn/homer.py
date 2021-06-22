import torch.nn as nn
from torch import optim
import numpy as np
from torch.autograd import Variable #necesario para calcular gradientes
import torch


#definimos la red neuronal 
class Homer(nn.Module):
    def __init__(self):
        super(Homer,self).__init__()
        self.type = 'classifier'
        self.input_layer = nn.Linear(17,100)
        self.hidden_layer = nn.Linear(100,50)
        self.output_layer = nn.Linear(50,1)
        self.activation = nn.ReLU()

    def forward(self, input_minute):
        input_minute = torch.tensor(input_minute.to_list())
        output = self.activation(self.input_layer(input_minute)) #pasada por la capa entrada
        output = self.activation(self.hidden_layer(output))   #pasada por la capa oculta
        output = self.output_layer(output)                    #pasada por la capa de salida
        return output


    def learn(self, minute):
        loss_function = nn.MSELoss() #función de pérdidas
        parameters = self.parameters()
        optimizer = optim.Adam(params=parameters, lr=0.001) #algoritmo usado para optimizar los parámetros
        losses = np.array([]) #array que guarda la pérdida en cada iteración

        output = self(minute) #calcular la salida para una imagen
        self.zero_grad() #poner los gradientes a cero en cada iteración
        error = loss_function(output, torch.tensor([float(minute.valoration)])) #calcular el error
        error.backward() #obtener los gradientes y propagar
        optimizer.step() #actualizar los pesos con los gradientes
        losses = np.append(losses,error.item())