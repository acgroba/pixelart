from PIL import Image, ImageFilter
import numpy as np
import sys
import json



class Numberize():
    def __init__(self, p, s=20):
        self.im = Image.open(p)
        self.size = (s,s)

    def run(self):
        numberized = np.array(self.im.convert("L").resize(self.size))
        values = np.sort(np.unique(numberized))
        
        number = 0
        for value in values:
            numberized[numberized == value ] = number
            number += 1
        
        return numberized


if __name__ == "__main__":
    with open("image.json", 'w') as outfile:
    
        if len(sys.argv) == 3:
            json.dump(Numberize(sys.argv[1], int(sys.argv[2])).run().tolist(), outfile)
        elif len(sys.argv) == 2:
            json.dump(Numberize(sys.argv[1]).run().tolist(), outfile)
        else:
            print("Incorrect parameters")