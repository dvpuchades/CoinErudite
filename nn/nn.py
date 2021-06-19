
#   https://www.paradigmadigital.com/dev/introduccion-pytorch/

import torch.nn as nn
#definimos la red neuronal 
class Classifier(nn.Module):
    def __init__(self):
        super(Classifier,self).__init__()
        self.input_layer = nn.Linear(28*28,100)
        self.hidden_layer = nn.Linear(100,50)
        self.output_layer = nn.Linear(50,10)
        self.activation = nn.ReLU()

    def forward(self, input_image):
        input_image = input_image.view(-1,28*28)                     #convertimos la imagen a vector
        output = self.activation(self.input_layer(input_image)) #pasada por la capa entrada
        output = self.activation(self.hidden_layer(output))   #pasada por la capa oculta
        output = self.output_layer(output)                    #pasada por la capa de salida
        return output


from torch import optim
import numpy as np
classifier = Classifier() #instanciamos la RN
loss_function = nn.CrossEntropyLoss() #función de pérdidas
parameters = classifier.parameters()
optimizer = optim.Adam(params=parameters, lr=0.001) #algoritmo usado para optimizar los parámetros
epochs = 3 #número de veces que pasamos cada muestra a la RN durante el entrenamiento
iterations = 0 #número total de iterations para mostrar el error
losses = np.array([]) #array que guarda la pérdida en cada iteración


from torch.autograd import Variable #necesario para calcular gradientes
for e in range(epochs):
    for i, (images, tags) in enumerate(image_loader):
        images, tags = Variable(images), Variable(tags) #Convertir a variable para derivación
        output = classifier(images) #calcular la salida para una imagen
        classifier.zero_grad() #poner los gradientes a cero en cada iteración
        error = loss_function(output, tags) #calcular el error
        error.backward() #obtener los gradientes y propagar
        optimizer.step() #actualizar los pesos con los gradientes
        iterations += 1
        losses = np.append(losses,error.item())

