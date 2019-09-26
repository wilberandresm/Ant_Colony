import numpy as np
import string, math, random
from copy import deepcopy
import template as t

def HeuristicaLocal(matriz,columna,fila): #divide 1/distancias
    matrizHL = deepcopy(matriz)
    for i in range(fila):
        for j in range(columna):
            if(matrizHL[i][j] != 0 ):
                matrizHL[i][j] = 1/matrizHL[i][j]#division
    return np.array(matrizHL)

def ObjetiveFunction(ruta,distances): 
    sum=0
    for i in range(len(ruta)-1): 
        DelaCiudad=ruta[i]
        AlaCiudad=ruta[i+1]
        sum=sum+distances[DelaCiudad][AlaCiudad]
    return sum#suma del recorrido 

def generarTours(nCities, pos, matriz):
    aux_list=[]
    for i in range(nCities):
        if(i!=pos):
            aux_list.append(i)#agregar cada valor a la lista auxiliar

    ruta=[pos]
    while len(aux_list)>0:
        aux = random.choice(aux_list)#escoge un valor aleatorio de la lista
        aux_list.remove(aux)
        ruta.append(aux)
    ruta.append(pos)
    z = ObjetiveFunction(ruta,matriz)

    return ruta,z

def evaporacion(pheromone):
    p = 0.1#factor de evaporación
    for i in range(len(pheromone)):
        for j in range(len(pheromone[0])):
            pheromone[i][j] = pheromone[i][j]*(1-p)
    return pheromone

def acumulandoPosiciones(probability,ran,positions):
    accumulated=0
    for i in range(len(probability)):
        accumulated+=probability[i]
        if probability[i] in positions:
            continue
        else:
            if(accumulated>ran):
                return i
    return 0

def SumarFeromonas(pheromone,solution,distances):
    aux_pheromone = deepcopy(pheromone)
    z = ObjetiveFunction(solution,distances)
    inverse_z = 1/z
    for i in range(len(solution)-1):
        DelaCiudad = solution[i]
        AlaCiudad = solution[i+1]
        aux_pheromone[DelaCiudad][AlaCiudad] += inverse_z
    
    return np.array(aux_pheromone)

def GenerarCamino(local_heu,pheromone,alpha,beta,pos):
    counter=0
    positions=[pos]
    while(len(positions)<len(pheromone)):
        ran=random.random()
        matriz=(pheromone**alpha)*(local_heu**beta)
        for i in positions:
            matriz[i,:]=0   
        summation=matriz.sum(axis=0)
        probabilities=matriz/summation 
        positions.append(acumulandoPosiciones(probabilities[:,positions[counter]],ran,positions))
        counter+=1
    positions.append(pos)
    return positions

if __name__ == "__main__":
    coor = t.distancesFromCoords()#obtención de las distancias para establecer coordenadas
    pos = random.randint(0,len(coor)-1)
    cities = len(coor)
    n = int(input("Numero de hormigas exploradoras: "))#hormigas exploradoras
    
    while(n<=0):
        print("\nNúmero invalido , ingrese uno mayor de 0 ")
        n = int(input("Numero de hormigas exploradoras: "))

    alpha = int(input("Alpha: "))

    while(alpha<0):
        print("\nDigite un valor correcto ")
        alpha = int(input("Numero de hormigas exploradoras: "))

    beta = int(input("Beta: "))

    while(beta<0):
        print("\nDigite un valor correcto ")
        beta = int(input("Numero de hormigas exploradoras: "))
    
    iterations = int(input("Iteraciones: "))#hormigas
    while(iterations<=0):
        print("\nDigite un valor correcto ")
        iterations = int(input("Numero de hormigas exploradoras: "))

    local_h = HeuristicaLocal(coor,len(coor[0]),cities) #matriz de heuristica local
    #pheromone_matrix = initialPheromone(coor,n, pos) 
    pheromone_matrix = np.zeros(np.shape(coor))#misma matriz pero inicializada en cero 
    while(n>0):
        nSolution, z = generarTours(len(coor),pos, coor)#se debe a que la matriz de feromonas se actualiza 
        inverseZ=1/z #1 sobre el cos.sum(axis=0)te del tour
        for i in range(len(nSolution)-1):
            DelaCiudad=nSolution[i]
            AlaCiudad=nSolution[i+1]
            pheromone_matrix[DelaCiudad][AlaCiudad]+=inverseZ#se suma la concentración de feromonas nuevas
        n-=1

    for i in range(iterations):#iterar para el numero de hormigas
        solution = GenerarCamino(local_h,pheromone_matrix,alpha,beta, pos)
        pheromone_matrix = SumarFeromonas(pheromone_matrix,solution,coor)
        pheromone_matrix = evaporacion(pheromone_matrix)
        
    print("\nSolución para el TSP:")
    print(solution)
    print("z:" ,ObjetiveFunction(solution,coor))