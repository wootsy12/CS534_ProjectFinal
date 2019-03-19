'''
This file contains the classes:
   Node -> The class for a graph node object
   Graph -> The class for an object consisting of vertices, edges, and edge weights
   Graph_gen -> The class for an object that reads formatted text files and produces graph objects
'''

class Node:

    def __init__(self, val, name):
        self.value = val
        self.Name = name
        self.N = []
        self.label = False
        self.time = 0

    def exp(self):
        '''
        Expand this node
        '''
        nbor_names = [it.Name for it in self.N]
        nbor_names.sort(reverse=True)
        ret_list = []
        for w in nbor_names:
            for nbor in self.N:
                if nbor.Name==w:
                    ret_list.append(nbor)
        return ret_list

class Graph:

    def __init__(self, nodes, Edges):
        '''
        Edges takes the following form:
           [[node1,    node2,  weight],    ... ]
        '''
        self.V = nodes
        self.E = Edges
        self.valList = []

class Stack:

    def __init__(self):
        self.cont = []

    def push(self, this):
        self.cont.insert(0, this)

    def pop(self):
        if len(self.cont) > 0: return self.cont.pop(0)
        else:
            print("Stack is Empty!")
            return -1

    def sizeOf(self):
        return len(self.cont)

    def isEmpty(self):
        return len(self.cont)==0

class Queue:

    def __init__(self):
        self.cont = []

    def push(self, it):
        self.cont.insert(0,it)

    def dequeue(self):
        return self.cont.pop()

    def isEmpty(self):
        return (self.cont==[])

    def sizeOf(self):
        return len(self.cont)

    def dequeue_from_back(self):
        return self.cont.pop(0)

    def push_right(self, it):
        self.cont.append(it)

    def delete(self, it):
        if it in self.cont:
            self.cont.remove(it)
            return
        print("Error: item "+str(it)+" not found")
        return -1
