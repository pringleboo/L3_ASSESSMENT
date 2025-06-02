from tkinter import *


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

        # Create a mini play frame to test check rounds function
        self.play_frame = Frame(self.play_box)
        self.play_frame.grid(padx=10, pady=10)

        # Create a simple label to check the play inputs work
        self.game_heading_label = Label(self.play_frame, text=f"Round 0 of {how_many}\n {mode} mode",
                                        font=("Arial", 16, "bold"))
        self.game_heading_label.grid(row=0)

        # Create the end game button
        self.end_game_button = Button(self.play_frame, text="End Game",
                                      font=("Arial", 16, "bold"),
                                      fg="#FFFFFF", bg="#990000", width="10",
                                      command=self.close_play)
        self.end_game_button.grid(row=1)

    # Closes the play GUI
    def close_play(self):
        # Reshow root (ie: choose rounds) and end current
        # quiz / allow new quiz to start
        root.deiconify()
        self.play_box.destroy()


# Main Routine

if __name__ == "__main__":
    root = Tk()
    root.title("Colour Quest")
    StartQuiz()
    root.mainloop()
