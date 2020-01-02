# Metronome - Johnathon Kwisses (Kwistech)
from tkinter import *
from winsound import Beep


class Metronome:
    """Create Metronome app with class instance."""

    def __init__(self, root):
        """Initiate default values for class and call interface().

        Args:
            root (tkinter.Tk): Main class instance for tkinter.
            beats (list): Contains time signatures for metronome.
        """
        self.root = root

        self.start = False
        self.steps = 0
        self.bpm = 0
        self.end_bpm = 0
        self.count = 0
        self.beat = 0
        self.time = 0
        self.cumulative_time = 0
        self.bpm_scale = 0
        self.time_step = 0

        self.var_bpm = StringVar()
        self.var_bpm.set(self.bpm)

        self.interface()

    def interface(self):
        """Set interface for Metronome app."""
        frame = Frame()
        frame.pack()

        # START TEMPO ENTRY
        self.entry_bpm_start = Entry(frame, width=6, justify="center")
        self.entry_bpm_start.insert(0, "60")
        self.entry_bpm_start.grid(row=0, column=0, padx=5, sticky="E")

        # END TEMPO ENTRY
        self.entry_bpm_end = Entry(frame, width=8, justify="center")
        self.entry_bpm_end.insert(0, "120")
        self.entry_bpm_end.grid(row=0, column=1, padx=5, sticky="E")

        # TRAINING TIME ENTRY
        self.entry_time = Entry(frame, width=8, justify="center")
        self.entry_time.insert(0, "60")
        self.entry_time.grid(row=1, column=0, padx=5, sticky="E")

        # STEPS ENTRY
        self.entry_steps = Entry(frame, width=8, justify="center")
        self.entry_steps.insert(0, "10")
        self.entry_steps.grid(row=1, column=1, padx=5, sticky="E")

        # BMP START LABEL
        self.label_bpm_start = Label(frame, text="BPM START:")
        self.label_bpm_start.grid(row=0, column=0, sticky="W")

        # BMP END LABEL
        self.label_bpm_end = Label(frame, text="BPM END:")
        self.label_bpm_end.grid(row=0, column=1, sticky="W")

        # TIME LABEL
        self.label_time = Label(frame, text="STEP TIME:")
        self.label_time.grid(row=1, column=0, sticky="W")

        # STEPS LABEL
        self.label_steps = Label(frame, text="STEPS:")
        self.label_steps.grid(row=1, column=1, sticky="W")


        self.label_count = Label(frame, textvariable=self.var_bpm, font=("Arial", 30))
        self.label_count.grid(row=3, column=0, columnspan=1)

        self.button_start = Button(frame, text="Start", width=10, height=2,
                              command=lambda: self.start_counter())
        self.button_start.grid(row=2, column=0, padx=10, sticky="W")

        self.button_stop = Button(frame, text="Stop", width=10, height=2,
                             command=lambda: self.stop_counter())
        self.button_stop.grid(row=2, column=1, padx=10, sticky="E")

    def start_counter(self):
        """Start counter if self.start is False (prevents multiple starts).

        Args:
            entry (tkinter.Entry): tkinter Entry widget for app.
            spinbox (tkinter.Spinbox): tkinter Spinbox widget for app.

        Raises:
            ValueError: if bpm field (self.bpm) on tkinter app is left blank.
        """
        if not self.start:
            try:
                self.bpm = int(self.entry_bpm_start.get())
            except ValueError:
                self.bpm = 60
            else:
                if self.bpm > 300:  # Limits BPM
                    self.bpm = 300

            try:
                self.time_step = int(self.entry_time.get())
            except ValueError:
                self.time_step = 60

            try:
                self.steps = int(self.entry_steps.get())
            except ValueError:
                self.steps = 10

            try:
                self.end_bpm = int(self.entry_bpm_end.get())
            except ValueError:
                self.time_step = 120

            # compute scale factor
            self.bpm_scale = pow(self.end_bpm / self.bpm, 1 / (self.steps - 1))

            self.cumulative_time = 0
            self.start = True
            self.counter()

    def stop_counter(self):
        """Stop counter by setting self.start to False."""
        self.start = False

    def counter(self):
        """Control counter display and audio with calculated time delay.

        Args:
            spinbox (tkinter.Spinbox): tkinter Spinbox widget to get beat.
        """
        if self.start:

            if self.cumulative_time > self.time_step * 1000: # as time_setp is in [s], and cumulative_time in [ms]
                self.bpm = self.bpm * self.bpm_scale
                self.cumulative_time = 0

                epsilon = 0.1 # to prevent from not playing final step
                if self.bpm > self.end_bpm + epsilon:
                    self.stop_counter()

            self.var_bpm.set( float("{0:.1f}".format(self.bpm)))
            self.time = int((60 / self.bpm - 0.1) * 1000)  # Math for delay
            self.cumulative_time = self.cumulative_time + self.time
            Beep(440, 100)


            # Calls this method after a certain amount of time (self.time).
            self.root.after(self.time, lambda: self.counter())


def main():
    """Call Metronome class instance with tkinter root class settings."""
    root = Tk()
    root.title("Metronome")

    Metronome(root)

    root.mainloop()

if __name__ == "__main__":
    main()
