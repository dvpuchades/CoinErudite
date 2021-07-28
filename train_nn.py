from util import coach
from nn import ted
from nn import beth
from nn import rick
import torch

nn = rick.Rick()
# nn.load_state_dict(torch.load('ted_3.pkl'))
c = coach.Coach(nn)
c.set_iterations(0, 10000)
c.epochs = 2
c.set_collection('Minutes')
c.train()
# torch.save(t.state_dict(), 'ted_4.pkl')