from heuristics import getUnassignedVariable
from Arc_Consistency import AC3
from heuristics import lcv
from heuristics import order_domain_values
import copy

def isComplete(domain):
    for row in domain:
        if(len(row)>1):
            return False
    return True


def backtracking(domain, graph, const, deadline):
    if isComplete(domain): return domain
    unassigned = getUnassignedVariable(domain,graph)
    
    vals = order_domain_values(unassigned,domain[unassigned],const)
    temp = copy.deepcopy(domain)
    for val in vals:
      
        domain[unassigned] = [val]
        if AC3(graph, domain, const, deadline):
            return backtracking(domain, graph, const, deadline)

        domain = temp

    return False
