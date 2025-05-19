import csv
import random
from tkinter import *
# from functools import partial  # To prevent unwanted windows
from PIL import Image, ImageTk


# Helper Functions...

def get_images(mode):
    """
    Retrieves movie name, image file name, and the quote
    from the csv, so it can be used for the rounds
    """

    # Retrieve the movie data from csv, put it in a list
    file = open("000_movie_quotes_emoji.csv", "r")
    file_names = random.choice(list(csv.reader(file, delimiter=",")))
    file.close()

    print(file_names)

    return file_names


class StartQuiz:
    """
    Initial Quiz interface (asks users how many rounds they
    would like to play)
    """

    def __init__(self):
        """
        Gets number of rounds from user
        """

        # Create frame and setup grid
        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        # String for the intro label
        intro_string = ("In each round you will be given a set of emojis "
                        "that you must use as clue to guess the movie they represent."
                        "If you get stuck, click the hint button to get a quote from the movie.")

        background_colour = "#f5ebc1"

        # List of labels to be made (text | font | fg)
        start_labels_list = [
            ["Emoji Movie Quiz", ("Arial", "16", "bold"), None],
            [intro_string, ("Arial", "12"), None],
            ["How many rounds?", ("Arial", "12", "bold"), "#009900"]
        ]

        # Create labels and give them names
        start_label_ref = []
        for count, item in enumerate(start_labels_list):
            make_label = Label(self.start_frame, text=item[0], font=item[1],
                               fg=item[2], bg="#f5ebc1", wraplength=320,
                               justify="left", pady=10, padx=20)
            make_label.grid(row=count)

            start_label_ref.append(make_label)

            # Alternative naming method (creates issues)

            # # List of the names that need to be given to the labels
            # label_names = ['title_label', 'text_label', 'changing_label']

            # # Assign names to the labels using the index
            # if count < len(label_names):
            #     setattr(self, label_names[count], make_label)

        # Extract changing label so it can be configured later
        self.changing_label = start_label_ref[2]

        # Frame so that entry box and button can be in the same row
        self.entry_area_frame = Frame(self.start_frame)
        self.entry_area_frame.grid(row=3)

        self.num_rounds_entry = Entry(self.entry_area_frame, font=("Arial", 20, "bold"),
                                      width=20)
        self.num_rounds_entry.grid(row=0, column=0, padx=10, pady=0)

        # Create play button...
        self.play_button = Button(self.entry_area_frame, font=("Arial", 16, "bold"),
                                  fg="#d99829", bg="#fcfc86", text="Play", width=23,
                                  command=self.check_rounds, borderwidth=3, relief="raised")
        self.play_button.grid(row=4, padx=10, pady=10)

        # Change the frame backgrounds
        self.start_frame.config(bg=background_colour)
        self.entry_area_frame.config(bg=background_colour)

    # Checks number of rounds enters is a valid input
    def check_rounds(self):

        # Retrieve temperature to be converted
        rounds_wanted = self.num_rounds_entry.get()

        # Reset label and entry box (for when users come back to home screen)
        self.changing_label.config(text="How many rounds?", fg="#009900", font=("Arial", "12", "bold"))
        self.num_rounds_entry.config(bg="#FFFFFF")

        has_errors = "no"

        # Checks that the amount to be converted is a number above absolute zero
        try:
            rounds_wanted = int(rounds_wanted)
            if rounds_wanted > 0:
                # Invoke Play Class (and take across number of rounds)
                Play(rounds_wanted)
                # Hide root_window (ie: hide rounds choice window)
                root.withdraw()

            else:
                has_errors = "yes"

        except ValueError:
            has_errors = "yes"

        # Display the error if necessary
        if has_errors == "yes":
            self.changing_label.config(text="Oops - Please enter a whole number more than 0",
                                       fg="#990000", font=("Arial", "9", "bold"))
            self.num_rounds_entry.config(bg="#F4CCCC")
            self.num_rounds_entry.delete(0, END)


