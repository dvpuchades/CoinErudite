from util import coach
from util import beth_coach
from util import richard_coach
from nn import ted
from nn import beth
from nn import beth_2
from nn import rick
from nn import richard
import torch

nn = richard.Richard()
nn = beth_2.Beth()
# nn.load_state_dict(torch.load('ted_3.pkl'))
c = beth_coach.Coach(nn)
c.set_iterations(130000, 10000)
c.epochs = 3
c.set_collection('Minutes')
c.train()
# torch.save(t.state_dict(), 'ted_4.pkl')