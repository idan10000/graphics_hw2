from classes.Cube import Cube
from classes.Light import Light
from classes.Material import Material
from classes.Plane import Plane
from classes.Sphere import Sphere
from classes.camera import Camera
from classes.settings import Settings


def parseScene(dataPath):
    output = {"mtls": [], "plns": [], "sphs": [], "lgts": [], "cubs": []}
    f = open(dataPath,'r')
    lines = f.readlines()
    for line in lines:
        values = line.split()
        if len(values) > 0:
            if values[0] == "cam":
                output["cam"] = Camera(*[float(x) for x in values[1:]])
            elif values[0] == "set":
                output["set"] = Settings(*[float(x) for x in values[1:]])
            elif values[0] == "mtl":
                output["mtls"].append(Material(*[float(x) for x in values[1:]]))
            elif values[0] == "pln":
                output["plns"].append(Plane(*[float(x) for x in values[1:-1]], output["mtls"][int(values[-1]) - 1]))
            elif values[0] == "sph":
                output["sphs"].append(Sphere(*[float(x) for x in values[1:-1]], output["mtls"][int(values[-1]) - 1]))
            elif values[0] == "cub":
                output["cubs"].append(Cube(*[float(x) for x in values[1:-1]], output["mtls"][int(values[-1]) - 1]))
            elif values[0] == "lgt":
                output["lgts"].append(Light(*[float(x) for x in values[1:]]))

    return output


if __name__ == '__main__':
    parseScene(r"C:\Users\idanp\OneDrive\Documents\University\Graphics\Homework\hw2\pool.txt")
