import tkinter as tk

import tkinter.filedialog
import base64


import os 


#PA2 imports 
import time 
from format_pa2.huffman_coding import encoder
from format_pa2.huffman_coding import file_writer_cmpt365
from format_pa2.huffman_coding import reader_365


from tkinter import messagebox



from bmp_reader import read_bmp

#holds decoded BMP pixels 
original_pixels_rgb = None 


def compress_to_365():
    #get file path from entry
    file_path = file_path_entry.get()

    #if no file path, open file dialog
    if not file_path:
        file_path = tk.filedialog.askopenfilename(
            title="Open BMP File",
            filetypes=[("BMP Files", "*.bmp"), ("All Files", "*.*")],
        )
        #if user cancels file dialog
        if not file_path:
            return

    #update the textbox with selected file path
    file_path_entry.delete(0, tk.END)
    file_path_entry.insert(0, file_path)

    if not file_path:
        messagebox.showerror("Error", "Open BMP File")
        return 
    
    #read the bmp bytes
    with open(file_path, "rb") as file: 
        bmp_bytes = file.read() 


    #read metadata from the bmp - matrix ignored
    _, metadata = read_bmp(file_path)

    #compress and record time 
    start_time = time.time()
    compressed_bytes, frequency_table, padding = encoder.compress_huffman(bmp_bytes)
    end_time = time.time()


    #metadata of the compressed image for the header 
    header__metadata = {
        "algorithm_id": 1,
        "width": metadata["width"],
        "height": metadata["height"],
        "bpp": metadata["bits_per_pixel"],
        "original_bmp_size": len(bmp_bytes),
    }


    #create .cmpt365 file 
    file_name = file_path + ".cmpt365"
    file_writer_cmpt365.create_cmpt_365_file(
        file_name,
        compressed_bytes,
        frequency_table,
        padding, 
        header__metadata,
    )


    #display the stats after compression 
    messagebox.showinfo(
        "Compressed to .cmpt365 file",
        f"File Created :{file_name}\n"
        f"Original File Size: {len(bmp_bytes)} bytes\n"
        f"Compressed Size: {len(compressed_bytes)}\n"
        f"Compression Ratio: {len(bmp_bytes)/len(compressed_bytes):.2f}\n"
        f"Time to compress: {(end_time - start_time)*1000:.2f} ms"

    
    )




   

#decompressing 365 format
def decompress_365():

    #get .365 file path from entry 
    file_path = file_path_entry.get().strip()

    if not file_path: 
        file_path = tk.filedialog.askopenfilename(
            title="Open .cmpt365 File",
            filetypes=[("CMPT365 Files", "*.cmpt365"), ("All Files", "*.*")],
        )
        #if user cancels file dialog
        if not file_path:
            return
        
        #update the textbox with filepath
        file_path_entry.delete(0, tk.END)
        file_path_entry.insert(0, file_path)
        


    #check for .365 FILE 
    if not file_path:
        messagebox.showerror("Error", "Open .365 File")
        return
    
    #read .365 bytes - get header, freq table + data 
    header_data, frequency_table, padding, compressed_data = reader_365.read_cmpt365(file_path)

    #get decompressed 365 bytes
    decompressed_bytes = reader_365.decompress_huffman(compressed_data, frequency_table, padding)

    #building decompressed file with bytes 
    file_name = file_path +".bmp"

    #write decompressed image data to bmp
    with open(file_name, "wb") as file: 
        file.write(decompressed_bytes)
    
    file_path_entry.delete(0, tk.END)
    file_path_entry.insert(0, file_name)
    open_bmp_image()

     
    messagebox.showinfo(
        "Decompression Complete",
        f"File Created :{file_name}\n"
    
    )







#file validation function
def validate_file(bmp_bytes):
    #bmp file has header 14 bytes that contains signature 2 bytes

    #checks and returns boolea for file signature 
    return bmp_bytes[:2] == b'BM'


#READER UI LOGIC 

#opens BMP image 
def open_bmp_image():

    #set python to use original variable defined on top 
    global original_pixels_rgb

    #get the file path
    file_path = file_path_entry.get()

    #open bytes of the image
    with open(file_path, "rb") as file:

        #read the image bytes
        bmp_bytes = file.read()

        #validating the bmp bytes

    if not validate_file(bmp_bytes):
        messagebox.showerror("Text", "Not a BMP File.Please try another file")
        return

    #get pixels 
    pixels_rgb, metadata = read_bmp(file_path)
    

    #save decoded pixels from BMP in the global variable - image data exits between two functions 
    original_pixels_rgb = pixels_rgb

    #call redraw the image - changes color of the image inside its code
    redraw_the_image()


    #update metadata labels

    file_size_label.config(text=f"File size: {metadata['file_size']} bytes")
    width_label.config(text=f"Width: {metadata['width']} px")
    height_label.config(text=f"Height: {metadata['height']} px")
    bpp_label.config(text=f"Bits per pixel: {metadata['bits_per_pixel']}")


