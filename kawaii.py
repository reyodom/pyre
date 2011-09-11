# Weeaboo module.
# Speaking of weeaboos, why not make a contract with me...

import random
facesAreLoaded='no'
facelist=[]

def loadfaces():
    global facelist
    global facesAreLoaded
    faces=open("kawaii.desu")
    facelist = faces.readlines()
    faces.close()
    for i, face in enumerate(facelist):
        facelist[i]=face.rstrip("\n")
    facesAreLoaded='yes'
    return 'OK'

def getface():
    facenum = random.randint(0,26)
    return str(facelist[facenum])
    