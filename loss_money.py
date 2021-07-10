from util import bank
from nn import ted
import torch

t = ted.Ted()
t.load_state_dict(torch.load('ted_2.pkl'))
b = bank.Bank(0.2, 0.5, t)
b.on_air()