#     """
#     Displays hints for playing game
#     :return:
#     """
#     DisplayHints(self)

def new_question(self):
    """
    Chooses four colours, works out median for score to beat. Configures
    buttons with chosen colours
    """

    # Retrieve number of rounds played, add one to it and configure heading
    rounds_played = self.rounds_played.get()
    rounds_played += 1
    self.rounds_played.set(rounds_played)


class DisplayHints:
    """
    Displays hints for colour quest game
    """

    def __init__(self, partner):
        # setup dialogue box and background colour
        background = "#ffe6cc"
        self.hints_box = Toplevel()

        # Disable hints button
        partner.hints_button.config(state=DISABLED)

        # If users press cross at top, closes hints and
        # 'releases' hints button
        self.hints_box.protocol('WM_DELETE_WINDOW',
                                partial(self.close_hints, partner))

        self.hints_frame = Frame(self.hints_box, width=300,
                                 height=200)
        self.hints_frame.grid()

        self.hints_heading_label = Label(self.hints_frame,
                                         text="Hints",
                                         font=("Arial", "14", "bold"))
        self.hints_heading_label.grid(row=0)

        hints_text = "To use the program, simply enter the temperature " \
                     "you wish to convert and then choose to convert " \
                     "to either degrees Celsius (centigrade) or " \
                     "Fahrenheit... \n\n" \
                     "Note that -273 degrees C " \
                     "(-459 F) is absolute zero (the coldest possible " \
                     "temperature). If you try to convert a " \
                     "temperature that is less than -273 degrees C, " \
                     "you will get an error message. \n\n" \
                     "To see your " \
                     "calculation history and export it to a text " \
                     "file, please click the 'History / Export' button. "

        self.hints_text_label = Label(self.hints_frame,
                                      text=hints_text, wraplength=350,
                                      justify="left")
        self.hints_text_label.grid(row=1, padx=10)

        self.dismiss_button = Button(self.hints_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Dismiss", bg="#CC6600",
                                     fg="#FFFFFF",
                                     command=partial(self.close_hints, partner))
        self.dismiss_button.grid(row=2, padx=10, pady=10)

        # List and loop to set background colour on everything except the buttons
        recolour_list = [self.hints_frame, self.hints_heading_label, self.hints_text_label]

        for item in recolour_list:
            item.config(bg=background)

    def close_hints(self, partner):
        """
        Closes hints dialogue box (and enables hints button)
        """
        # Put hints button back to normal...
        partner.hints_button.config(state=NORMAL)
        self.hints_box.destroy()
    # def to_hints(self):
    #