#this file defines a header for cmpt 365 format 
#https://docs.python.org/3/library/struct.html

import os
import random
import io

#struct library python - bytes as packaged data 
import struct 


# ID for cmpt 365 format: lenght - 8 bytes 
FILE_SIGNATURE = b"CMPT365\0"


#binary layout for the header - defines bytes organization that contains information
HEADER_FORMAT = "<8sBIIBII"


# < - little edian order (LSB First)
# 8s - 8 byte string for FILE_SIGNATURE CMPT365\0
# B - unsigned char - 1 byte - range 2^8
# I - unsigned int- 4 bytes for image width - range 2^32
# I - unsigned int - 4 bytes for image height - range 2^32
# B - unsigned bytes for bits per pixel - range 2^8
# I - 4 byte integer for original BMP size  - range 2^32
# I - 4 byte integer for compressed BMP file - range 2^32
# total size = 26 bytes


#calcualte the header size - allows to read the header easily when packed or unpacked 
HEADER_SIZE_STRUCT = struct.calcsize("<8sBIIBII")

#testing - confrm total size 
#print("Size of header struct:", HEADER_SIZE_STRUCT)



#function that creates and returns header for cmpt365 format 
#takes regular inputs values defining the header and packs them as bits 
def create_header(algorithm_id, width, height,bpp, original_bmp_size, compressed_bmp_size):


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
#reads normal objects and returns bytes 
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

##TESTING

def test_bytes_packing_header():

    algorithm_id = random.randint(0,5)
    width = random.randint(0,5)
    height = random.randint(0,5)
    bpp = random.randint(0,5)
    original_bmp_size = random.randint(0,5)
    compressed_bmp_file =random.randint(0,5)

    #print("Testing create_header function:",create_header(algorithm_id, width, height, bpp,original_bmp_size, compressed_bmp_file))
    


def test_read_header():
    algorithm_id = 100
    width = 77
    height = 11
    bpp = 11
    original_bmp_size = 200
    compressed_bmp_file =1

    header = create_header(algorithm_id, width, height, bpp, original_bmp_size, compressed_bmp_file)

    file = io.BytesIO(header)

    #print("Testing reading header:", read_header(file))











