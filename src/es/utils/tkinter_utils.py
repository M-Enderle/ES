from tkinter import ttk
from PIL import Image, ImageTk

def add_image_to_frame(frame, image_path, size_multiplier=1.0):
    """Add an image to a frame.

    Args:
        frame (tk.Frame): The frame to add the image to.
        image_path (str): The path to the image.
        image_size (tuple): The size of the image (width, height).

    Returns:
        tk.Label: The label widget containing the image.
    """

    img = Image.open(image_path)

    img = img.resize(
            (int(img.size[0] * size_multiplier), 
             int(img.size[1] * size_multiplier)), 
        Image.LANCZOS)

    photo = ImageTk.PhotoImage(img)

    image_label = frame.Label("Image",
                widgetkwargs={
                    "image": photo,
                })
    
    image_label.image = photo
    return image_label
