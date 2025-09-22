#reads bmp image metadata 
#opens in binary mode, reads bytes, slices bytes array to extract data, converts data to integers and prints the data summary
#BMP uses little-endian: first byte is the lowest part of the number


#open bmp file
#bmp image: 0 to 255 bytes containing data 
def read_bmp(file_path):

    filePath = file_path


    file = open(filePath, "rb") #rd read in binary

    bmp_bytes = file.read()

    file.close()

    #decimal offset - position of bytes in the bits array 
    print(int("0x002",16)) #filezie - 2 - size 4 bytes 
    print(int("0x012",16)) #width - 18 - size 4 bytes
    print(int("0x016",16)) #height - 22 - size 4 bytes 
    print(int("0x01C",16)) #bits per pixel - 28 - size 2 bytes 
    print(int("0x0A",16)) #data offset - where the image data starts - 10 - size 4 bytes 

    #each has position 4 bytes 

    #print(bmp_bytes)

    #extract data - file size, width, height, bits per pixel 

    fileSizeBytes = bmp_bytes[2:6]
    widthBytes = bmp_bytes[18:22]
    heightBytes = bmp_bytes[22:26]
    bitesPerPixelBytes = bmp_bytes[28:30]
    imageDataOffsetBytes = bmp_bytes[10:14] #where pixel data image starts 


    print(fileSizeBytes)
    print(widthBytes)
    print(heightBytes)
    print(bitesPerPixelBytes)



    #decode and printdata - file size, width, height, bits per pixel 

    image_size = int.from_bytes(fileSizeBytes, 'little')
    image_width = int.from_bytes(widthBytes, 'little')
    image_height = int.from_bytes(heightBytes,'little')
    image_bytes_per_pixel = int.from_bytes(bitesPerPixelBytes,'little')
    image_offset_data = int.from_bytes(imageDataOffsetBytes, 'little') #where pixel data image starts 



    print(image_size )
    print(image_width)
    print(image_height)
    print(image_bytes_per_pixel)
    print(image_offset_data)


    print("File size: ", image_size, ", bytes width: ",image_width, ", bytes height: ",image_height, ", bytes per pixel: ", image_bytes_per_pixel )



    #TODO use pixel_offset, width, height to read one full pixel row and check the first RGB values.


    #slicing pixel array to get pixel image data

    pixel_image_data = bmp_bytes [image_offset_data: ]


    #number of bytes of pixel color data in one row - RGB - Unpadded 
    color_bytes_per_row = image_width * 3

    print(color_bytes_per_row)

    #calculate total color data + padding = amount of rows blocks containing image data 
    row_stride = ((color_bytes_per_row +3)//4) * 4

    print(row_stride)


    #reading image data - extract all pixels and store them 

    #starting point for pixel data 
    pointer = image_offset_data


    #TEST - one full block to confirm correct sizing of each row block 
    one_full_row_block = bmp_bytes[pointer: pointer + row_stride]

    print(len(one_full_row_block))


    #container for decoded pixels - each decoded row will be added here 
    row_pixels_container = []


    #loop through all rows 

    for i in range(image_height):

        row_block = bmp_bytes[pointer: pointer + row_stride] #extract one block from the row 
        pointer += row_stride #move pointer to the next block 

        #to hold row pixel data
        row_pixel_data = []
        
        #loop though the pixels in one block
        #BGR 

        for x in range (image_width):

            #set the starting pixel

            start = x*3 
            B = row_block[start]
            G = row_block[start + 1]
            R = row_block[start + 2]
            row_pixel_data.append((R,G,B)) #save pixel data as RGB 


        #save the completed row 
        row_pixels_container.append(row_pixel_data)


    #reverse the pixels order so it is stored top to bottom 
    pixels_rgb = row_pixels_container [::-1]

    return pixels_rgb


        
        













