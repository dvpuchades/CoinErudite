from util import bank
from nn import randy
import torch

t = randy.Randy()
# t.load_state_dict(torch.load('ted_3.pkl'))
b = bank.Bank(0.2, 0.5, t)
b.on_air_new_edition()