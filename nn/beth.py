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
        self.input_layer = nn.Linear(22, 150)
        self.hidden_layer = nn.Linear(150,25)
        self.output_layer = nn.Linear(25,3)
        self.activation = nn.ReLU()

    def forward(self, input_minute):
        i = input_list_from_minute(input_minute)
        output = self.activation(self.input_layer(i)) # pasada por la capa entrada
        output = self.activation(self.hidden_layer(output))   # pasada por la capa oculta
        output = self.output_layer(output)                    # pasada por la capa de salida
        return output


    def learn(self, minute, next_minute):
        loss_function = nn.CrossEntropyLoss() #función de pérdidas
        parameters = self.parameters()
        optimizer = optim.Adam(params=parameters, lr=0.001) #algoritmo usado para optimizar los parámetros
        losses = np.array([]) #array que guarda la pérdida en cada iteración

        output = self(minute) #calcular la salida para una imagen
        self.zero_grad() #poner los gradientes a cero en cada iteración

        if next_minute_unstable(next_minute):
            target = torch.tensor([0, 0, 1])
            print('not!')
        elif int(minute.valoration) == 0:
            target = torch.tensor([0, 1, 0])
        else:
            target = torch.tensor([1, 0, 0])

        error = loss_function(output, target) #calcular el error
        error.backward() #obtener los gradientes y propagar
        optimizer.step() #actualizar los pesos con los gradientes
        losses = np.append(losses,error.item())

def is_stable(l): # 1, 3
    trends = (l[1] + 0.001) / (l[0] + 0.001)
    x = 0
    while x < 4:
        t = (l[x + 1] + 0.001) / (l[x] + 0.001)
        if (trends > 0) and (t < 0):
            return 0
        if (trends < 0) and (t > 0):
            return 0
        x += 1        
    return 1

def evolution(l): # 2, 4
    return zero_div(l[4], l[0])

def price_evolution_from_average(m):  # 5
    return m.minute_list[4] / m.average

def init_price_from_average(m): # 6
    return m.minute_list[0] / m.average

def always_increase(price_list): # 7, 8
    ret = 0
    increase = True
    x = 4
    while (increase & x > 0):
        if(price_list[x] >= price_list[x - 1]):
            ret += 0.25
        else:
            increase = False
    return ret

def evolution_from_last_price(m): # 13, 14, 15, 16 (returns a list)
    ret = []
    x = 0
    while x < 4:
        r = m.minute_list[x + 1] / m.minute_list[x]
        ret.append(r)
        x += 1
    return ret

def evolution_for_operation(m): #9, 10, 11, 12
    ret = []
    ev = evolution_from_last_price(m)
    x = 0
    while x < 4:
        r = zero_div(ev[x], m.operation_list[x + 1])
        ret.append(r)
        x += 1
    return ret

def average_5_from_average(m): #17
    return m.average_5 / m.average

def average_10_from_average(m): #18
    return m.average_10 / m.average

def average_15_from_average(m): #19
    return m.average_15 / m.average

def average_5_from_average_10(m): #20
    return m.average_5 / m.average_10

def average_5_from_average_15(m): #21
    return m.average_5 / m.average_15

def average_10_from_average_15(m): #22
    return m.average_10 / m.average_15

def input_list_from_minute(m): # (ALL)
    input = []

    input.append(is_stable(m.minute_list))
    input.append(evolution(m.minute_list))

    input.append(is_stable(m.operation_list))
    input.append(evolution(m.operation_list))

    input.append(price_evolution_from_average(m))
    input.append(init_price_from_average(m))

    input.append(always_increase(m.minute_list))
    input.append(always_increase(m.operation_list))

    input += evolution_for_operation(m)
    input += evolution_from_last_price(m)

    input.append(average_5_from_average(m))
    input.append(average_10_from_average(m))
    input.append(average_15_from_average(m))

    input.append(average_5_from_average_10(m))
    input.append(average_5_from_average_15(m))
    input.append(average_10_from_average_15(m))

    return torch.tensor([input, input])


def zero_div(c, d):
    if c == 0:
        return 0
    if d == 0:
        return 1
    return c / d


def next_minute_unstable(m):
    if m.price_list[4] == False and m.price_list[3] == True and m.price_list[2] == False:
        return True

    if m.price_list[4] == True and m.price_list[3] == False and m.price_list[2] == True:
        return True

    return False