import torch.nn as nn
from torch import optim
import numpy as np
from torch.autograd import Variable #necesario para calcular gradientes
import torch


# Barney es una variante de Barney que no tiene en cuenta
# como han evolucionado los precios durante los minutos anteriores

# Tendencias: [1/0]
# precio respecto a precio medio
# kline respecto a kline_hora/60
# kline siempre ascendente
#     [0.25 por cada kline anterior inferior consecutivo]

# 8 entradas


#definimos la red neuronal 
class Barney(nn.Module):
    def __init__(self):
        super(Barney,self).__init__()
        self.type = 'classifier'
        self.input_layer = nn.Linear(3,15)
        self.hidden_layer = nn.Linear(15,5)
        self.output_layer = nn.Linear(5,1)
        self.activation = nn.ReLU()

    def forward(self, input_minute):
        stats_list = []
        if(input_minute.minute_list[4] > input_minute.average):
            stats_list.append(float(1))
        else:
            stats_list.append(float(0))

        if(input_minute.operation_list [4] > input_minute.operation_list[5]):
            stats_list.append(float(1))
        else:
            stats_list.append(float(0))

        stats_list.append(always_increase(input_minute.operation_list[:5]))
        
        input_minute = torch.tensor(stats_list)
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

def always_increase(price_list):
    ret = 0
    increase = True
    x = 4
    while (increase & x > 0):
        if(price_list[x] >= price_list[x - 1]):
            ret += 0.25
        else:
            increase = False
    return ret