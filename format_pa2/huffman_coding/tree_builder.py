#this file contains the logic of building a huffman tree 

#https://docs.python.org/3/library/heapq.html

import heapq


#node data class defenition - single element 
class Node:
    def __init__(self, frequency, symbol= None, left=None, right = None):
        self.frequency = frequency
        self.symbol = symbol
        self.left_child = left
        self.right_child = right
     
    #override less than method to compare frequency of two nodes 
    def __lt__(self, other_node):
        return self.frequency < other_node.frequency
    
    #override repr method so node decrypts itself when printing
    def __repr__(self):
        return f"Node (freq = {self.frequency},id = {self.symbol})"


#huffman tree building method 
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

#function for traversing the tree and building coding table 
#starts from the root node 
def traverse_tree_build_coding(root: Node)->dict[int,str]:

    #dictionary to store codes
    codes: dict[int, str] = {}

    #edge case - only one symbol - assing zero 
    if root.symbol is not None and root.left_child is None and root.right_child is None:
        codes[root.symbol] = "0"
        return codes
    
    #to-do visit nodes - starts with the root 
    #contains root and huffamn code through the path - left zero and right 1 
    nodes_queue = [(root, "")]

    #loop through the nodes 
    while nodes_queue: 

        #pop the node - takes the node and its encoded string 
        node, huffman_code = nodes_queue.pop()

        #check for a leaf node - store its encoding 
        if node.symbol is not None: 
            codes[node.symbol]= huffman_code

        #check for left child. if exists, go left and add 0 to encoding
        if node.left_child is not None: 
            nodes_queue.append((node.left_child, huffman_code + "0"))

        #check for the right child. if exists, go right and add 1 to encoding
        if node.right_child is not None:
            nodes_queue.append((node.right_child, huffman_code + "1"))

    return codes 


#TESTING

def test_tree_creation():

    sample_frequency = {
        65: 10,
        77: 20,
        33: 20,
        40: 11,
        20: 1,
    }

    sample_tree = build_tree(sample_frequency)

    #root = 10 + 20 + 20 + 11 + 1
    print("sample tree root: ", sample_tree.frequency)
    print("left child: " , sample_tree.left_child)
    print("right_child: ", sample_tree.right_child)

    #generate huffman codes
    print("Huffamn Codes", traverse_tree_build_coding(sample_tree))


test_tree_creation()






