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
    for n in range(40):
        list = f.readline().split()
        film_id.append(list[0].split("/")[4])
        film_name.append(list[1])
        pos_rew.append(list[-2])
        neg_rew.append(list[-1])
        neg_k += int(list[-1])
        pos_k += int(list[-2])
        proz += int(int(list[-2]) * 0.084)+1
        raz += int(int(list[-2]) * 0.084)+1 - int(list[-1])
        print(f"{int(list[-2])}~{int(int(list[-2]) * 0.084)+1} - {int(list[-1])} = {int(int(list[-2]) * 0.084)+1 - int(list[-1])}")
print(f"{pos_k}~{proz} - {neg_k} = {raz}")


"""perpa = [x - (int(int(rew) * 0.084) + 1) for x in per]
    #print(x for x in perpa)
    ags = zip(per, perpa)
    perpaz = min([abs(r) for v, r in ags])
    vsego = (v for v, r in ags if r == perpaz)
    #print(x for x in vsego)
    print(f"~ {perpaz}")"""
"""mni = 1000
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



"""n = 0 
for rew in pos_rew:
    mni = 1000
    perpage = 10
    for x in per:
        perpa = x - (int(int(rew) * 0.084) + 1) 
        if abs(perpa) < mni:
            mni = abs(perpa)
            perpage = x
            #print(f"{mni} == {x}")
    if perpage <= (int(int(rew) * 0.084) + 1) and (perpage *2 - (int(int(rew) * 0.084) + 1) > 10):
        print(f"##### {n}: {(int(int(rew) * 0.084) + 1)} ~ {perpage}   ~~~~:{perpage if (perpage *2 - (int(int(rew) * 0.084) + 1) <= 10) else 0}")
    n+=1
print("\n\n")
n = 0
for rew in neg_rew:
    mni = 1000
    perpage = 10
    for x in per:
        perpa = x - int(rew)
        if abs(perpa) < mni:
            mni = abs(perpa)
            perpage = x
            #print(f"{mni} == {x}")
    if perpage <= int(rew) and (perpage *2 - int(rew)> 10):
        print(f"##### {n}: {int(rew)} ~ {perpage}   ~~~~:{perpage  if (perpage * 2 - int(rew) <= 10) else 0}")
    n+=1"""

"""raspr = []
for x in per:
    for y in per:
        if x <= y:
            raspr.append(f"{x}.{y} ~ {x+y}")
for x in raspr:
    print(x)"""

divisors = {}
for num in per:
    divs = []
    for other in per:
        if other < num and num % other == 0:
            divs.append(other)
    divisors[num] = divs

#rasp = dict()
for stat in (pos_rew, neg_rew):
    print(f"\n\n{stat} ")
    for flm in stat:
        fil = int(flm) if stat == neg_rew else int(int(flm) * 0.084)+1
        for pe in per:
            dop = ""
            pag = 1
            while True:
                if pe*pag >= fil:
                    break
                else:
                    pag+=1
            if pag > 1 and divisors[pe]:
                sled = divisors[pe][0]
                sp = int(pe // sled) + 1
                dop = f"{sled} : {sp}"
            #rasp.update({pe : pag})
            print(f"{pe} : {pag} -> {dop}")
"""
200 : 1 ->
100 : 2 -> 50 : 3
75 : 3 -> 25 : 4
50 : 4 -> 25 : 3

гипотеза: int(pe//sled) из sр=int(pe//sled)+1 следует увеличивать на пейдж-1"""



"""for x in divisors.items():
    print(x)

def build_chains(current, chain):
    chain.append(current)
    if divisors[current]:
        for d in divisors[current]:
            build_chains(d, chain.copy())
    else:
        print(' -> '.join(map(str, chain)))

for start in per:
    build_chains(start, [])"""

#print(rasp.items())



        
def get_films():
    return zip(film_id, film_name, pos_rew, neg_rew)