from Graphics import *
from PIL import Image as PilImage, ImageTk

def swapImages(self, image_path, resize_x, resize_y, canvas_item, canvas_item_image):

    self.canvas_item = canvas_item
    self.canvas_item_image = canvas_item_image

    new_img = PilImage.open(image_path)
    new_img_resized = new_img.resize((resize_x, resize_y))
    new_tk_image = ImageTk.PhotoImage(new_img_resized)
    self.canvas_item_image = new_tk_image
    self.canvas.itemconfig(self.canvas_item, image=new_tk_image)

def swapImageWithoutResize(self, image_path, canvas_item, canvas_item_image):

    self.canvas_item = canvas_item
    self.canvas_item_image = canvas_item_image

    new_img = PilImage.open(image_path)
    new_tk_image = ImageTk.PhotoImage(new_img)
    self.canvas_item_image = new_tk_image
    self.canvas.itemconfig(self.canvas_item, image=new_tk_image)