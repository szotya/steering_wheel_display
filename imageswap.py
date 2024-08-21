from Graphics import *
from PIL import Image as PilImage, ImageTk

class ImageSwapper:
    def __init__(self):
        pass

    def swapImages(self, canvas, image_path, resize_x, resize_y, canvas_item, canvas_item_image):
        new_img = PilImage.open(image_path)
        new_img_resized = new_img.resize((resize_x, resize_y))
        new_tk_image = ImageTk.PhotoImage(new_img_resized)
        canvas_item_image = new_tk_image
        canvas.itemconfig(canvas_item, image=new_tk_image)
        return canvas_item_image

    def swapImageWithoutResize(self, canvas, image_path, canvas_item, canvas_item_image):
        new_img = PilImage.open(image_path)
        new_tk_image = ImageTk.PhotoImage(new_img)
        canvas.itemconfig(canvas_item, image=new_tk_image)
        canvas_item_image = new_tk_image
        return canvas_item_image