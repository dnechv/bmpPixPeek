#this file contains the logic of building a huffman tree 

#https://docs.python.org/3/library/heapq.html

import heapq


#node data class defenition - single element 
class Node:
    def __init__(self, frequency, symbol= None, left=None, right = None):
        self.frequency = frequency
        self.symbol = symbol
        self.left = left
        self.right = right
     
    #override less than method to compare frequency of two nodes 
    def __lt__(self, other_node):
        return self.frequency < other_node.frequency


#this method builds a huffman tree 
def build_tree(data: dict[int,int]) -> Node: 

    #list to contain nodes 
    heap = []

    #go through all data and add their frequency and symbol to node 
    for symbol, frequency in data.items():
        node = Node(frequency, symbol)
        heap.append(node)

    #create min heap -smallest element on top
    heapq.heapify(heap)


    #edge case: only one data

    if len(heap) ==1 : 
        #remove node 
        single_node = heapq.heappop(heap)
        #make it parent node 
        return Node(frequency = single_node.frequency, left = single_node, right = None)
    
    #building tree logic 
    while len(heap)>1: 
        #take two smallest nodes
        left_node = heapq.heappop(heap)
        right_node = heapq.heappop(heap)

        #merge two nodes in a single node - create a new parent 
        #sum frequency of its children
        new_parent = Node(frequency=left_node.frequency + right_node.frequency, left= left_node, right = right_node )

        #push merged node back in heap
        heapq.heappush(heap, new_parent)

    #return the root - containig all merged nodes 
    return heap[0]


def traverse_tree_build_coding(root: Node)->dict[int,str]:

