import csv
import random
from tkinter import *
from functools import partial  # To prevent unwanted windows
from PIL import Image, ImageTk



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
                        "that you must use as clues to guess the movie they represent."
                        "If you get stuck, click the hint button to get a quote from the movie.")

        # BG colour for labels and frames
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

            # Add the label to a list to extract from
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

        # Create buttons using the list
        for item in play_button_list:
            make_play_button = Button(item[0], text=item[1], bg=item[2],
                                         command=item[3], font=("Arial", 16, "bold"),
                                         fg="#FFFFFF", width=item[4])
            make_play_button.grid(row=item[5], column=item[6])

        # Change the frames background colours
        self.start_frame.config(bg=background_colour)
        self.entry_area_frame.config(bg=background_colour)

    # Checks number of rounds enters is a valid input
    def check_rounds(self, mode):

        """
        When normal / hard button pressed, check the number of rounds wanted is a valid input
        (i.e. an integer above 0)
        """

        # Retrieve rounds wanted from the entry form
        rounds_wanted = self.num_rounds_entry.get()

        # Reset label and entry box (for when users come back to home screen)
        self.changing_label.config(text="How many rounds?", fg="#009900", font=("Arial", "12", "bold"))
        self.num_rounds_entry.config(bg="#FFFFFF")

        has_errors = "no"

        # Checks that the number of rounds wanted is above zero and not an invalid input
        try:
            rounds_wanted = int(rounds_wanted)
            if rounds_wanted > 0:

                # Invoke Play Class (and take across number of rounds)
                Play(rounds_wanted, mode)

                # Hide root_window (ie: hide rounds choice window)
                root.withdraw()

            else:
                has_errors = "yes"

        # If it's an invalid input (i.e. a letter)
        except ValueError:
            has_errors = "yes"

        # Display the error if necessary by configuring the changing label
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

        # Bring the Play GUI to the front
        self.play_box = Toplevel()

        # Create an empty list for movie button options
        self.movie_button_options = []

        # Set up rounds_won as an integer variable
        self.rounds_won = IntVar()

        # Rounds played - start with zero
        self.rounds_played = IntVar()
        self.rounds_played.set(0)

        # Set rounds wanted to the number specified in the start GUI
        self.rounds_wanted = IntVar()
        self.rounds_wanted.set(how_many)

        # Create the play frame and set to grid
        self.quiz_frame = Frame(self.play_box, padx=10, pady=10)
        self.quiz_frame.grid()

        # BG colour for labels and frame
        background_colour = "#f5ebc1"

        # List for label details (text | font | row)
        play_labels_list = [
            [f"Round # of {how_many}", ("Arial", "16", "bold"), 0],
            ["Select an option", ("Arial", "18"), 3]
        ]

        # Create the two labels using the list above
        play_labels_ref = []
        for item in play_labels_list:
            self.make_label = Label(self.quiz_frame, text=item[0], font=item[1],
                                    bg=background_colour, wraplength=300, justify="left")
            self.make_label.grid(row=item[2], pady=10, padx=10)

            # add the label to a list so it can be extracted
            play_labels_ref.append(self.make_label)

        # Extract labels so they can be configured with each new question
        self.heading_label = play_labels_ref[0]
        self.play_changing_label = play_labels_ref[1]

        # Create frame to hold movie option buttons
        self.option_frame = Frame(self.quiz_frame)
        self.option_frame.grid(row=2)

        # Create movie option buttons. For now they will display 'Option'
        # When a button is clicked, it sends user to round_results to check their answer
        self.movie_button_ref = []
        for item in range(0, 4):
            self.option_button = Button(self.option_frame, font=("Arial", 12, "bold"),
                                        text="Option", command=partial(self.round_results, item),
                                        width=32, bg="#f2f2f2")
            self.option_button.grid(row=item, padx=5, pady=2)

            # Add the button to a list so it can extracted and configured later on
            self.movie_button_ref.append(self.option_button)

        # Create frame to hold hint and end buttons
        self.hints_end_frame = Frame(self.quiz_frame)
        self.hints_end_frame.grid(row=6)

        # List for button details (frame | text | bg | command | width | row | column)
        # Note we are also specifying the 'Next Round' button here
        control_button_list = [
            [self.quiz_frame, "Next Round", "#1ca1e2", lambda: self.new_question(mode), 25, 5, None],
            [self.hints_end_frame, "Need a hint?", "#f0a30d", self.display_hint, 12, 0, 0],
            [self.hints_end_frame, "End", "#ff3232", self.close_play, 12, 0, 1],
        ]

        # Create the control buttons
        # When 'Next Round' is pressed --> go to 'new_question' function
        # When hint button is pressed --> go to 'display_hint' function
        # When end button pressed --> go to 'close_play' function
        control_ref_list = []
        for item in control_button_list:
            make_control_button = Button(item[0], text=item[1], bg=item[2],
                                         command=item[3], font=("Arial", 16, "bold"),
                                         fg="#FFFFFF", width=item[4])
            make_control_button.grid(row=item[5], column=item[6])

            # Add buttons to list so they can be extracted
            control_ref_list.append(make_control_button)

        # Retrieve next, hints and end button so that they can be configured (enabled and disabled) later
        self.next_button = control_ref_list[0]
        self.hint_button = control_ref_list[1]
        self.end_button = control_ref_list[2]

        # Change the frame background colours
        self.quiz_frame.config(bg=background_colour)
        self.option_frame.config(bg=background_colour)
        self.hints_end_frame.config(bg=background_colour)

        # Once interface has been created, invoke new
        # question function for first round
        self.new_question(mode)


    def new_question(self, mode):
        """
        Gets the next question ready, configures round heading,
        populates option buttons
        """

        # Call the get_data function to generate data
        # (i.e. movie options and an image) for the question
        self.get_data(mode)

        # Retrieve number of rounds played and wanted so they can be counted with each round
        rounds_played = self.rounds_played.get()
        rounds_wanted = self.rounds_wanted.get()

        # Reset changing label
        self.play_changing_label.config(text="Select an option", fg="#000000")

        # Update heading label with new rounds variables
        self.heading_label.config(text=f"Round {rounds_played + 1} of {rounds_wanted}")

        # Shuffle buttons lists so movie option buttons display in random positions
        random.shuffle(self.movie_button_options)

        # Get the win index to later compare users selected answer
        self.win_index = self.movie_button_options.index(self.movie_name)

        # Configure buttons text as the names of the random movies generated for the question
        for count, item in enumerate(self.movie_button_ref):

            item.config(text=self.movie_button_options[count], bg="#f2f2f2", state=NORMAL)

        # Disable next button until user has selected an answer
        self.next_button.config(state=DISABLED)

        # Enable the hints button
        self.hint_button.config(state=NORMAL)


    def get_data(self, mode):
        """
        Retrieves movie name, image file name, movie quote and number of emojis
        from the csv, so it can be used for the questions
        """

        # Create separate lists to populate with data
        self.selected_movie_data = []
        self.other_movie_names = []

        i = 0 # Use as loop counter
        # Loop 4 times (to get 4 random movies for the 1x4 grid)
        while len(self.other_movie_names) < 3:

            # Open the csv file and randomly chose a row
            file = open("000_movie_quotes_emoji_v2.csv", "r")
            potential_movie = random.choice(list(csv.reader(file, delimiter=",")))

            # Let the first random movie be the chosen movie (the answer to the question)
            if i == 0:
                self.selected_movie_data = potential_movie

            # If the potential movie is not already in the list (or is the selected movie), then we can use it
            # This should prevent deplicate movies being extracted for the same question
            elif potential_movie[0] not in self.other_movie_names and potential_movie[0] != self.selected_movie_data[0]:
                self.movie_button_options.append(potential_movie[0])

            i += 1 # add to count

        # Extract the movie name, filename, quote, and no. of emojis from the list
        self.movie_name = self.selected_movie_data[0]
        self.file_name = f"{self.selected_movie_data[1]}.png" # include '.png' file format for later
        self.quote = self.selected_movie_data[2]
        self.num_of_emojis = int(self.selected_movie_data[3])

        # Add the chosen movie to the option button list (so we have 4 items)
        self.movie_button_options.append(self.movie_name)

        # Call image_display function to generate image
        self.image_display(mode)


    def image_display(self, mode):
        """
        Extracts image file from folder and adjusts image depending on normal / hard mode.
        For hard mode the image is cropped case-specifically to remove some emojis so the
        cropped image only has 2 emojis visible, making it harder for the user
        """

        # Open the image corresponding to the chosen movie
        raw_image = Image.open(f'image_files/{self.file_name}')

        if mode == "Normal":

            # Hard code width and height values for ideal image resize
            width = 330
            height = 60

            # Resize the image to fit the width of the movie option buttons
            # No need to crop the image for Normal Mode
            resized_image = raw_image.resize((width, height))
            self.final_image = ImageTk.PhotoImage(resized_image)

            # Display the final image in the quiz frame grid
            self.full_label = Label(self.quiz_frame, image=self.final_image)
            self.full_label.grid(row=1)

        # When mode is 'Hard'
        else:

            # Get image dimensions
            width, height = raw_image.size

            # According to number of emojis (3, 4 or 5), set the crop values
            # that will be used to crop the image to 2 emojis for hard mode
            if self.num_of_emojis == 3:
                crop = (width / 2.5, 0, width - 160, height)
                height = 151
            elif self.num_of_emojis == 4:
                crop = (width / 2, 0, width - 80, height)
                height = 151
            else:
                crop = (width / 1.7, 0, width, height)
                height = 145

            # Crop the image using the crop values from above
            cropped_image = raw_image.crop(crop)

            # Width is the same for all (matches the option buttons width)
            width = 330

            # Scale the cropped image to fit into the grid nicely
            resized_image = cropped_image.resize((width, height))
            self.final_image = ImageTk.PhotoImage(resized_image)

            # Display the final image in the grid
            self.full_label = Label(self.quiz_frame, image=self.final_image)
            self.full_label.grid(row=1)


    def round_results(self, user_choice):
        """
        Retrieves which button was pushed (index 0 - 3), retrieves
        score and then compares it with median, updates results
        and adds results to stats list.
        """

        print(f"selected item - {user_choice}")
        print(f"Win button number: {self.win_index + 1}")

        if user_choice == self.win_index:
            result_text = "Correct!"
            print(result_text)
            label_colour = "#009900" # green text for changing label
            selected_btn_bg = "#00E000" # green background colour for selected button

            # Add 1 to the number round rounds won
            rounds_won = self.rounds_won.get()
            rounds_won += 1
            self.rounds_won.set(rounds_won)


        else:
            result_text = "Incorrect"
            print(result_text)
            label_colour = "#ff3232" # red text for changing label
            selected_btn_bg = "#ff3232" # red background colour for selected button

            # Highlight the correct button as green so users can compare their answer
            self.movie_button_ref[self.win_index].config(bg="#00E000")

        self.movie_button_ref[user_choice].config(bg=selected_btn_bg)

        self.play_changing_label.config(text=result_text, fg=label_colour, font=("Arial", 18))

        # Enables stats & next buttons, disable colour buttons
        self.next_button.config(state=NORMAL)
        self.hint_button.config(state=DISABLED)

        # Add one to the number of rounds played and retrieve
        # the number of rounds won
        rounds_played = self.rounds_played.get()
        rounds_played += 1
        self.rounds_played.set(rounds_played)

        # Check to see if game is over
        rounds_wanted = self.rounds_wanted.get()

        rounds_won = self.rounds_won.get()

        # Code for when game ends
        if rounds_played == rounds_wanted:
            # Work out success rate
            print(f"You won {rounds_won} out of {rounds_played}")

            # Configure end game labels / buttons
            self.heading_label.config(text="No more questions")
            self.play_changing_label.config(text="All done!", fg="#000000")
            self.next_button.config(state=DISABLED)

        # Disable option buttons once user chooses an answer
        for item in self.movie_button_ref:
            item.config(state=DISABLED)

    def display_hint(self):

        self.play_changing_label.config(text=f'Hint:\n " {self.quote} "', font=8,
                                        fg="#996c14", wraplength=300, justify="center")
        self.hint_button.config(state=DISABLED)
        hints_used = 0
        hints_used += 1

    # Closes the play GUI and automatically opens stats GUI
    def close_play(self):

        self.play_box.destroy()

        # IMPORTANT: Retrieve number of rounds
        # won as a number (rather than the 'self' container)
        rounds_won = self.rounds_won.get()
        rounds_played = self.rounds_played.get()
        rounds_wanted = self.rounds_wanted.get()
        stats_bundle = [rounds_won, rounds_played, rounds_wanted]

        # Send to stats GUI
        Stats(self, stats_bundle)


