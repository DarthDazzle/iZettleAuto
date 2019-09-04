from iZettleUsers import *
import pickle

def saveUserDateMap(UserDateMap):
    with open("dates.pickle","wb") as f:
        pickle.dump(UserDateMap, f)

userDateMap = dict()
for user in users:
    userDateMap[user] = set()
saveUserDateMap(userDateMap)
