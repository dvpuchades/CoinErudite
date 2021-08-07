from util import coach
from util import beth_coach
from nn import ted
from nn import beth
from nn import rick
import torch

nn = beth.Beth()
# nn.load_state_dict(torch.load('ted_3.pkl'))
c = beth_coach.Coach(nn)
c.set_iterations(110000, 30000)
c.epochs = 3
c.set_collection('Minutes')
c.train()
# torch.save(t.state_dict(), 'ted_4.pkl')