class Stats:

    def __init__(self, partner, all_stats_info):

        # Extract information from master list...
        rounds_won = all_stats_info[0]
        rounds_played = all_stats_info[1]
        rounds_wanted = all_stats_info[2]

        # setup dialogue box and background colour
        self.stats_box = Toplevel()

        self.stats_frame = Frame(self.stats_box, width=500,
                                 height=700)
        self.stats_frame.grid()

        rounds_string = f"\n{rounds_played} rounds played out of {rounds_wanted}"
        correct_string = f"{rounds_won} correct"
        incorrect_string = f"{rounds_played - rounds_won} incorrect"

        if rounds_played == 0:
            score = 0
        else:
            score = int((rounds_won / rounds_played) * 100)
        score_string = f"\nScore = {score:.0f}"

        colour_map = [
            "#8B0000", # Red end
            "#A52A2A",
            "#B04C2C",
            "#C06F25",
            "#C78F1C",
            "#BDAF12",
            "#9EB210",
            "#7AA40D",
            "#569A0B",
            "#3F850A" # Green end
        ]

        if score == 0:
            fg_colour = colour_map[0]
        else:
            fg_colour = colour_map[int(str(score)[:-1]) - 1]

        if score >= 50:
            comment_string = "Well done!"
            bg_colour ="#81e385" # Green
        else:
            comment_string = "Better luck next time!"
            bg_colour = "#e38191" # Pink

        # Configure the background colour of the GUI
        self.stats_frame.config(bg=bg_colour)

        all_stats_strings = [
            ["\nQuiz Statistics", ("Arial", 14, "bold"), "W"],
            [rounds_string, ("Arial", 10, "bold"), "W"],
            [correct_string, ("Arial", 10, "bold"), "W"],
            [incorrect_string, ("Arial", 10, "bold"), "W"],
            [score_string, ("Arial", 16, "bold"), "W"],
            [comment_string, ("Arial", 9, "bold"), "W"],
        ]

        stats_label_ref_list = []
        for count, item in enumerate(all_stats_strings):
            self.stats_label = Label(self.stats_frame, text=item[0], font=item[1],
                                     anchor="w", justify="left",
                                     padx=30, pady=5, bg=bg_colour)
            self.stats_label.grid(row=count, sticky=item[2], padx=10)
            stats_label_ref_list.append(self.stats_label)

        print(stats_label_ref_list)
        self.score_label = stats_label_ref_list[4]
        self.score_label.config(fg=fg_colour)

        self.close_button = Button(self.stats_frame, text="Close",
                                   font=("Arial", 12, "bold"), bg="#ffffff",
                                   command=partial(self.close_stats, partner),
                                   padx=45, pady=5)
        self.close_button.grid(row=6, pady=15)

        # If users press cross at top, closes stats and
        # 'releases' stats button
        self.stats_box.protocol('WM_DELETE_WINDOW',
                                partial(self.close_stats, partner))


    def close_stats(self, partner):
        """
        Closes stats dialogue box
        """

        # Reshow root (ie: choose rounds) and end current
        # quiz / allow new quiz to start
        root.deiconify()
        self.stats_box.destroy()



# Main Routine

if __name__ == "__main__":
    root = Tk()
    root.title("Emoji Movie Quiz")
    StartQuiz()
    root.mainloop()