def redraw_the_image(*_):
    #check for the image loaded
    if original_pixels_rgb is None:
        return 
    
    #read the scaling value from the UI slider
    scale = size_scale.get() / 100.0


    #to turn off RGB. multiply the channel by 0

    red_channel_multiplier = 1 if red_toggle.get() else 0
    green_channel_multiplier = 1 if green_toggle.get() else 0
    blue_channel_multiplier = 1 if blue_toggle.get() else 0

    #extract each pixel 
    #pixel = pixels[y][x]
    height = len(original_pixels_rgb) #row y 
    width = len(original_pixels_rgb[0]) #column x

    #computing scaled dimensions 

    #calculate new width and height 
    
    #set 0 slider to 1 - SAFETY
    if scale == 0.0: #
        new_width, new_height = 1, 1

    else:
        new_width  = max(1, int(width  * scale))
        new_height = max(1, int(height * scale))
    
    #matrix to hold scaled image pixels 
    scaled_image_pixels = []


    #loop over image height 
    for y in range(new_height):

        #list to hold one row of pixels 
        row = []

        #loop over image width
        for x in range(new_width):
            
            #slider set to 0 - use image's first pixel
            if scale == 0.0:
                original_x = 0
                original_y = 0

            else: 
                #map new pixel to original pixel - applying scaling matrix 
                original_x = min(width-1, int(x/scale))
                original_y = min(height-1, int(y/scale))

            #get original pixels 
            pixels = original_pixels_rgb[original_y][original_x]

            #add pixel to the row 
            row.append(pixels)

        #add finished pixel to the scaled image
        scaled_image_pixels.append(row)
    

    #apply current brightness 
    brightness = brightness_scale.get()/100.0
    #create new ppm header 
    header_bytes = f"P6\n{new_width} {new_height}\n255\n".encode("ascii")


    #build and display the image 

    #array to hold pixel data 
    all_rgb_bytes = bytearray()

    #loop through every pixel 
    for row in scaled_image_pixels:
        for(R,G,B) in row:
            r = min(255, int(R * brightness)) * red_channel_multiplier
            g = min(255, int(G * brightness)) * green_channel_multiplier
            b = min(255, int(B * brightness)) * blue_channel_multiplier
            all_rgb_bytes.extend((r, g, b)) 
    
    #show the image 
    all_bytes = header_bytes + all_rgb_bytes
    photo = tk.PhotoImage(data=all_bytes, format="PPM")
    image_label.configure(image=photo)
    image_label.image = photo







#file browser 
def browse_file():
    filepath = tk.filedialog.askopenfilename()
    file_path_entry.delete(0, tk.END)
    file_path_entry.insert(0, filepath)

    



#UI code 
    
    
root = tk.Tk()

tk.Label(root, text="File Path").grid(row=0, column=0)

file_path_entry = tk.Entry(root, width=50)
file_path_entry.grid(row=0, column=1)

#buttons 

button_frame = tk.Frame(root)
button_frame.grid(row=1, column=0, columnspan=4)

tk.Button(button_frame, text="Browse", command=browse_file).grid(row=1, column=0)

tk.Button(button_frame, text="Open BMP Image", command=open_bmp_image).grid(row=1, column=1)

tk.Button(button_frame, text="Compress to .cpmt365", command = compress_to_365).grid(row=1, column=2)

tk.Button(button_frame, text="Decompress .cpmt365", command = decompress_365).grid(row=1, column=3)


#image widget

image_label = tk.Label(root)
image_label.grid(row = 2, column = 0, columnspan =2)

#metadata lables
file_size_label = tk.Label(root, text="File size: ")
file_size_label.grid(row=3, column=0, columnspan=2, sticky="w")

width_label = tk.Label(root, text="Width: ")
width_label.grid(row=4, column=0, columnspan=2, sticky="w")

height_label = tk.Label(root, text="Height: ")
height_label.grid(row=5, column=0, columnspan=2, sticky="w")

bpp_label = tk.Label(root, text="Bits per pixel: ")
bpp_label.grid(row=6, column=0, columnspan=2, sticky="w")

#brigtness slider
brightness_scale = tk.Scale(root, from_=0, to=100, orient="horizontal",
    label="Brightness (%)", command=redraw_the_image)
brightness_scale.set(100)
brightness_scale.grid(row=7, column=0, columnspan=2, sticky="we")

#size scale
size_scale = tk.Scale(
    root, from_= 0, to= 100, orient="horizontal",
    label = "Size(%)", command = redraw_the_image
)
size_scale.set(100) #default size 
size_scale.grid(row =8, column = 0, columnspan =2, sticky ="we")

#rgb toggles 
red_toggle = tk.BooleanVar(value=True)
green_toggle = tk.BooleanVar(value=True)
blue_toggle = tk.BooleanVar(value=True)

rgb_container_frame = tk.Frame(root)
rgb_container_frame.grid(row=9, column = 0, columnspan = 2, pady=(6,0))

tk.Checkbutton(rgb_container_frame, text = "Red", variable = red_toggle, command = redraw_the_image).pack()
tk.Checkbutton(rgb_container_frame, text = "Green", variable = green_toggle, command = redraw_the_image).pack()
tk.Checkbutton(rgb_container_frame, text = "Blue", variable = blue_toggle,command = redraw_the_image ).pack()


#background image 





#end of the UI block 

root.mainloop()



