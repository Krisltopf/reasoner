import numpy as np


compositions = np.load("compositions.npy")

base_relations = 13
num_relations = pow(2, base_relations)
relation1 = num_relations-1

new_compositions = np.zeros((num_relations, num_relations), dtype=int)
new_compositions[:num_relations, :num_relations] = compositions

for relation2 in range(num_relations):
    new_compositions[relation1][relation2] = relation1
    new_compositions[relation2][relation1] = relation1

new_compositions[num_relations-1][0] = 0
new_compositions[0][num_relations-1] = 0

print(new_compositions)
np.save("compositions.npy", new_compositions)