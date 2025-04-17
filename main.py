# main.py
# Main script to launch the CPU Scheduler Simulator GUI.

import tkinter as tk
from gui import SchedulerGUI # Assuming gui.py is in the same directory

if __name__ == "__main__":
    # Create the main application window
    root = tk.Tk()

    # Instantiate the GUI class, passing the root window
    app = SchedulerGUI(root)

    # Start the Tkinter event loop
    root.mainloop()

