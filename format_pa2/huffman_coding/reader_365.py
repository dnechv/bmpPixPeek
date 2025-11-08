#contains the logic of reading the 365 file format
import struct

#python3 -m format_pa2.huffman_coding.365_reader

try:
    from format_pa2.cmpt_365_header import read_header
    from format_pa2.huffman_coding import tree_builder
except ModuleNotFoundError:
    from cmpt_365_header import read_header
    import tree_builder

#reads frequency table of the file - rebuilds huffman tree 
def read_freq_table(file) -> dict[int, int]: 
    #count frequency
    #reads 4 bytes from the file (little-edian, unsigned 4 byte integer)
    count = struct.unpack("<I", file.read(4))[0]


    reconstructed_frequency_table: dict[int, int] = {}

    #read entry: (1 byte = symbol, 4 byte frequency)

    for i in range(count):

        #read data 
        symbol, frequency = struct.unpack("<BI", file.read(5))
        
        #put data in new table 
        reconstructed_frequency_table [symbol] = frequency

    return reconstructed_frequency_table

#file reader function

def read_cmpt365(path: str)-> tuple[dict, dict[int, int], int, bytes]:
    with open(path, "rb") as file:

        #read header info
        header_data = read_header(file)

        #read frequency table 
        frequency_table = read_freq_table(file)

        #read padding 
        padding = struct.unpack("<B", file.read(1))[0]

        #read compressed data 
        compressed_data = file.read()

        return header_data, frequency_table, padding, compressed_data
    
#decompressing logic 
def decompress_huffman(compressed_data: bytes, frequency_table: dict[int, int], padding: int)-> bytes:
    
    #build the huffman tree from frequency table
    tree = tree_builder.build_tree(frequency_table)

    #create a bitstring from compressed bytes
    bitstring = "".join(f"{b:08b}" for b in compressed_data)

    #remove padding zeros 
    if padding>0: 
        bitstring = bitstring[:len(bitstring) - padding]

    #tree traversal logic

    result = bytearray()
    node = tree

    for bit in bitstring:
        
        #go left
        if bit =="0":
            node = node.left_child
        
        #go right 
        else: 
            node = node.right_child

        #if leaf 
        if node.symbol is not None:
            result.append(node.symbol)
            node = tree

    return bytes(result)


#TESTING

def test_huffman_reader():
    header, freq, pad, comp = read_cmpt365("testing_file_creation")
    decoded = decompress_huffman(comp, freq, pad)
    print(decoded)


test_huffman_reader()