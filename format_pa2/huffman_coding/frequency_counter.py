#huffman coding uses frequency count of bytes to assing coding for each symbol
#this file contains frequency counter that will proceess raw data and count occurance of each bytes 


#https://docs.python.org/3/library/collections.html#collections.Counter


import os 



from collections import Counter 

#takes bytes input and returns number of times each byte occurs 
def create_frequency(data: bytes) -> dict[int,int]:

    #(key:count)
    return dict(Counter(data))



##test

def test_frequency_counter():
    
    data = os.urandom(10)
    print("testing frequency counter", data)


#test_frequency_counter()







