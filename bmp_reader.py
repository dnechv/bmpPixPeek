#reads bmp image metadata 
#opens in binary mode, reads bytes, slices bytes array to extract data, converts data to integers and prints the data summary
#BMP uses little-endian: first byte is the lowest part of the number


#open bmp file
#bmp image: 0 to 255 bytes containing data 


filePath = "/Users/dnechv/Desktop/bmpPixPeek/input/BIOS.bmp"


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
imageDataOffsetBytes = bmp_bytes[10:14]


print(fileSizeBytes)
print(widthBytes)
print(heightBytes)
print(bitesPerPixelBytes)


#decode and printdata - file size, width, height, bits per pixel 

image_size = int.from_bytes(fileSizeBytes, 'little')
image_width = int.from_bytes(widthBytes, 'little')
image_height = int.from_bytes(heightBytes,'little')
image_bytes_per_pixel = int.from_bytes(bitesPerPixelBytes,'little')
image_offset_data = int.from_bytes(imageDataOffsetBytes, 'little')



print(image_size )
print(image_width)
print(image_height)
print(image_bytes_per_pixel)
print(image_offset_data)

print("File size: ", image_size, ", bytes width: ",image_width, ", bytes height: ",image_height, ", bytes per pixel: ", image_bytes_per_pixel )