#!/usr/bin/env python
from timeit import Timer

formula = '6x4d6M3'
count = 1000000

t = Timer("parse(formula)", setup=f"from dice.parser import parse; formula='{formula}'")
value = t.timeit(count)  # this takes about 0.3 seconds on my machine

print(f'Performed {count} iterations in {value:.3f} seconds using formula: "{formula}".')
