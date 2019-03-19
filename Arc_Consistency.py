'''
This file contains arc-consistency (constraint propagation) code.
'''
import graph_stuff as gr

def AC3(Graph, Dom, const,deadline):
    '''
    This AC3 method accepts a constraint graph, allong with binary constraints,
    encoded in constraint matrices. This method returns False if an inconsistency
    is found with binary constraints. It returns True otherwise.
    @param Graph -> Constraint graph
    @param Dom -> List of domains
    @param const -> Dictionary of binary constraint matrices
    '''
    queue = gr.Queue()
    for edge in Graph.E: queue.push(edge[0:2])
    while not queue.isEmpty():
        print("Current Queue Size: ", len(queue.cont))
        print("Current Domain Values: ")
        for w in Dom: print(w)
        #input()
        edge = queue.dequeue()
        n1, n2 = edge[0], edge[1]
        #print(n1.value, n2.value)

        Dom1, Dom2 = Dom[n1.value], Dom[n2.value]
        #print(Dom1, Dom2)
        if len(Dom1) == 0 or len(Dom2) == 0: return False
        if Revise(Dom1, Dom2, const[(n1.value, n2.value)],Graph):
            if len(Dom1) == 0: return False
            for nbor in n1.N:
                if nbor.value != n2.value:
                    queue.push([n1, nbor])
                    queue.push([nbor, n1])
    deadlines = {}
    for node in Graph.V:
        if(len(Dom[node.value])==1):
            for d in Dom[node.value]:
                deadlines[d]=deadlines.get(d,0)+int(node.time)
    if(max(deadlines.values())>int(deadline)):
        return False

    return True

def Revise(Dom1, Dom2, const_mat,graph):
    '''
    This method returns true if the domain of variable n1 must be revised
    in order to meet constraints with variable n2.
    @param Dom1 -> Domain of variable n1
    @param Dom2 -> Domain of variable n2
    @param const_mat -> Binary constraint matrix for n1 and n2
    '''
    revised = False
    for val1 in Dom1:
        exists = False
        ls = []
        for val2 in Dom2:
            if const_mat[val1][val2]: exists = True
        if not exists:
            Dom1.remove(val1)
            revised = True
    return revised
