from heuristics import getUnassignedVariable
from Arc_Consistency import AC3
from heuristics import lcv
from heuristics import order_domain_values

def isComplete(domain):
    for row in domain:
        if(len(row)>1):
            return False
    return True


def backtracking(domain, graph, const, deadline):
    if isComplete(domain): return domain
    unassigned = getUnassignedVariable(domain,graph)
    vals = order_domain_values(unassigned,domain[unassigned],const)
    print(vals)
    input()
    for val in vals:
        temp = domain[unassigned].copy()
        #temp.remove(val)
        domain[unassigned] = [val]
        if AC3(graph, domain, const, deadline):
            return backtracking(domain, graph, const, deadline)
        domain[unassigned] = temp
        #return backtracking(domain, graph, const, deadline)
 #   for val in domain:
#        if AC3(graph, domain,const):

#            val
 #           domain[unassigned]=[lcv(val,domain,const)]


#            result = backtracking(domain,graph,const)
#            if result:
#                return True

#        domain[unassigned]=[0,1,2,3,4,5]
    return False
