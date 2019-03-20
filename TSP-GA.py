##
import pandas as pd
import random
import networkx as nx
import matplotlib.pyplot as plt
import itertools
import math

def takeInput():
    n=int(input("Enter no. of cities : "))
    #input for city names
    response=True
    while response==True:
        response=input("Use random city name ? (Y/N) : ")
        if response=='Y' or response=='y':
            try:
                df = pd.read_csv('cities.csv')
                for index,row in df.iterrows():
                    if index == n:
                        break
                    city.append(row['City'])
            except FileNotFoundError:
                print('FileNotFoundError: cities.csv')
                #create exit
        elif response=='n' or response=='N':
            for i in range(n):
                city.append(input())
        else:
            response=True
            print('Wrong input')
            
    ## Displaying generated city list
    for i in range(len(city)):
        print(i+1,city[i])

    #input for distance in between cities
    response=True
    while response==True:
        response=input("Use random city distance ? (Y/N) : ")
        if response=='Y' or response=='y':
            for i in range(n):
                temp=[]
                for j in range(n):
                    if i==j:
                        temp.append(0)
                    elif j<i:
                        temp.append(distance[j][i])
                    else:
                        # Auto generated distance is in between 1 and 50
                        temp.append(random.randint(1, 50))
                distance.append(temp)
        elif response=='n' or response=='N':
            for i in range(n):
                temp=[]
                for j in range(n):
                    if i==j:
                        temp.append(0)
                    elif j<i:
                        temp.append(distance[j][i])
                    else:
                        temp.append(int(input("From city %s to %s: "%(city[i],city[j]))))
                distance.append(temp)
        else:
            response=True
            print('Wrong input')

    ## modifying auto generated input
    print("=====CITY DISTANCE TABLE=====")
    print(*distance,sep="\n")
    response=True
    while response==True:
        response=input("Do you want to modify any distance ? (Y/N)")
        if response=='Y' or response=='y':
            i=int(input("Enter i : "))
            j=int(input("Enter j : "))
            temp=int(input("Enter distance : "))
            distance[i][j]=temp
            print("=====NEW CITY DISTANCE TABLE=====")
            print(*distance,sep="\n")
            response=True
        elif response=='N' or response=='n':
            break
        else:
            response=True
            print('Wrong input')
            
    return


## To create a graph for drawGarph function
## The parameter is in List format which needs to be formatted as
## graph = [(20, 21), (21, 22), (22, 23), (23, 24), (24, 25), (25, 20)]
## label = [0, 1, 2, 3, 4, 5]
def createGraph(gList,gType):
    g=[]
    d=[]
    if gType=='path':
        for i in range(len(gList)-1):
            g.append((gList[i],gList[i+1]))
    elif gType=='complete':         ##Processing the upper right Triange part of the 2D list
        for i in range(len(gList)):
            for j in range(i+1,len(gList)):
                d.append(distance[i][j])
                g.append((gList[i],gList[j]))
    return [g,d]


## To visualize the graph
def drawGraph(EdgeWeight):

    #print(EdgeWeight)
    graph=EdgeWeight[0]
    labels=EdgeWeight[1]
    
    # create networkx graph
    G=nx.Graph()
    
    # add edges
    for edge in graph:
        G.add_edge(edge[0], edge[1])
    
    # There are graph layouts like shell, spring, spectral and random.
    graph_pos = nx.shell_layout(G)
##    colorMap = []
##    for node in G:
##        if node==city[hometown]:colorMap.append('red')
##        else:colorMap.append('blue')
    # draw nodes, edges and labels
    nx.draw_networkx_nodes(G, graph_pos, node_size=1000, node_color='blue', alpha=0.3)
    nx.draw_networkx_edges(G, graph_pos)
    nx.draw_networkx_labels(G, graph_pos, font_size=12, font_family='sans-serif')

    edge_labels = dict(zip(graph, labels))
    # {(23, 20): 7, (22, 23): 2, (20, 21): 10, (24, 25): 4, (21, 22): 1, (25, 20): 5, (24, 22): 8, (25, 21): 6, (23, 24): 3, (21, 24): 9}

    nx.draw_networkx_edge_labels(G, graph_pos, edge_labels=edge_labels)

    # show graph
    plt.show()
    return

## To generate random population of solution
def generatePopulation():
    ##    pathSeq is a list of city indices
    pathSeq=list(range(0,len(city)))
    ##    taking 30% chromosome of the population for the process
    ##    means, 30% of the total no of permutations
    populationSize=int(math.factorial(len(city)-1)*0.3)
    ##    populationSize is always taken as even no. for good crossover
    if populationSize%2!=0:
        populationSize+=1
    ##    samples contains 30% of permutations of pathSeq in list of tuples order
    samples=random.sample(list(itertools.permutations(pathSeq)), populationSize)
    ##    population contains chromosomes in list order
    for i in samples:
        population.append(list(i))
    random.shuffle(population)
    return

