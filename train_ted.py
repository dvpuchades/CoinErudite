from util import coach
from nn import ted

h = ted.Ted()
c = coach.coach(h)
c.set_iterations(30000, 30000)
c.train()
