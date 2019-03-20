'''
This file contains a Wrapper for Part I of the project.
NEEDED METHODS:
    -AC3/AC4: Arc Consistency
    -CSP Solution Handler
    (-Choose Variable)
    (-Choose Value)
'''

import graph_stuff as gr
from Arc_Consistency import AC3
from backtracking import backtracking
import sys

def Build_Constraint_Graph(inFile):
    '''
    This method accepts a textfile and returns a constraint graph for the CSP encoded in the file.
    BEWARE: There are two copies of each edge: one for each direction.
    Default edge weight is 1.
    @param inFile -> Text file containing CSP data
    '''
    Graph = gr.Graph([],[])
    inFile = inFile.split("\n")
    deadline = sys.maxsize
    sect, count = 0, 0
    values = {}
    variables = {}
    unaryInclusive = {}
    unaryExclusive = {}
    equals = {}
    notEquals = {}
    notSim = {}
    constraints = {}
    for idx,w in enumerate(inFile):
        if '#' in w:
            sect += 1
            continue
        elif sect==1:
            w = w.split()
            variables[w[0]]=count
            Graph.V.append(gr.Node(count,w[0]))
            Graph.V[len(Graph.V) - 1].time = w[1]
            count += 1
        elif sect==2:
            values[w.rstrip()] = idx-count-2
        elif sect==3:
            deadline = w.rstrip()
        elif sect==4: #unary inclusive
            w = w.split()
            numbered = []
            [numbered.append(values[x]) for x in w[1:]]
            unaryInclusive[variables[w[0]]]=numbered
        elif sect==5: 
            w = w.split()
            numbered = []
            [numbered.append(values[x]) for x in w[1:]]
            unaryExclusive[variables[w[0]]]=numbered
        elif sect==6:
            w = w.split(" ")
            edge1, edge2 = [0, 0, 0], [0, 0, 0]
            for nd in Graph.V:
                if nd.Name==w[0]: edge1[0], edge2[1] = nd, nd
                if nd.Name==w[1]: edge1[1], edge2[0] = nd, nd
            edge1[2], edge2[2] = 1, 1
            Graph.E.append(edge1)
            Graph.E.append(edge2)
            equals[variables[w[0]]]=variables[w[1]]
            equals[variables[w[1]]]=variables[w[0]]
        elif sect==7:
            w = w.split(" ")
            edge1, edge2 = [0, 0, 0], [0, 0, 0]
            for nd in Graph.V:
                if nd.Name==w[0]: edge1[0], edge2[1] = nd, nd
                if nd.Name==w[1]: edge1[1], edge2[0] = nd, nd
            edge1[2], edge2[2] = 1, 1
            Graph.E.append(edge1)
            Graph.E.append(edge2)
            if variables[w[0]] in notEquals.keys():
                notEquals[variables[w[0]]].append(variables[w[1]])
            else:
                notEquals[variables[w[0]]] = [variables[w[1]]]
            if variables[w[1]] in notEquals.keys():
                notEquals[variables[w[1]]].append(variables[w[0]])
            else:
                notEquals[variables[w[1]]] = [variables[w[0]]]
        elif sect==8:
            w = w.split(" ")
            edge1, edge2 = [0, 0, 0], [0, 0, 0]
            for nd in Graph.V:
                if nd.Name==w[0]: edge1[0], edge2[1] = nd, nd
                if nd.Name==w[1]: edge1[1], edge2[0] = nd, nd
            edge1[2], edge2[2] = 1, 1
            Graph.E.append(edge1)
            Graph.E.append(edge2)
            numbered = []
            [numbered.append(values[x]) for x in w[2:]]
            notSim[(variables[w[0]],variables[w[1]])]=numbered
            notSim[(variables[w[1]],variables[w[0]])]=numbered
    constraints['unaryInclusive']=unaryInclusive
    constraints['unaryExclusive']=unaryExclusive
    constraints['equals']=equals
    constraints['notEquals']=notEquals
    constraints['notSim']=notSim
    for vert1 in Graph.V:
        for vert2 in Graph.V:
            if [vert1, vert2, 1] in Graph.E:
                vert1.N.append(vert2)
                vert2.N.append(vert1)
    return Graph,values,variables,constraints,deadline

    
def buildConstraintMatrix(var1, var2, constraints, values):
    matrix=[]
    for i in range(len(values)):
        row=[]
        for j in range(len(values)):
            #NEXT LINE EDITED: Originally ...constraints['notEquals'].get(var1,"")==var2...
            if(i==j and var1 in constraints['notEquals'].keys() and var2 in constraints['notEquals'][var1]):
                row.append(False)
            elif(i!=j and (constraints['equals'].get(var1,False)) and (constraints['equals'][var1]==var2)):
                row.append(False)
            elif(((constraints['unaryExclusive'].get(var1,False)) and (i in constraints['unaryExclusive'][var1])) or 
            ((constraints['unaryExclusive'].get(var2,False)) and (j in constraints['unaryExclusive'][var2]))):
                row.append(False)
            elif(((constraints['unaryInclusive'].get(var2,False)) and (j not in constraints['unaryInclusive'][var2])) or
                ((constraints['unaryInclusive'].get(var1,False)) and (i not in constraints['unaryInclusive'][var1]))):
                row.append(False)
            elif((constraints['notSim'].get((var1,var2),False)) and (i in constraints['notSim'].get((var1,var2)) and 
                j in constraints['notSim'].get((var1,var2)))):
                row.append(False)
            else:
                row.append(True)
        matrix.append(row)
    return matrix

if __name__=="__main__":
    if(len(sys.argv)<2):
        print("run the code as follows:")
        print("python Wrapper.py <filename>")
        exit(0)
    fname = sys.argv[1]
    fid = open(fname, "r")
    data = fid.read()
    fid.close()
    Constraint_Graph,values,variables,constraints,deadline = Build_Constraint_Graph(data)
    print("Vertices:\n")
    print(values)
    print(variables)
    print(constraints)
    Constraint_Graph.valList=list(values.values())
    
    for w in Constraint_Graph.V: print(w.Name)
    print("Edges:\n")
    for w in Constraint_Graph.E: print(w[0].Name + " " + w[1].Name + " " + str(w[2]))
    constmat = buildConstraintMatrix(4,0,constraints,values)
    
    domains = []
    for i in range(len(variables)):
        t = []
        for j in range(len(values)):
            t.append(j)
        domains.append(t)
    
    Const_Dict = {}
    for i in range(len(variables)):
        for j in range(len(variables)):
            if(i==j): continue
            Const_Dict[(i, j)] = buildConstraintMatrix(i, j, constraints, values)

    #print(AC3(Constraint_Graph, domains, Const_Dict))
    
    #for row in Const_Dict[(5,9)]: print(row)
    #input()
    for i in range(len(variables)):
        if(constraints['unaryExclusive'].get(i,False)):

            for val in constraints['unaryExclusive'].get(i):
                if(val in domains[i]):
                    domains[i].remove(val)

        if(constraints['unaryInclusive'].get(i,False)):
            domains[i]=constraints['unaryInclusive'].get(i)
    #print(domains)
    
    
    print(backtracking(domains,Constraint_Graph,Const_Dict,deadline))
