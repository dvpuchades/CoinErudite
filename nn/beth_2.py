import torch.nn as nn
from torch import optim
import numpy as np
from torch.autograd import Variable #necesario para calcular gradientes
import torch


# el objetivo de Beth es clasificar un minute segun las
# tendencias que muestra

#COPIAR TENDENCIAS EN ALGUN MOMENTO


#definimos la red neuronal 
class Beth(nn.Module):
    def __init__(self):
        super(Beth,self).__init__()
        self.type = 'classifier'
        self.input_layer = nn.Linear(34, 150)
        self.hidden_layer = nn.Linear(150,25)
        self.output_layer = nn.Linear(25,2)
        self.activation = nn.ReLU()

    def forward(self, input_minute):

        if input_minute.product == 'ethereum':
            i = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        elif input_minute.product == 'cardano':
            i = [0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        elif input_minute.product == 'dogecoin':
            i = [0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        elif input_minute.product == 'polkadot':
            i = [0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
        elif input_minute.product == 'ripple':
            i = [0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        elif input_minute.product == 'bitcoin':
            i = [0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
        elif input_minute.product == 'binance coin':
            i = [0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
        elif input_minute.product == 'uniswap':
            i = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
        elif input_minute.product == 'iota':
            i = [0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
        elif input_minute.product == 'luna coin':
            i = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        else:
            i = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        if input_minute.minute_list[4] > input_minute.minute_list[3]:
            i.append(1)
        else:
            i.append(0)

        if input_minute.minute_list[3] > input_minute.minute_list[2]:
            i.append(1)
        else:
            i.append(0)

        if input_minute.minute_list[2] > input_minute.minute_list[1]:
            i.append(1)
        else:
            i.append(0)

        if input_minute.minute_list[1] > input_minute.minute_list[0]:
            i.append(1)
        else:
            i.append(0)
        
        amount_price = 0
        for e in input_minute.minute_list:
            amount_price += e 
        
        for e in input_minute.minute_list:
            i.append( e / amount_price )
        
        i.append(always_increase(input_minute.minute_list))

        amount_op = 0 
        for e in range(4):
            amount_op += input_minute.operation_list[e]

        for e in range(4):
            i.append(zero_div(input_minute.operation_list[e], amount_op))
        
        if input_minute.operation_list[4] > input_minute.operation_list[3]:
            i.append(1)
        else:
            i.append(0)

        if input_minute.operation_list[3] > input_minute.operation_list[2]:
            i.append(1)
        else:
            i.append(0)

        if input_minute.operation_list[2] > input_minute.operation_list[1]:
            i.append(1)
        else:
            i.append(0)

        if input_minute.operation_list[1] > input_minute.operation_list[0]:
            i.append(1)
        else:
            i.append(0)

        if input_minute.minute_list[4] > input_minute.average_5:
            i.append(1)
        else:
            i.append(0)

        if input_minute.average_5 > input_minute.average_10:
            i.append(1)
        else:
            i.append(0)

        if input_minute.average_10 > input_minute.average_15:
            i.append(1)
        else:
            i.append(0)

        if input_minute.average_15 > input_minute.average:
            i.append(1)
        else:
            i.append(0)

        i.append(always_increase(input_minute.operation_list))

        if input_minute.minute_list[4] > input_minute.minute_list[0]:
            i.append(1)
        else:
            i.append(0)

        i = torch.tensor([i, i])

        output = self.activation(self.input_layer(i)) # pasada por la capa entrada
        output = self.activation(self.hidden_layer(output))   # pasada por la capa oculta
        output = self.output_layer(output)                    # pasada por la capa de salida
        return output


    def learn(self, minute):
        loss_function = nn.CrossEntropyLoss() #función de pérdidas
        parameters = self.parameters()
        optimizer = optim.Adam(params=parameters, lr=0.001) #algoritmo usado para optimizar los parámetros
        losses = np.array([]) #array que guarda la pérdida en cada iteración

        output = self(minute) #calcular la salida para una imagen
        self.zero_grad() #poner los gradientes a cero en cada iteración

        if int(minute.valoration) == 0:
            target = torch.tensor([0, 1])
        else:
            target = torch.tensor([1, 0])

        error = loss_function(output, target) #calcular el error
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

def zero_div(c, d):
    if c == 0:
        return 0
    if d == 0:
        return 1
    return c / d