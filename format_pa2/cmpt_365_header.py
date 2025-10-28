#this file defines a header for cmpt 365 format 
#https://docs.python.org/3/library/struct.html


#struct library python - bytes as packaged data 
import struct 

# ID for cmpt 365 format: lenght - 8 bytes 
FILE_SIGNATURE = b"CMPT365\0"


#binary layout for the header - defines bytes organization that contains information
HEADER_FORMAT = "<8sBIIBII"

# < little edian order (LSB First)
# 8s - 8 byte string for FILE_SIGNATURE CMPT365\0
# B: unsigned byte number for algorithm ID
# I: int- 4 bytes for image width
# I: int - 4 bytes for image height
# B: unsigned bytes for bits per pixel 
# I: 4 byte integer for original BMP size 
# I: 4 byte integer for compressed BMP file 


#calcualte the header size - allows to read the header easily when packed or unpacked 
HEADER_SIZE_STRUCT = struct.calcsize("<8sBIIBII")

#function that creates and returns header for cmpt365 format 
def create_header(algorithm_id,width, height,bpp, original_bmp_size, compressed_bmp_size):


    #converts python values in a byte object with binary data 
    header_data = struct.pack(
        HEADER_FORMAT,
        FILE_SIGNATURE,
        algorithm_id,
        width,
        height,
        bpp, 
        original_bmp_size,
        compressed_bmp_size,
    )

    #return packaged bytes-can added to file later
    return header_data 

#function for reading header data

def read_header(file):

    #read all header bytes so they can be unpacked 
    header_data = file.read(HEADER_SIZE_STRUCT) 


    #check for correct header lenght 
    if len(header_data) != HEADER_SIZE_STRUCT:
        raise ValueError("Invalid cmpt365 format. Incomplete or broken header")


    #unpack binary data values using tuple - accessed via indexing
    header_data_unpacked = struct.unpack(HEADER_FORMAT, header_data)


    #check for file signature to confirm cmpt365 format
    if header_data_unpacked[0] !=FILE_SIGNATURE:
        raise ValueError("NOT CMPT 365 FORMAT!")
    
    #convert header data into python data - using indexing
    header_info = { 
        "algorithm_id": header_data_unpacked[1],
        "width": header_data_unpacked[2],
        "height": header_data_unpacked[3],
        "bpp": header_data_unpacked[4],
        "original_bmp_size": header_data_unpacked[5],
        "compressed_bmp_file": header_data_unpacked[6],

    }


    return header_info

#TESTING
def test():
     #create header test 
    header_bytes = create_header(0, 512, 512, 24, 300000, 100000)
    print("binary header bytes:", header_bytes)

    #read header test
    header_unpacked = struct.unpack(HEADER_FORMAT, header_bytes)
    print("binary header bytes unpacked:", header_unpacked)   

test()



