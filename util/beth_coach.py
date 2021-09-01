import pymongo
from model import training
from model import minute
from util import configuration
import datetime

configuration = configuration.Configuration()

class Coach:
    def __init__(self, nn):
        self.nn = nn
        self.training_iterations = 0
        self.epochs = 1
        self.test_iterations = 0
        self.collection = 'Minutes'

    def set_iterations(self, training_iterations, test_iterations):
        self.training_iterations = training_iterations
        self.test_iterations = test_iterations

    def set_collection(self, collection):
        self.collection = collection


    def train(self):
        mongo_client = pymongo.MongoClient(host=[configuration.mongo_uri])
        db = mongo_client['NN3']
        collection = db[self.collection]
        collection = collection.find()

        minute_list = []
        for element in collection:
            minute_list.append(element)

        print('In!')

        for epoch in range(self.epochs):
            for element in minute_list[: self.training_iterations]:
                m = minute.from_dict(element)

        test_result = 0
        if (self.nn.type == 'classifier') :
            for element in minute_list[self.training_iterations : (self.training_iterations + self.test_iterations)]:
                m = minute.from_dict(element)

                if(float(self.nn(m)[0][0].item()) > float(self.nn(m)[0][1].item())):
                    result = 1
                else:
                    result = 0
                print('Pred: ' + str(result) + '  Res:' + str(element['valoration']))
                if (compare(element['valoration'], result)):
                    test_result += 1 / self.test_iterations
        else:
            for element in minute_list[self.training_iterations : (self.training_iterations + self.test_iterations)]:
                m = minute.from_dict(element)
                result = float(self.nn(m)[0].item())
                loss = 0
                if(element['result'] < result):
                    loss = result - element['result']
                if(element['result'] > result):
                    loss = element['result'] - result
                test_result += loss / self.test_iterations
        
        t = training.Training(type(self.nn), self.training_iterations, self.test_iterations, self.epochs)
        if(self.nn.type == 'classifier'):
            t.set_avg_success(test_result)
        else:
            t.set_avg_error(test_result)

        db['Trainings'].insert_one(t.to_dict())

def compare(x, y):
    if x == 0:
        if y < 0.5:
            return True
        else:
            return False
    if x == 1:
        if y > 0.5:
            return True
        else:
            return False
