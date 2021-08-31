from util import coach
from util import beth_coach
from util import richard_coach
from nn import ted
from nn import beth
from nn import rick
from nn import richard
import torch

nn = richard.Richard()
# nn.load_state_dict(torch.load('ted_3.pkl'))
c = richard_coach.Coach(nn)
c.set_iterations(4300, 1000)
c.epochs = 7
c.set_collection('Days')
c.train()
# torch.save(t.state_dict(), 'ted_4.pkl')