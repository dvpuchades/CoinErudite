from util import coach
from nn import homer

h = homer.Homer()
c = coach.Coach(h)
c.set_iterations(30000, 20000)
c.train()
