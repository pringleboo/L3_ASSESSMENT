import csv
import random
from tkinter import *
from functools import partial  # To prevent unwanted windows
from PIL import Image, ImageTk


def get_data(mode):
    """
    Retrieves movie name, image file name, and the quote
    from the csv, so it can be used for the rounds
    """

    # Create separate lists of data to populate
    selected_movie_data = []
    other_movie_names = []

    # Loop 4 times (to get 4 random movies for the 2x2 grid)
    for i in range(4):

        # Open the csv file and randomly chose a row
        file = open("000_movie_quotes_emoji_v2.csv", "r")
        random_movie = random.choice(list(csv.reader(file, delimiter=",")))

        # Let the first random selection be the chosen movie
        # So the 2nd, 3rd, and 4th loop should only extract a movie name (we need 3 to
        # be incorrect answers). For these three we don't need to extract any of the other data (e.g. filename)
        if i >= 1:
            other_movie_names.append(random_movie[0])

        else:
            selected_movie_data.append(random_movie)

    print(selected_movie_data)
    print(f"Other names: {other_movie_names}")

    return selected_movie_data, other_movie_names


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
                               fg=item[2], bg=background_colour, wraplength=320,
                               justify="left", pady=10, padx=20)
            make_label.grid(row=count)

            start_label_ref.append(make_label)

        # Extract changing label so it can be configured later
        self.changing_label = start_label_ref[2]

        # Frame so that entry box and button can be in the same row
        self.entry_area_frame = Frame(self.start_frame)
        self.entry_area_frame.grid(row=3)

        # Create the entry frame
        self.num_rounds_entry = Entry(self.entry_area_frame, font=("Arial", 20, "bold"),
                                      width=20)
        self.num_rounds_entry.grid(row=0, column=0, padx=10, pady=0)

        # Create a frame for the play buttons
        self.play_frame = Frame(self.start_frame)
        self.play_frame.grid(row=4, padx=10, pady=10)

        # Create mode / play buttons

        # List for buttons (frame | text | bg | command | width | row | column)
        play_button_list = [
            [self.play_frame, "Normal Mode", "#1ca1e2", lambda: self.check_rounds("Normal"), 11, 0, 0],
            [self.play_frame, "Hard Mode", "#f0a30d", lambda: self.check_rounds("Hard"), 11, 0, 1],
        ]

        # Create buttons and add to list
        play_ref_list = []
        for item in play_button_list:
            make_play_button = Button(item[0], text=item[1], bg=item[2],
                                         command=item[3], font=("Arial", 16, "bold"),
                                         fg="#FFFFFF", width=item[4])
            make_play_button.grid(row=item[5], column=item[6])

            play_ref_list.append(make_play_button)

        # Change the frame backgrounds
        self.start_frame.config(bg=background_colour)
        self.entry_area_frame.config(bg=background_colour)

    # Checks number of rounds enters is a valid input
    def check_rounds(self, mode):

        # Retrieve rounds wanted from teh entry form
        rounds_wanted = self.num_rounds_entry.get()

        # Reset label and entry box (for when users come back to home screen)
        self.changing_label.config(text="How many rounds?", fg="#009900", font=("Arial", "12", "bold"))
        self.num_rounds_entry.config(bg="#FFFFFF")

        has_errors = "no"

        # Checks that the number of rounds wanted is above zero
        try:
            rounds_wanted = int(rounds_wanted)
            if rounds_wanted > 0:
                # Invoke Play Class (and take across number of rounds)
                Play(rounds_wanted, mode)
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

    def __init__(self, how_many, mode):
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
        [movie_data, movie_button_options] = get_data(None)

        # Extract the movie name, filename, and quote from the list
        movie_name = movie_data[0]
        file_name = f"{movie_data[1]}.png"
        quote = movie_data[2]
        num_of_emojis = int(movie_data[3])

        print(movie_button_options)

        # Open the image
        raw_image = Image.open(f'image_files/{file_name}')

        if mode == "Normal":

            # Hard code width and height values for ideal image resize
            width = 330
            height = 60

            # Resize the image to fit the width of the 2x2 button grid
            # No need to crop the image for Normal Mode
            resized_image = raw_image.resize((width, height))
            self.final_image = ImageTk.PhotoImage(resized_image)

            # Display the final image in the grid
            self.full_label = Label(self.quiz_frame, image=self.final_image)
            self.full_label.grid(row=1)


        # When mode is 'Hard'
        else:

            # Get image dimensions
            width, height = raw_image.size

            # According to number of emojis (3, 4 or 5), set the crop values
            # that will be used to crop the image to 2 emojis for hard mode
            if num_of_emojis == 3:
                crop = (width / 2.5, 0, width - 160, height)
                height = 151
            elif num_of_emojis == 4:
                crop = (width / 2, 0, width - 80, height)
                height = 151
            else:
                crop = (width / 1.7, 0, width, height)
                height = 145

            # Crop the image using the crop values from above
            cropped_image = raw_image.crop(crop)

            # Width is the same for all (matches the buttons width)
            width = 330

            # Scale the cropped image to fit into the grid nicely
            resized_image = cropped_image.resize((width, height))
            self.final_image = ImageTk.PhotoImage(resized_image)

            # Display the final image in the grid
            self.full_label = Label(self.quiz_frame, image=self.final_image)
            self.full_label.grid(row=1)


        # LABELS

        background_colour = "#f5ebc1"

        # List for label details (text | font | background | row)
        play_labels_list = [
            [f"Round # of {how_many}", ("Arial", "16", "bold"), 0],
            ["Select an option", ("Arial", "18"), 3]
        ]

        play_labels_ref = []
        for item in play_labels_list:
            self.make_label = Label(self.quiz_frame, text=item[0], font=item[1],
                                    bg=background_colour, wraplength=300, justify="left")
            self.make_label.grid(row=item[2], pady=10, padx=10)

            play_labels_ref.append(item)

        # Extract heading label so it can be configured with each new question
        self.heading_label = play_labels_ref[0]

        # Frame to hold hints and stats buttons
        self.hints_stats_frame = Frame(self.quiz_frame)
        self.hints_stats_frame.grid(row=6)

        # OPTION BUTTONS
        self.option_frame = Frame(self.quiz_frame)
        self.option_frame.grid(row=2)

        self.movie_button_ref = []
        self.option_button_list = []

        # Create four buttons in a 2 x 2 grid
        for item in range(0, 4):
            self.option_button = Button(self.option_frame, font=("Arial", 12, "bold"),
                                        text="Option", width=15, bg="#f2f2f2")
            self.option_button.grid(row=item // 2,
                                    column=item % 2,
                                    padx=5, pady=5)

            self.movie_button_ref.append(self.option_button)

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

        # self.stats_button.config(state=DISABLED)

        # Once interface has been created, invoke new
        # question function for first round.
        # self.new_question()


    # def new_question(self):
    #     """
    #     Chooses four colours, works out median for score to beat. Configures
    #     buttons with chosen colours
    #     """
    #
    #     # Retrieve number of rounds played, add one to it and configure heading
    #     rounds_played = self.rounds_played.get()
    #     self.rounds_played.set(rounds_played)
    #
    #     rounds_wanted = self.rounds_wanted.get()
    #
    #     # Update heading label with each new question
    #     self.heading_label.config(text=f"Round {rounds_played + 1} of {rounds_wanted}")
    #
    #     # Configure buttons using foreground and background colours from list
    #     # Enable colour buttons (disabled at the end of the last round)
    #     for count, item in enumerate(self.movie_button_ref):
    #         item.config(text=self.round_colour_list[count][0], state=NORMAL)
    #
    #     self.next_button.config(state=DISABLED)


    # def movie_data(self, list):
    #
    #     # Randomly select the next movie, place data into a list
    #     movie_data = get_images(None)
    #
    #     # Extract the movie name, filename, and quote from the list
    #     movie_name = list[0]
    #     file_name = f"{list[1]}.png"
    #     quote = list[2]
    #     num_of_emojis = int(list[3])

        #
        # # Open the image
        # raw_image = Image.open(f'image_files/{file_name}')



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
