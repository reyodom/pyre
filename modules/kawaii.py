# Weeaboo module.
# Speaking of weeaboos, why not make a contract with me...

class Weeaboo():
    from random import randint
    facesAreLoaded = False
    facelist = []
    def __init__(self):
        faces=open("kawaii.desu")
        self.facelist = faces.readlines()
        faces.close()
        for i, face in enumerate(self.facelist):
            self.facelist[i]=face.rstrip("\n")
        self.facesAreLoaded='yes'
    
    def getFace(self, Channel, ws):
        facenum = randint(0, len(self.facelist) - 1)
        ws("PRIVMSG {0} :{1}\r\n".format(Channel, self.facelist[facenum]))
        