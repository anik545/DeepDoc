import json
import string 
import random

with open ("../NN/NN_test","r") as f:
    lines = [[float(i.replace('\n','')) for i in x.split(',')] for x in f.readlines()]
    print(lines)
    with open("data.json","r") as d:
        j = json.load(d)
        for x in lines:
            id = ''.join([str(random.randint(0,9)) for x in range(len(str(100001326800715)))])
            n = "".join([random.choice(string.ascii_lowercase) for y in range(5)])
            j[id] = {"pains":{},"name":n,"model":x}
    print(j)
    with open("data.json","w") as d_:
        json.dump(j,d_)