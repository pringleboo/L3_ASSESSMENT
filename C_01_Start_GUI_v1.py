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

        self.start_frame = Frame(padx=10, pady=10, bg="#ede69f")
        self.start_frame.grid()

        # Strings for labels

        intro_string = ("----- Welcome ----- \n\nIn each round you will be given a set of emojis "
                        "that you must use as clue to guess the movie they represent."
                        "If you get stuck, click the hint button to get a quote from the movie.")

        # List of labels to be made (text | font | fg)
        start_labels_list = [
            ["Emoji Movie Quiz", ("Arial", "16", "bold"), None],
            [intro_string, ("Arial", "12"), None],
            ["How many rounds?", ("Arial", "12", "bold"), "#009900"]
        ]

        # Create labels and add them to the reference list...
        start_label_ref = []
        for count, item in enumerate(start_labels_list):
            make_label = Label(self.start_frame, text=item[0], font=item[1],
                               fg=item[2], wraplength=320,
                               justify="center", pady=10, padx=20,
                               bg="#ede69f")
            make_label.grid(row=count)

            start_label_ref.append(make_label)

        self.changing_label = start_label_ref[2]
        self.changing_label.config(pady=0)

        # Frame so that entry box and button can be in the same row
        self.entry_area_frame = Frame(self.start_frame)
        self.entry_area_frame.grid(row=3)

        self.num_rounds_entry = Entry(self.entry_area_frame, font=("Arial", "20", "bold"),
                                      width=20)
        self.num_rounds_entry.grid(row=0, column=0, padx=10, pady=0)

        # Create play button...
        self.play_button = Button(self.entry_area_frame, font=("Arial", "16", "bold"),
                                  fg="#FFFFFF", bg="#0057D8", text="Play", width=23,
                                  command=self.check_rounds)
        self.play_button.grid(row=4, padx=10, pady=10)

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
    Interface for playing the colour Quest Game
    """

    def __init__(self, how_many):
        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        self.game_heading_label = Label(self.game_frame, text=f"Round 0 of {how_many}",
                                        font=("Arial", "16", "bold"))
        self.game_heading_label.grid(row=0)

        self.end_game_button = Button(self.game_frame, text="End Game",
                                      font=("Arial", "16", "bold"),
                                      fg="#FFFFFF", bg="#990000", width="10",
                                      command=self.close_play)
        self.end_game_button.grid(row=1)

    def close_play(self):
        # Reshow root (ie: choose rounds) and end current
        # game / allow new game to start
        root.deiconify()
        self.play_box.destroy()


# Main Routine

if __name__ == "__main__":
    root = Tk()
    root.title("Colour Quest")
    StartQuiz()
    root.mainloop()
