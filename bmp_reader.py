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


    #saves images bits per pixel 
    bpp = image_bytes_per_pixel  

    # calculate row stride 
    row_stride = ((bpp * image_width + 31) // 32) * 4  

    #degub row stride
    print(row_stride)
    
    #BMP 24bpp stores BGR values directly
    #BMP with 1,4,8 bpp stores index used in pallete to locate RGB color 
    #palette/colortable - BMP image part stores a lost of RGB Colors 
    #read palete if index is 1, 4, 8 bpp
    #each entry = BGRA - 4 bytes - blue, green, red, reserved 

    colorTable = []

    if bpp in (1,4,8):
        
        #read dib header 0x0E (14)-> color table starts after 
        dib_header_size = int.from_bytes(bmp_bytes[14:18], 'little')
        
        #calcuate the end of the DIB header 
        dib_end = 14 + dib_header_size 

        #slice the color table bytes
        colorTable_bytes = bmp_bytes[dib_end:image_offset_data]

        #calculate number of expect entires in the color table 
        expected_entries = 2 ** bpp

        #calculate the amount of entries in the color table 
        entires = len(colorTable_bytes) // 4

        #BMP files can have fewer colors than expected 
        color_entires = min(entires, expected_entries)

        #go through color enties and extract them 
        for i in range(color_entires):
            B = colorTable_bytes[4*i]
            G = colorTable_bytes[4*i +1]
            R = colorTable_bytes[4*i +2]
            colorTable.append((R,G,B))










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


        #must be decoded based on bits per pixel


        #decoding loop 
        for x in range (image_width):

            #decoding the image based on bpp


            if bpp ==24:

                start = x*3 
                B = row_block[start]
                G = row_block[start + 1]
                R = row_block[start + 2]
                row_pixel_data.append((R,G,B)) #save pixel data as RGB 

            elif bpp == 8:
                #1 byte per pixel - index in colortable

                #get colortable index from row data
                index = row_block[x]

                #match index with colortable 
                color = colorTable[index]

                #add RGB color to row's pixel list
                row_pixel_data.append(color)

            elif bpp == 4:
                #2 pixels per byte 

                #calculate byte position for current pixel
                byte_position = x //2 

                #read byte's value from row data 

                byte_value = row_block[byte_position]

                #check if the pixel is first (even) or second (odd) inside the byte

                if x %2 ==0:

                    #take first high bits 
                    index = byte_value >> 4 
                
                else: 

                    #take 4 low bits
                    index = byte_value & 0x0F


                #record color 
                color = colorTable[index]

                #add to pixel data 
                row_pixel_data.append(color)


            elif bpp ==1:
                #8 pixels per byte

                #calculate yte holding the pixel 
                byte_position = x//8

                #read the byte value 
                byte_value = row_block[byte_position]

                #calculate which bit to use inside 
                bit_position = 7 - (x%8)

                #extract the single bit at the given position from the byte 
                index = (byte_value >> bit_position) & 1

                #find RGB color from Colortable 
                color = colorTable[index]

                #add to row's pixel data
                row_pixel_data.append(color)



        #save the completed row 
        row_pixels_container.append(row_pixel_data)


    #reverse the pixels order so it is stored top to bottom 
    pixels_rgb = row_pixels_container [::-1]


    #store metadata in a container 

    image_metadata = {
        "file_size": image_size,
        "width" : image_width,
        "height" : image_height,
        "bits_per_pixel" : bpp,
    }

    return pixels_rgb,image_metadata 


        
        













