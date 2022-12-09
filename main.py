from z3 import Int, Solver, And, Or
import numpy as np

FEATURE_COUNT = 1
features = ["f1", "f2"]
feature = {feature_name:fid for fid, feature_name in enumerate(features)}

bundles = {"f1": ((0,), (1,)), "f2": ((0, 2), (1, 3))}

pins = np.arange(4)

z3pins = []
for pin in pins:
    z3pins.append(Int(f"pin_{pin}"))

valid_feature = [And(0 <= z3pin, z3pin <= FEATURE_COUNT) for z3pin in z3pins]

feature_constraints = []
for to_implement in features:
    fid = feature[to_implement]
    reqs = bundles[to_implement]
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