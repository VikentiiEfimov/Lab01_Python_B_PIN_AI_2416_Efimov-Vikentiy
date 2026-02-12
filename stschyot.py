import os
path = os.path.join("dataset", "topyat.txt")
neg_k = 0
pos_k = 0
proz = 0
raz = 0
film_id = []
film_name = []
pos_rew = []
neg_rew = []
per = [200, 100, 75, 50, 25, 10]
with open(path, "r", encoding="utf-8") as f:
    for n in range(39):
        list = f.readline().split()
        film_id.append(list[0].split("/")[4])
        film_name.append(' '.join(list[1:-3]))
        pos_rew.append(list[-2])
        neg_rew.append(list[-1])
        neg_k += int(list[-1])
        pos_k += int(list[-2])
        proz += int(int(list[-2]) * 0.084)+1
        raz += int(int(list[-2]) * 0.084)+1 - int(list[-1])
        #print(f"{int(list[-2])}~{int(int(list[-2]) * 0.084)+1} - {int(list[-1])} = {int(int(list[-2]) * 0.084)+1 - int(list[-1])}")
#print(f"{pos_k}~{proz} - {neg_k} = {raz}")


"""perpa = [x - (int(int(rew) * 0.084) + 1) for x in per]
    #print(x for x in perpa)
    ags = zip(per, perpa)
    perpaz = min([abs(r) for v, r in ags])
    vsego = (v for v, r in ags if r == perpaz)
    #print(x for x in vsego)
    print(f"~ {perpaz}")
    mni = 1000
    perpage = 10
    for x in per:
        for y in per:
            if x <= y:
                perpa = x +y - (int(int(rew) * 0.084) + 1)
                #print(f"{perpa} == {x +y}")
                if abs(perpa) < mni:
                    mni = abs(perpa)
                    perpage = x +y
                    print(f"{mni} == {x} + {y}")
    #if perpage - (int(int(rew) * 0.084) + 1) < 0:
    print(f"##### {n}: {(int(int(rew) * 0.084) + 1)} ~ {perpage}")
    n+=1"""

        
def get_films():
    return zip(film_id, film_name, pos_rew, neg_rew)