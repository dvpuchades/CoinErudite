from util import coach
from nn import ted
from nn import barney
from nn import eleven
import torch

nn = eleven.Eleven()
# nn.load_state_dict(torch.load('ted_3.pkl'))
c = coach.Coach(nn)
c.set_iterations(20000, 1000)
c.epochs = 3
c.set_collection('Minutes')
c.train()
# torch.save(t.state_dict(), 'ted_4.pkl')