from tkinter import *
from PIL import Image, ImageTk  # Import ImageTk for displaying cropped images
import os, random
#
# class ImageExperiment:
#
#     def __init__(self):
#         self.frame = Frame()
#         self.frame.grid()
#
#         # Open the image
#         image = Image.open('image files/Abugs.png')
#
#         # Get image dimensions
#         width, height = image.size
#
#         self.full_image = ImageTk.PhotoImage(image)
#
#         # Crop the left half (can be altered to crop certain widths)
#         cropped_image = image.crop((width * .2, 0, width * .6, height))
#
#         # Convert to a format Tkinter can use
#         self.cropped_img = ImageTk.PhotoImage(cropped_image)
#
#         # Display the cropped image
#         self.full_label = Label(self.frame, image=self.full_image)
#         self.full_label.grid()
#
#         self.cropped_label = Label(self.frame, image=self.cropped_img)
#         self.cropped_label.grid()


# class StartGame:
#
#     def __init__(self):
#         self.start_frame = Frame(padx=10, pady=10)
#         self.start_frame.grid()
#
#         self.head = Label(text="🚋💔🎭", font=("", "100", ""), fg="#b87914")
#         self.head.grid()

#
# if __name__ == "__main__":
#     root = Tk()
#     root.title("Sandbox")
#     app = ImageExperiment()
#     root.mainloop()

def get_random_image_path(folder_path):
    try:
        files = os.listdir(folder_path)
        # Filter the list to get only image files
        images = [file for file in files if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

        if not images:
            print("No images found in the specified folder.")
            return None

        # Choose a random image file
        random_image = random.choice(images)
        random_image_path = os.path.join(folder_path, random_image)
        return random_image_path

    except Exception as e:
        print(f"An error occurred while selecting image randomly: {e}")
        return None


def display_image(image_path):
    try:
        if image_path and os.path.isfile(image_path):
            with Image.open(image_path) as img:
                img.show()
                print(f"Displayed image: {image_path}")
        else:
            print(f"Invalid image path: {image_path}")
    except Exception as e:
        print(f"An error occurred while displaying the image: {e}")


def show_random_image_from_folder(folder_path):
    random_image_path = get_random_image_path(folder_path)
    display_image(random_image_path)


# usage:
if __name__ == "__main__":
    folder_path = '/image_files'
    if os.path.isdir(folder_path):
        show_random_image_from_folder(folder_path)
    else:
        print(f" The specified folder does not exist: {folder_path}")


