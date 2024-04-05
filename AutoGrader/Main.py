import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import code_handler 

def open_code():
    # Call the function to open the code GUI from code module
    code_handler.create_code_gui()

    # Remove or comment out the messagebox since it's no longer necessary
    # messagebox.showinfo("Code Option Selected", "You selected the Code option")

def open_pdf():
    messagebox.showinfo("PDF Option Selected", "You selected the PDF option")

def exit_application():
    if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
        root.destroy()

root = tk.Tk()
root.title("Menu Options")

root.attributes('-fullscreen', True)

canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
canvas.pack()

# Using a hex color code for background
background_color = "#486474"
canvas.create_rectangle(0, 0, root.winfo_screenwidth(), root.winfo_screenheight(), fill=background_color)

# Load top image using PIL
top_image_pil = Image.open("top_image.jpg")
top_image = ImageTk.PhotoImage(top_image_pil)

# Display top image on canvas
canvas.create_image(0, 0, anchor=tk.NW, image=top_image)

label = tk.Label(root, text="Welcome To The Autograder", font=("Helvetica", 30),fg ='#486474', bg='#080a09')
label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

code_button = tk.Button(root, text="Code", font=("Helvetica", 20),fg ='#486474', bg='#080a09' ,command=open_code)
code_button.place(relx=0.4, rely=0.5, anchor=tk.CENTER)

pdf_button = tk.Button(root, text="PDF", font=("Helvetica", 20),fg ='#486474', bg='#080a09',command=open_pdf)
pdf_button.place(relx=0.6, rely=0.5, anchor=tk.CENTER)

exit_button = tk.Button(root, text="Exit", font=("Helvetica", 20),fg ='#486474', bg='#080a09',command=exit_application)
exit_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

# Load bottom image using PIL
bottom_image_pil = Image.open("bottom_image.jpg")
bottom_image = ImageTk.PhotoImage(bottom_image_pil)

# Display bottom image at the bottom of the window
canvas.create_image(0, root.winfo_screenheight(), anchor=tk.SW, image=bottom_image)

root.mainloop()
