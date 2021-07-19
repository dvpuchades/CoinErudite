from util import bank
from nn import ted
import torch

t = ted.Ted()
t.load_state_dict(torch.load('ted_3.pkl'))
b = bank.Bank(0.125, 1, t)
b.on_air()