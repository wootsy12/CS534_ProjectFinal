'''
This file contains code for variable and value heuristics.
mrv(Dom) returns a list of variables that are tied for the minimum remaining values.
deg(Dom, ls, Graph) is meant to break ties; of the variables included in ls (indicated by integer value,
    i.e., j for X_j), deg returns the one that has the most constraints with currently unassigned variables.
'''

def getUnassignedVariable(Dom,graph):
    minrem = mrv(Dom)
    tiebreaker = deg(Dom,minrem,graph)
    return tiebreaker

def mrv(Dom):
    '''
    Returns a list of variables that are tied for having the least remaining possible values in their domains
    '''
    rem_values = []
    for w in Dom:
        if len(w) > 1:
            rem_values.append(len(w))
    ls = []
    for ind in range(len(Dom)):
        if len(Dom[ind]) == min(rem_values): ls.append(ind)
    return ls

def deg(Dom, ls, Graph):
    '''
    Returns the variable with the lowest degree heuristic of the variable list, ls
    '''
    Graph.V = sorted(Graph.V, key=lambda w:len(w.N), reverse=True)
    for vert in Graph.V:
        if vert.value in ls and (len(Dom[vert.value]) > 0): return vert.value
    return -1

def lcv(var, dom, Const_Dict):
    vect = []
    for val in dom:
        count = 0
        for key in Const_Dict.keys():
            if key[0] == var:
                for ind in range(len(Const_Dict[key][0])):
                    if not Const_Dict[key][val][ind]: count += 1
        vect.append(count)
    for ind in range(len(dom)):
        if vect[ind] == min(vect): return dom[ind]
    return -1

def order_domain_values(var, dom, Const_Dict):
    ls = []
    dom2 = dom.copy()
    while len(dom2) > 0:
        val = lcv(var, dom2, Const_Dict)
        ls.append(val)
        dom2.remove(val)
    return ls
