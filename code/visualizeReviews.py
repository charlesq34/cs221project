import pickle
b1 = pickle.load(open('business1.dict','rb'))
keys = [k for k in b1]
for r in b1[keys[0]]:
    print r,'\n'
