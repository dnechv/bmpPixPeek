#creates a custom 365 file 
try:
    from format_pa2.cmpt_365_header import create_header
    from format_pa2.huffman_coding import encoder
except ModuleNotFoundError: 
    from cmpt_365_header import create_header
    import encoder


#python3 -m format_pa2.huffman_coding.file_writer_cmpt365



import struct


#adds frequency table to the file 
def add_frequency_table(file, frequency_table: dict[int,int]) -> None:

    #count of frequncy entires
    #pack the data as 4-byte unsigned integer- little edian 
    file.write(struct.pack("<I", len(frequency_table)))

    #write each symbol and its frequency
    #< BI = little edian, unsigned char + unsigned int 
    for symbol, freqency in frequency_table.items():
        file.write(struct.pack("<BI", symbol, freqency ))

#file creator

def create_cmpt_365_file (filename: str, compressed_data: bytes, frequency_table : dict[int, int],padding: int, header_data:dict ):
    
    #create header info
    header_info = create_header(
    header_data["algorithm_id"],
    header_data["width"],
    header_data["height"],
    header_data["bpp"],
    header_data["original_bmp_size"],
    len(compressed_data),
)
    
    #open file and write data to it 
    with open(filename, "wb") as file: 
        file.write(header_info)
        add_frequency_table(file, frequency_table)
        file.write(struct.pack("<B", padding))
        file.write(compressed_data)


#TESTING

def test_file_writer():
    data = b"AASASDASDASFASFDASDSASDASDSADSSAD"
    commpressed_data, frequency_table, padding = encoder.compress_huffman(data)
    header_data = {"algorithm_id": 1,
                   "width": 0,
                   "height": 100,
                   "bpp": 0,
                   "original_bmp_size": len(data),
                   }
    create_cmpt_365_file("testing_file_creation", commpressed_data, frequency_table, padding, header_data)
    print("testing cmpt365 file creation")
    
#test_file_writer()