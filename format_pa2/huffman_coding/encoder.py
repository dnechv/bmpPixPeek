#imports 
try:
    from format_pa2.huffman_coding import frequency_counter, tree_builder
except ModuleNotFoundError: 
    import frequency_counter, tree_builder

#econding logic 

#takes bytes and their huffman codes - creates bitstring
def encode_to_bits(data: bytes, h_codes: dict[int, str]) -> str:
    data_bits: list[str]= []

    #loop through the data 
    for b in data: 
        #find byte in huffman code
        huffman_code_byte = h_codes[b]
        #add to the list
        data_bits.append(huffman_code_byte)
    
    #return all codes joined togethe r
    return "".join(data_bits)


#takes bitstring and converts it to bytes 
def convert_to_bytes(bitstring: str)-> tuple[bytes, int]:
   
    #calcualte required padding
    padding = (8 - len(bitstring)%8) %8

    #apply padding 
    bitstring += "0" * padding 

    #convert 8 bits into bytes 
    data_bytes = bytes(int(bitstring[i:i+8],2) for i in range(0, len(bitstring),8))

    #return bytes and padding 
    #padding is nedded for decoding to remove extra 0s that were not in the file 
    return data_bytes, padding 




#combines all functions and does compression
def compress_huffman(data:bytes) -> tuple[bytes, dict[int,int], int]:
    #build frequiency table
    frequency_table = frequency_counter.create_frequency(data)

    #build huffman tree 
    tree = tree_builder.build_tree(frequency_table)

    #build huffamn codes with the tree 
    huffman_codes = tree_builder.traverse_tree_build_coding(tree)

    #create bit string 
    bitstring= encode_to_bits(data, huffman_codes)

    #convert to bytes
    bytes_huffman, padding = convert_to_bytes(bitstring)

    return bytes_huffman, frequency_table, padding



#TESTING

def test_encoder():
    data =b"AAAABBBSNCMNASDADASDSAD"
    compressed_data, frequency_table, padding = compress_huffman(data)
    print("original data:", data)
    print("frequency table:", frequency_table)
    print("compressed bytes:", compressed_data)
    print("padding:", padding)
    print("compressed size:", len(compressed_data), "bytes")


test_encoder()