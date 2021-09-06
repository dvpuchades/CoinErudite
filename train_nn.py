from util import coach
from util import beth_coach
from util import richard_coach
from util import jared_coach
from nn import ted
from nn import beth
from nn import beth_2
from nn import rick
from nn import richard
from nn import jared
import torch

# nn = richard.Richard()
nn = jared.Jared()
# nn = beth_2.Beth()
# nn.load_state_dict(torch.load('ted_3.pkl'))
c = jared_coach.Coach(nn)
c.set_iterations(4000, 1000)
c.epochs = 7
c.set_collection('Days')
c.train()
# torch.save(t.state_dict(), 'ted_4.pkl')