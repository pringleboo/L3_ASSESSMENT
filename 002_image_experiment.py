from tkinter import *
from PIL import Image, ImageTk  # Import ImageTk for displaying cropped images


class ImageExperiment:

    def __init__(self):
        self.frame = Frame()
        self.frame.grid()

        # Open the image
        image = Image.open('image_files/12Monke.png')

        # Get image dimensions
        width, height = image.size

        self.full_image = ImageTk.PhotoImage(image)

        # Crop the left half (from x=0 to x=width/2)
        # (left | top | right | bottom)
        cropped_image = image.crop((100, 0, width - 100, height))

        # Convert to a format Tkinter can use
        self.cropped_img = ImageTk.PhotoImage(cropped_image)

        # Display the cropped image
        self.full_label = Label(self.frame, image=self.full_image)
        self.full_label.grid()

        self.cropped_label=Label(self.frame, image=self.cropped_img)
        self.cropped_label.grid()


if __name__ == '__main__':
    root = Tk()
    app = ImageExperiment()
    root.mainloop()
