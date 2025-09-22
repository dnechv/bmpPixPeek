import tkinter as tk
import tkinter.filedialog
import base64



from bmp_reader import read_bmp


#bmp reader ui 

#opens BMP image 
def open_bmp_image():
    #get the file path
    file_path = file_path_entry.get()
    #get pixels 
    pixels_rgb = read_bmp(file_path)
    #fill the pixels 

    #compute the image size
    height = len(pixels_rgb)
    width = len(pixels_rgb[0])

    #build header 
    header_bytes = f"P6\n{width} {height}\n255\n".encode("ascii")


    #byte array for the image 
    all_rgb_bytes = bytearray()


    #loop through every row in pixels rgb

    for row in pixels_rgb:

        #loop over each pixel in the row 
        for (R,G,B) in row:

            all_rgb_bytes.extend([R,G,B])
    
  
    #create a photo image from all bytes 
    photo = tk.PhotoImage(data = all_bytes, format = "PPM")
    #display photo in the image label 
    image_label.configure(image = photo)
    #store the reference inside the label widget 
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



#end of the UI block 

root.mainloop()



