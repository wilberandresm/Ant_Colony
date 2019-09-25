import numpy as np
import string, math, random
from copy import deepcopy
from tqdm import tqdm
import template as t

def localHeuristics(matriz,col,row): #divide 1/distancias
    matrizHL = deepcopy(matriz)
    for i in range(row):
        for j in range(col):
            if(matrizHL[i][j] != 0 ):
                matrizHL[i][j] = 1/matrizHL[i][j]#division
    return np.array(matrizHL)

def ObjetiveFunction(route,distances): 
    sum=0
    for i in range(len(route)-1): 
        fromCity=route[i]
        toCity=route[i+1]
        sum=sum+distances[fromCity][toCity]
    return sum#suma del recorrido 

def generateRoutes(nCities, pos, matriz):

    aux_list=[]
    for i in range(nCities):
        if(i!=pos):
            aux_list.append(i)#agregar cada valor a la lista auxiliar

    route=[pos]
    while len(aux_list)>0:
        aux = random.choice(aux_list)#escoge un valor aleatorio de la lista
        aux_list.remove(aux)
        route.append(aux)
    route.append(pos)
    z = ObjetiveFunction(route,matriz)

    return route,z

def initialPheromone(matriz, n, pos):
    pheromone = np.zeros(np.shape(matriz))#misma matriz pero inicializada en cero 
    while(n>0):
        nSolution, z = generateRoutes(len(matriz),pos, matriz)#se debe a que la matriz de feromonas se actualiza 
        inverseZ=1/z #1 sobre el cos.sum(axis=0)te del tour
        for i in range(len(nSolution)-1):
            fromCity=nSolution[i]
            toCity=nSolution[i+1]
            pheromone[fromCity][toCity]+=inverseZ#se suma la concentración de feromonas nuevas

        n-=1
    return pheromone

def evaporation(pheromone):
    p = 0.1
    for i in range(len(pheromone)):
        for j in range(len(pheromone[0])):
            pheromone[i][j] = pheromone[i][j]*(1-p)
    return pheromone

def Probabilities(local_heu,pheromone,alpha,beta,positions):

    matriz=(pheromone**alpha)*(local_heu**beta)

    for i in positions:
        matriz[i,:]=0
        
    summation=matriz.sum(axis=0)

    probabilities=matriz/summation
    return probabilities

def accumulatedPositions(probability,ran,positions):
    accumulated=0
    for i in range(len(probability)):
        accumulated+=probability[i]
        if probability[i] in positions:
            continue
        else:
            if(accumulated>ran):
                return i
    return 0

def addPheromone(pheromone,solution,distances):
    aux_pheromone = deepcopy(pheromone)
    z = ObjetiveFunction(solution,distances)
    inverse_z = 1/z
    for i in range(len(solution)-1):
        fromCity = solution[i]
        toCity = solution[i+1]
        aux_pheromone[fromCity][toCity] += inverse_z
    
    return np.array(aux_pheromone)

def generatePath(local_heu,pheromone,alpha,beta,pos):
    counter=0
    positions=[pos]
    while(len(positions)<len(pheromone)):
        ran=random.random()
        probabilities=Probabilities(local_heu,pheromone,alpha,beta,positions)
        positions.append(accumulatedPositions(probabilities[:,positions[counter]],ran,positions))
        counter+=1
    positions.append(pos)
    return positions

if __name__ == "__main__":
    coor = t.distancesFromCoords()#obtención de las distancias para establecer coordenadas
    #distances = distancesFromCoords()
  # pos = random.randint(0,len(distances)-1)
    pos = random.randint(0,len(coor)-1)
    cities = len(coor)
    while(True):
        n = input("Number of initial tours: ")
        try:
            n = int(n)
            if(n<0):
                print("\nInvalid number!\n")
            else:
                break
        except ValueError:
            print("\nInsert a number!\n")
    while(True):
        alpha = input("Alpha: ")
        try:
            alpha = int(alpha)
            if(alpha<0):
                print("\nInvalid number!\n")
            else:
                break
        except ValueError:
            print("\nInsert a number!\n")
    while(True):
        beta = input("Beta: ")
        try:
            beta = int(beta)
            if(beta<0):
                print("\nInvalid number!\n")
            else:
                break
        except ValueError:
            print("\nInsert a number!\n")
    while(True):
        iterations = input("Iterations: ")#hormigas
        try:
            iterations = int(iterations)
            if(iterations<0):
                print("\nInvalid number!\n")
            else:
                break
        except ValueError:
            print("\nInsert a number!\n")
            
    local_h = localHeuristics(coor,len(coor[0]),cities) #matriz de heuristica local
    pheromone_matrix = initialPheromone(coor,n, pos) 
    for i in tqdm(range(iterations)):#iterar para el numero de hormigas
        solution = generatePath(local_h,pheromone_matrix,alpha,beta, pos)
        pheromone_matrix = addPheromone(pheromone_matrix,solution,coor)
        pheromone_matrix = evaporation(pheromone_matrix)
        
    print("\nSolution for TSP:")
    print(solution)
    print("z:" ,ObjetiveFunction(solution,coor))