##  To calculate fitness of each chromosomes
def calculateFitness():
    global sumFX,avgFX,maxFX
    ##  xVal = Di, f(xVal)=100/xVal upto 3 decimal places
    sumFX,avgFX,maxFX=0,0,0
    for chromosome in population:
        temp=0
        for i in range(-1,len(chromosome)-1):
            temp+=distance[int(chromosome[i])][int(chromosome[i+1])]
        xVal.append(temp)
        f=round(100/temp,3)
        sumFX+=f
        if maxFX<f:
            maxFX=f
        fitness.append(f)
    sumFX=round(sumFX,3)
    avgFX=round(sumFX/len(population),3)
    return

##  To calculate probability and Actual Count of each chromosome
##  prob(i)=(f(x) of i or Fitness of i)/sumFX
##  expCount(i)=(f(x) of i or Fitness of i)/avgFX
def calculateProbCount():
    for chromosomeIndex in range(len(population)):
        f=fitness[chromosomeIndex]
        prob.append(round(f*100/sumFX,3))
        expCount.append(round(f/avgFX,3))
    return

##  Roulette wheel selection
def rouletteWheel():
    pick    = random.uniform(0, sumFX)
    current = 0
    for chromosome in population:
        current += fitness[population.index(chromosome)]
        if current > pick:
            if len(newPopulation)<len(population):
                newPopulation.append(chromosome)
                rouletteWheel()
            else:
                return

                
def printResult():
    temp=pd.DataFrame(
        {
            'Chromosome'    :   population,
            'X-Value'       :   xVal,
            'Fitness'       :   fitness,
            'Prob(%)'       :   prob,
            'Exp.Count'     :   expCount
        })
    print(temp)
    print("Sum: ",sumFX,", Average: ",avgFX ,", Maximum: ",maxFX)
    return

##  Order-1 Crossover
def crossover():
    for ch in range(int(len(population)/2)):
        parent=random.sample(population,2)
        
        for i in range(2):      ## for child1 and child2
            point=random.sample(range(0,len(population[ch])),2)
            if point[0] > point[1]:
                temp,point[0]=point[0],point[1]
                point[1]=temp
            partition=parent[i][point[0]:point[1]+1]
            if i==0:
                otherParent=1
            else:
                otherParent=0
            child=[]
            for j in range(len(parent[otherParent])):
                if len(child)==point[0]:
                    child+=partition
                if parent[otherParent][j] not in partition:
                    child+=[parent[otherParent][j]]
            if len(child)!=len(parent[i]):
                child+=partition
            if len(child)!=len(parent[i]):
                raise('Error in crossover')
            newPopulation.append(child)
    return

def mutation():
    totalMutation=int(len(population)*0.2)
    selectedChromosome=random.sample(population,totalMutation)
    tempPopulation=[]
    for i in range(0,totalMutation):
        point=random.sample(range(len(selectedChromosome[i])),2)
        ##  swap between generated two points
        temp=selectedChromosome[i][point[0]]
        selectedChromosome[i][point[0]]=selectedChromosome[i][point[1]]
        selectedChromosome[i][point[1]]=temp
        tempPopulation.append(selectedChromosome[i])
    for i,chromosome in enumerate(population):
        match=0
        for j,ch in enumerate(selectedChromosome):
            if chromosome == selectedChromosome[j]:
                match=1
                break;
        if match==1:            
            newPopulation.append(tempPopulation[j])
            match=0
        else:
            newPopulation.append(chromosome)
    return
#starting of program
print("Hi")
city=[]
distance=[]
takeInput()
drawGraph(createGraph(city,'complete'))     # 'complete' To draw a complete graph

population=[]
generatePopulation()
print("Total no. of chromosomes generated in the population: %i"%len(population))

xVal,fitness,prob,expCount=[],[],[],[]
calculateFitness()
calculateProbCount()
print("Initial... ")
printResult()

for gen in range(1,10):
    print("==== GENERATION ",gen,"====")

##  Selection
    newPopulation=[]
    rouletteWheel()
    population=newPopulation
    
    xVal,fitness,prob,expCount=[],[],[],[]
    calculateFitness()
    calculateProbCount()
    print("After selection... : ")
    printResult()

##  Crossover
    newPopulation=[]
    crossover()
    population=newPopulation
    
    xVal,fitness,prob,expCount=[],[],[],[]
    calculateFitness()
    calculateProbCount()
    print("Crossover... ")
    printResult()

##  Mutation    
    newPopulation=[]
    mutation()
    population=newPopulation
    
    xVal,fitness,prob,expCount=[],[],[],[]
    calculateFitness()
    calculateProbCount()
    print("Mutation... ")
    printResult()

print("Resultant chromosome : ",population[fitness.index(maxFX)])
for cityIndex in population[fitness.index(maxFX)]:
    print("->",city[cityIndex],end=" ")
print("->",city[population[fitness.index(maxFX)][0]])
drawGraph(createGraph(city,'complete'))     # 'complete' To draw a complete graph
