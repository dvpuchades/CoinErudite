from util import coach
from nn import ted
import torch

t = ted.Ted()
c = coach.Coach(t)
c.set_iterations(100000, 3000)
c.set_collection('Minutes')
c.train()
torch.save(t.state_dict(), 'ted_3.pkl')
