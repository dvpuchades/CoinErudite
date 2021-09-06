import torch.nn as nn
from torch import optim
import numpy as np
from torch.autograd import Variable #necesario para calcular gradientes
import torch


# el objetivo de Jared es clasificar un day segun las
# tendencias que muestra

#COPIAR TENDENCIAS EN ALGUN MOMENTO


#definimos la red neuronal 
class Jared(nn.Module):
    def __init__(self):
        super(Jared,self).__init__()
        self.type = 'classifier'
        self.input_layer = nn.Linear(27, 150)
        self.hidden_layer = nn.Linear(150,25)
        self.output_layer = nn.Linear(25,2)
        self.activation = nn.ReLU()

    def forward(self, input_day):
        i = []

        if input_day.product == 'bitcoin':
            i = [1, 0, 0, 0, 0, 0, 0]
        elif input_day.product == 'ethereum':
            i = [0, 1, 0, 0, 0, 0, 0]
        elif input_day.product == 'ripple':
            i = [0, 0, 1, 0, 0, 0, 0]
        elif input_day.product == 'binancecoin':
            i = [0, 0, 0, 1, 0, 0, 0]
        elif input_day.product == 'polkadot':
            i = [0, 0, 0, 0, 1, 0, 0]
        elif input_day.product == 'litecoin':
            i = [0, 0, 0, 0, 0, 1, 0]
        elif input_day.product == 'stellar':
            i = [0, 0, 0, 0, 0, 0, 1]
        else:
            i = [0, 0, 0, 0, 0, 0, 0]

        twitter_followers = input_day.twitter_followers / 10000000
        i.append(twitter_followers)

        reddit_average_posts_48h = input_day.reddit_average_posts_48h / 100
        i.append(reddit_average_posts_48h)

        reddit_average_comments_48h = input_day.reddit_average_comments_48h / 100000
        i.append(reddit_average_comments_48h)

        alexa_rank = input_day.alexa_rank / 100000
        i.append(alexa_rank)

        p0_avg = (input_day.price_list[0] / input_day.average_90) * 0.01
        p1_avg = (input_day.price_list[1] / input_day.average_90) * 0.01
        p2_avg = (input_day.price_list[2] / input_day.average_90) * 0.01
        p3_avg = (input_day.price_list[3] / input_day.average_90) * 0.01
        p4_avg = (input_day.price_list[4] / input_day.average_90) * 0.01

        i.append(p0_avg)
        i.append(p1_avg)
        i.append(p2_avg)
        i.append(p3_avg)
        i.append(p4_avg)

        avg_90_cap = input_day.average_90 / input_day.market_cap
        avg_30_cap = input_day.average_30 / input_day.market_cap
        avg_15_cap = input_day.average_15 / input_day.market_cap

        i.append(avg_90_cap)
        i.append(avg_30_cap)
        i.append(avg_15_cap)

        if input_day.price_list[4] > input_day.price_list[3]:
            i.append(1)
        else:
            i.append(0)

        if input_day.price_list[3] > input_day.price_list[2]:
            i.append(1)
        else:
            i.append(0)

        if input_day.price_list[2] > input_day.price_list[1]:
            i.append(1)
        else:
            i.append(0)

        if input_day.price_list[1] > input_day.price_list[0]:
            i.append(1)
        else:
            i.append(0)

        increase_p0 = (input_day.price_list[4]/input_day.price_list[0]) * 0.01
        i.append(increase_p0)

        increase_15 = (input_day.average_15 / input_day.average_90) * 0.01
        i.append(increase_15)

        increase_30 = (input_day.average_30 / input_day.average_90) * 0.01
        i.append(increase_30)

        i.append(always_increase(input_day.price_list))

        fi = []
        for e in i:
            fi.append(float(e))
            if (e > 1) or (e < 0):
                print('ERROR:')
                print(e)
                print(i)

        i = torch.tensor(fi)

        output = self.activation(self.input_layer(i)) # pasada por la capa entrada
        output = self.activation(self.hidden_layer(output))   # pasada por la capa oculta
        output = self.output_layer(output)                    # pasada por la capa de salida
        return output


    def learn(self, day):
        loss_function = nn.MSELoss() #función de pérdidas
        parameters = self.parameters()
        optimizer = optim.Adam(params=parameters, lr=0.001) #algoritmo usado para optimizar los parámetros
        losses = np.array([]) #array que guarda la pérdida en cada iteración

        output = self(day) #calcular la salida para una imagen
        self.zero_grad() #poner los gradientes a cero en cada iteración

        if int(day.valoration) == 0:
            target = torch.tensor([0.0, 1.0])
        else:
            target = torch.tensor([1.0, 0.0])

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
            ret += 0.01
        else:
            increase = False
    return ret
