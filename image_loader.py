# image_loader.py

from PIL import Image, ImageTk

def load_images():
    top_image_pil = Image.open("top_image.jpg")
    top_image = ImageTk.PhotoImage(top_image_pil)

    bottom_image_pil = Image.open("bottom_image.jpg")
    bottom_image = ImageTk.PhotoImage(bottom_image_pil)

    return top_image, bottom_image
