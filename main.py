from z3 import Int, And, Or, If, Solver
import numpy as np

# feature: ((pins that implement...,), ...required pins)

bundles = {0: ((0,), (1,)), 1: ((0, 2), (1, 3))}

FEATURE_COUNT = len(bundles.items())
req_features = [0, 1]

z3pins = []
for pin in np.arange(4):
    z3pins.append(Int(f"pin_{pin}"))

valid_feature = [And(0 <= z3pin, z3pin <= FEATURE_COUNT) for z3pin in z3pins]

feature_constraints = []
for fid in req_features:
    reqs = bundles[fid]
    current_cond = True
    pin_conds = []
    for pinids in reqs:
        pin_conds.append(Or(*[z3pins[pinid] == fid for pinid in pinids]))
    
    feature_constraints.append(And(*pin_conds))

print(z3pins)

solver = Solver()
solver.add(valid_feature)
solver.add(feature_constraints)

print(f"{feature_constraints=}")
print(f"{valid_feature=}")

print(solver.check())
print(solver.model())