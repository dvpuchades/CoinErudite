from util import coach
from nn import ted

h = ted.Ted()
c = coach.coach(h)
c.set_iterations(20000, 45000)
c.train()
