from util import coach
from nn import ted
import torch

t = ted.Ted()
c = coach.Coach(t)
c.set_iterations(80000, 20000)
c.set_collection('Minutes (Ted)')
c.train()
torch.save(t.state_dict(), 'ted_2.pkl')
