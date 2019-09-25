import string, math
def distancesFromCoords():
    f = open('berlin52.tsp')
    data = [line.replace("\n","").split(" ")[1:] for line in f.readlines()[6:58]]
    coords =  list(map(lambda x: [float(x[0]),float(x[1])], data))
    distances = []
    for i in range(len(coords)):
        row = []
        for j in range(len(coords)):
            row.append(math.sqrt((coords[i][0]-coords[j][0])**2 + (coords[i][1]-coords[j][1])**2))
        distances.append(row)
    return distances