class Play:
    """
    Interface for playing the Emoji Movie Quiz
    """

    def __init__(self, how_many):
        self.play_box = Toplevel()

        # Rounds played - start with zero
        self.rounds_played = IntVar()
        self.rounds_played.set(0)

        self.rounds_wanted = IntVar()
        self.rounds_wanted.set(how_many)

        self.quiz_frame = Frame(self.play_box, padx=10, pady=10)
        self.quiz_frame.grid()

        # IMAGES

        # Randomly select the next movie, place data into a list
        movie_data = get_images(None)

        # Extract the movie name, filename, and quote from the list
        movie_name = movie_data[0]
        file_name = f"{movie_data[1]}.png"
        quote = movie_data[2]
        num_of_emojis = movie_data[3]

        # Open the image
        raw_image = Image.open(f'image_files/{file_name}')


        mode = input("Mode: ")


        if mode == "n":

            width = 330
            height = 60
            resized_image = raw_image.resize((width, height))

            self.final_image = ImageTk.PhotoImage(resized_image)


        elif mode == "h":

            # Get image dimensions
            width, height = raw_image.size

            # Crop the left half (can be altered to crop certain widths)
            cropped_image = raw_image.crop((120, 0, width * .6, height))

            width = 330
            height = 60
            resized_image = cropped_image.resize((width, height))

            self.final_image = ImageTk.PhotoImage(resized_image)


        # Display the image
        self.full_label = Label(self.quiz_frame, image=self.final_image)
        self.full_label.grid(row=1)

        background_colour = "#f5ebc1"

        # LABELS

        # List for label details (text | font | background | row)
        play_labels_list = [
            ["Round # of #", ("Arial", "16", "bold"), 0],
            ["Select an option", ("Arial", "18"), 3]
        ]

        play_labels_ref = []
        for item in play_labels_list:
            self.make_label = Label(self.quiz_frame, text=item[0], font=item[1],
                                    bg=background_colour, wraplength=300, justify="left")
            self.make_label.grid(row=item[2], pady=10, padx=10)

            play_labels_ref.append(item)

        # Frame to hold hints and stats buttons
        self.hints_stats_frame = Frame(self.quiz_frame)
        self.hints_stats_frame.grid(row=6)

        # OPTION BUTTONS
        self.option_frame = Frame(self.quiz_frame)
        self.option_frame.grid(row=2)

        self.option_button_ref = []
        self.option_button_list = []

        # Create four buttons in a 2 x 2 grid
        for item in range(0, 4):
            self.option_button = Button(self.option_frame, font=("Arial", 12, "bold"),
                                        text="Option", width=15, bg="#f2f2f2")
            self.option_button.grid(row=item // 2,
                                    column=item % 2,
                                    padx=5, pady=5)

            self.option_button_ref.append(self.option_button)

        # CONTROL BUTTONS

        self.control_frame = Frame(self.quiz_frame)
        self.control_frame.grid(row=3)

        # List for buttons (frame | text | bg | command | width | row | column)
        control_button_list = [
            [self.quiz_frame, "Next Round", "#1ca1e2", None, 25, 5, None],
            [self.hints_stats_frame, "Hints", "#f0a30d", None, 12, 0, 0],
            [self.hints_stats_frame, "End", "#ff3232", self.close_play, 12, 0, 1],
        ]

        # Create buttons and add to list
        control_ref_list = []
        for item in control_button_list:
            make_control_button = Button(item[0], text=item[1], bg=item[2],
                                         command=item[3], font=("Arial", 16, "bold"),
                                         fg="#FFFFFF", width=item[4])
            make_control_button.grid(row=item[5], column=item[6])

            control_ref_list.append(make_control_button)

        # Retrieve next, stats and end button so that they can be configured
        self.next_button = control_ref_list[0]
        self.hint_button = control_ref_list[1]
        self.end_button = control_ref_list[2]

        # Change the frame backgrounds
        self.quiz_frame.config(bg=background_colour)
        self.option_frame.config(bg=background_colour)
        self.hints_stats_frame.config(bg=background_colour)

        # # Once interface has been created, invoke new
        # # round function for first round.
        # self.new_question()3

    # Closes the play GUI
    def close_play(self):
        # Reshow root (ie: choose rounds) and end current
        # quiz / allow new quiz to start
        root.deiconify()
        self.play_box.destroy()


# Main Routine

if __name__ == "__main__":
    root = Tk()
    root.title("Emoji Movie Quiz")
    StartQuiz()
    root.mainloop()
