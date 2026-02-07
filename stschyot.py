import os
path = os.path.join("dataset", "topyat.txt")
neg_k = 0
pos_k = 0
proz = 0
raz = 0
with open(path, "r", encoding="utf-8") as f:
    for n in range(40):
        list = f.readline().split()
        neg_k += int(list[-1])
        pos_k += int(list[-2])
        proz += int(int(list[-2]) * 0.084)+1
        raz += int(int(list[-2]) * 0.084)+1 - int(list[-1])
        print(f"{int(list[-2])}~{int(int(list[-2]) * 0.084)+1} - {int(list[-1])} = {int(int(list[-2]) * 0.084)+1 - int(list[-1])}")
print(f"{pos_k}~{proz} - {neg_k} = {raz}")