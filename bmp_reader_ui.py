import tkinter as tk
import tkinter.filedialog
import base64


from tkinter import messagebox



from bmp_reader import read_bmp

#holds decoded BMP pixels 
original_pixels_rgb = None 


#file validation function
def validate_file(bmp_bytes):
    #bmp file has header 14 bytes that contains signature 2 bytes

    #checks and returns boolea for file signature 
    return bmp_bytes[:2] == b'BM'


#bmp reader ui 

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

    #call color changing function - also displays the image 
    change_color()


    #update metadata labels

    file_size_label.config(text=f"File size: {metadata['file_size']} bytes")
    width_label.config(text=f"Width: {metadata['width']} px")
    height_label.config(text=f"Height: {metadata['height']} px")
    bpp_label.config(text=f"Bits per pixel: {metadata['bits_per_pixel']}")




def change_color(*_):


    #check if image is loaded

    if original_pixels_rgb is None:
        return
    
    #reads the value from the brightless slider -> scaling factor in the range 0.0 - 1.0
    factor = brightness_scale.get()/100.0 

    #get height and width of the image from the stored pixel array 
    h = len(original_pixels_rgb)
    w = len(original_pixels_rgb[0])


    #build PPM image header in bytes for Tkinter
    header_bytes = f"P6\n{w} {h}\n255\n".encode("ascii")


    #holds new pixel data with adjusted brightness 
    all_rgb_bytes = bytearray()
    
    #loop through original pixels 
    for row in original_pixels_rgb:
        #adjust the brightness 
        for (R, G, B) in row:
            r = min(255, int(R * factor))
            g = min(255, int(G * factor))
            b = min(255, int(B * factor))

            #put adjusted pixels in the byte array 
            all_rgb_bytes.extend((r, g, b))


    #combine header data with new pixel data 
    all_bytes = header_bytes + all_rgb_bytes


    #show the image

    photo = tk.PhotoImage(data = all_bytes, format = "PPM")
    image_label.configure(image = photo)
    image_label.image = photo




 




#file browser 
def browse_file():
    filepath = tk.filedialog.askopenfilename()
    file_path_entry.delete(0, tk.END)
    file_path_entry.insert(0, filepath)




    
    

root = tk.Tk()

tk.Label(root, text="File Path").grid(row=0, column=0)

file_path_entry = tk.Entry(root, width=50)
file_path_entry.grid(row=0, column=1)

tk.Button(root, text="Browse", command=browse_file).grid(row=1, column=0)

tk.Button(root, text="Open BMP Image", command=open_bmp_image).grid(row=1, column=1)


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
    label="Brightness (%)", command=change_color)
brightness_scale.set(100)
brightness_scale.grid(row=7, column=0, columnspan=2, sticky="we")


#end of the UI block 

root.mainloop()



