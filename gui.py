# gui.py
# Implements the Tkinter GUI for the CPU Scheduler Simulator with a dark and modern look using sv-ttk.

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import random # For coloring Gantt chart bars
import sv_ttk

from process import Process
import scheduler # Assuming scheduler.py is in the same directory

class SchedulerGUI:
    """
    Manages the Tkinter GUI for the CPU Scheduler Simulator with a dark theme using sv-ttk.
    """
    def __init__(self, master):
        """
        Initializes the GUI with a dark theme using sv-ttk.

        Args:
            master: The root Tkinter window.
        """
        self.master = master
        self.master.title("CPU Scheduler Simulator")
        self.master.geometry("950x800") # Slightly larger for better spacing

        # --- Dark Theme Configuration using sv-ttk ---
        sv_ttk.set_theme("dark")

        self.processes = []
        self.process_id_counter = 1
        self.time_quantum = tk.IntVar(value=2) # Default time quantum for RR

        # --- Main Frame for Padding ---
        main_frame = ttk.Frame(self.master, padding=(15, 15))
        main_frame.pack(fill="both", expand=True)

        # --- Input Frame ---
        input_frame = ttk.LabelFrame(main_frame, text="Process Input", padding=(10, 8))
        input_frame.pack(pady=(0, 10), padx=10, fill="x")

        ttk.Label(input_frame, text="Arrival Time:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.arrival_entry = ttk.Entry(input_frame, width=10)
        self.arrival_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Burst Time:").grid(row=0, column=2, padx=10, pady=5, sticky="w")
        self.burst_entry = ttk.Entry(input_frame, width=10)
        self.burst_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(input_frame, text="Priority (Optional):").grid(row=0, column=4, padx=10, pady=5, sticky="w")
        self.priority_entry = ttk.Entry(input_frame, width=10)
        self.priority_entry.grid(row=0, column=5, padx=5, pady=5)
        self.priority_entry.insert(0, "0") # Default priority

        add_button = ttk.Button(input_frame, text="Add Process", command=self.add_process)
        add_button.grid(row=0, column=6, padx=10, pady=5)

        clear_button = ttk.Button(input_frame, text="Clear All", command=self.clear_processes)
        clear_button.grid(row=0, column=7, padx=5, pady=5)

        # --- Process List Frame ---
        list_frame = ttk.LabelFrame(main_frame, text="Process List", padding=(10, 8))
        list_frame.pack(pady=(0, 10), padx=10, fill="x")

        self.tree = ttk.Treeview(list_frame, columns=("ID", "Arrival", "Burst", "Priority"), show="headings", height=5)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Arrival", text="Arrival Time")
        self.tree.heading("Burst", text="Burst Time")
        self.tree.heading("Priority", text="Priority")
        self.tree.column("ID", width=60, anchor=tk.CENTER)
        self.tree.column("Arrival", width=120, anchor=tk.CENTER)
        self.tree.column("Burst", width=120, anchor=tk.CENTER)
        self.tree.column("Priority", width=120, anchor=tk.CENTER)
        self.tree.pack(fill="x", expand=True)

        # --- Simulation Control Frame ---
        control_frame = ttk.LabelFrame(main_frame, text="Simulation Controls", padding=(10, 8))
        control_frame.pack(pady=(0, 15), padx=10, fill="x")

        ttk.Label(control_frame, text="Time Quantum (RR):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.quantum_entry = ttk.Entry(control_frame, textvariable=self.time_quantum, width=5)
        self.quantum_entry.grid(row=0, column=1, padx=5, pady=5)

        fcfs_button = ttk.Button(control_frame, text="FCFS", command=lambda: self.run_simulation('fcfs'))
        fcfs_button.grid(row=0, column=2, padx=10, pady=5)

        sjf_button = ttk.Button(control_frame, text="SJF", command=lambda: self.run_simulation('sjf'))
        sjf_button.grid(row=0, column=3, padx=10, pady=5)

        priority_button = ttk.Button(control_frame, text="Priority", command=lambda: self.run_simulation('priority'))
        priority_button.grid(row=0, column=4, padx=10, pady=5)

        rr_button = ttk.Button(control_frame, text="Round Robin", command=lambda: self.run_simulation('rr'))
        rr_button.grid(row=0, column=5, padx=10, pady=5)

        # --- Results Frame ---
        results_frame = ttk.Frame(main_frame, padding=(10, 8))
        results_frame.pack(pady=(0, 10), padx=10, fill="both", expand=True)

        # Gantt Chart Area
        gantt_frame = ttk.LabelFrame(results_frame, text="Gantt Chart", padding=(10, 8))
        gantt_frame.pack(pady=(0, 10), fill="x")
        self.gantt_canvas = tk.Canvas(gantt_frame, bg='#333', height=120, scrollregion=(0, 0, 1000, 120), highlightthickness=0) # Dark background
        # Horizontal Scrollbar for Gantt Chart
        gantt_scrollbar_x = ttk.Scrollbar(gantt_frame, orient=tk.HORIZONTAL, command=self.gantt_canvas.xview)
        self.gantt_canvas.configure(xscrollcommand=gantt_scrollbar_x.set)
        gantt_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.gantt_canvas.pack(fill="x", expand=True)

        # Metrics and Table Area (Combined in a PanedWindow for resizing)
        paned_window = ttk.PanedWindow(results_frame, orient=tk.VERTICAL)
        paned_window.pack(pady=5, fill="both", expand=True)

        # Metrics Display Area
        metrics_frame = ttk.LabelFrame(paned_window, text="Performance Metrics", padding=(10, 8))
        paned_window.add(metrics_frame, weight=1) # Add to paned window

        self.metrics_label = ttk.Label(metrics_frame, text="Run a simulation to see metrics.", justify=tk.LEFT)
        self.metrics_label.pack(anchor="w", padx=5, pady=5)

        # Process Results Table Area
        table_frame = ttk.LabelFrame(paned_window, text="Process Results", padding=(10, 8))
        paned_window.add(table_frame, weight=3) # Add to paned window, give more weight

        self.results_tree = ttk.Treeview(table_frame, columns=("ID", "Arrival", "Burst", "Priority", "Start", "Completion", "Waiting", "Turnaround"), show="headings")
        self.results_tree.heading("ID", text="ID")
        self.results_tree.heading("Arrival", text="Arrival")
        self.results_tree.heading("Burst", text="Burst")
        self.results_tree.heading("Priority", text="Priority")
        self.results_tree.heading("Start", text="Start Time")
        self.results_tree.heading("Completion", text="Completion Time")
        self.results_tree.heading("Waiting", text="Waiting Time")
        self.results_tree.heading("Turnaround", text="Turnaround Time")

        # Set column widths appropriately
        for col in self.results_tree["columns"]:
            self.results_tree.column(col, width=110, anchor=tk.CENTER)

        # Vertical Scrollbar for Results Table
        results_scrollbar_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=results_scrollbar_y.set)

        results_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_tree.pack(fill="both", expand=True)

    def add_process(self):
        """Adds a process based on the input fields."""
        try:
            arrival = int(self.arrival_entry.get())
            burst = int(self.burst_entry.get())
            priority_str = self.priority_entry.get()
            priority = int(priority_str) if priority_str else 0 # Default priority if empty

            if arrival < 0 or burst <= 0 or priority < 0:
                messagebox.showerror("Input Error", "Arrival time and priority must be non-negative.\nBurst time must be positive.")
                return

            process = Process(self.process_id_counter, arrival, burst, priority)
            self.processes.append(process)
            self.process_id_counter += 1

            # Add to the list view (Treeview)
            self.tree.insert("", tk.END, values=(process.p_id, process.arrival_time, process.burst_time, process.priority))

            # Clear entry fields
            self.arrival_entry.delete(0, tk.END)
            self.burst_entry.delete(0, tk.END)
            self.priority_entry.delete(0, tk.END)
            self.priority_entry.insert(0, "0") # Reset default priority
            self.arrival_entry.focus() # Set focus back to arrival time

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid integer values for arrival time, burst time, and priority.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def clear_processes(self):
        """Clears all entered processes and resets the view."""
        if messagebox.askyesno("Confirm Clear", "Are you sure you want to remove all processes?"):
            self.processes = []
            self.process_id_counter = 1
            # Clear the input list treeview
            for item in self.tree.get_children():
                self.tree.delete(item)
            # Clear results as well
            self.clear_results()

    def clear_results(self):
        """Clears the results area (Gantt, metrics, table)."""
        self.gantt_canvas.delete("all")
        self.gantt_canvas.configure(scrollregion=(0, 0, 1000, 120)) # Reset scroll region
        self.metrics_label.config(text="Run a simulation to see metrics.")
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)


    def run_simulation(self, algorithm_name):
        """Runs the selected scheduling algorithm."""
        if not self.processes:
            messagebox.showwarning("No Processes", "Please add processes before running a simulation.")
            return

        # Clear previous results
        self.clear_results()

        try:
            gantt_chart = []
            avg_waiting = 0.0
            avg_turnaround = 0.0
            completed_procs = []

            if algorithm_name == 'fcfs':
                gantt_chart, avg_waiting, avg_turnaround, completed_procs = scheduler.fcfs(self.processes)
            elif algorithm_name == 'sjf':
                gantt_chart, avg_waiting, avg_turnaround, completed_procs = scheduler.sjf(self.processes)
            elif algorithm_name == 'priority':
                gantt_chart, avg_waiting, avg_turnaround, completed_procs = scheduler.priority_scheduling(self.processes)
            elif algorithm_name == 'rr':
                try:
                    quantum = self.time_quantum.get()
                    if quantum <= 0:
                        messagebox.showerror("Input Error", "Time quantum for Round Robin must be a positive integer.")
                        return
                    gantt_chart, avg_waiting, avg_turnaround, completed_procs = scheduler.round_robin(self.processes, quantum)
                except ValueError:
                    messagebox.showerror("Input Error", "Please enter a valid integer for the time quantum.")
                    return


            # --- Display Results ---
            # Update Metrics Label
            metrics_text = (f"Algorithm: {algorithm_name.upper()}\n"
                            f"Average Waiting Time: {avg_waiting:.2f}\n"
                            f"Average Turnaround Time: {avg_turnaround:.2f}")
            if algorithm_name == 'rr':
                metrics_text += f"\nTime Quantum: {self.time_quantum.get()}"
            self.metrics_label.config(text=metrics_text)

            # Populate Results Table
            for proc in completed_procs:
                self.results_tree.insert("", tk.END, values=(
                    proc.p_id, proc.arrival_time, proc.burst_time, proc.priority,
                    proc.start_time, proc.completion_time,
                    proc.waiting_time, proc.turnaround_time
                ))

            # Draw Gantt Chart
            self.draw_gantt_chart(gantt_chart)

        except Exception as e:
            messagebox.showerror("Simulation Error", f"An error occurred during simulation: {e}")
            import traceback
            traceback.print_exc() # Print detailed traceback to console for debugging


    def draw_gantt_chart(self, gantt_chart):
        """Draws the Gantt chart on the canvas."""
        self.gantt_canvas.delete("all")
        if not gantt_chart:
            return

        # Define colors for processes (can add more if needed)
        colors = ["#80CBC4", "#A1887F", "#FFD54F", "#64B5F6", "#E64A19", "#4DB6AC", "#7986CB", "#D4E157", "#F4511E"] # More modern color palette
        process_colors = {}
        color_index = 0

        # Constants for drawing
        bar_height = 40
        y_pos = 40
        padding = 10
        time_label_y = y_pos + bar_height + 15
        pid_label_y = y_pos + bar_height / 2

        # Determine scale
        max_time = gantt_chart[-1][2] if gantt_chart else 1
        # Add some buffer to the max time for better visualization
        canvas_width_target = max(1000, max_time * 20) # Adjust multiplier for desired density
        self.gantt_canvas.configure(scrollregion=(0, 0, canvas_width_target + 50, 150)) # Update scroll region

        scale_factor = canvas_width_target / max_time if max_time > 0 else 1

        current_x = padding

        for entry in gantt_chart:
            p_id, start_time, end_time = entry
            duration = end_time - start_time
            if duration <= 0: continue # Skip zero-duration entries

            bar_width = duration * scale_factor

            # Assign color
            if p_id != "Idle":
                if p_id not in process_colors:
                    process_colors[p_id] = colors[color_index % len(colors)]
                    color_index += 1
                fill_color = process_colors[p_id]
                outline_color = "#222" # Darker outline
                pid_text = f"P{p_id}"
            else:
                fill_color = "#555" # Darker grey for idle
                outline_color = "#444"
                pid_text = "Idle"

            # Draw rectangle
            self.gantt_canvas.create_rectangle(
                current_x, y_pos, current_x + bar_width, y_pos + bar_height,
                fill=fill_color, outline=outline_color, width=1
            )

            # Draw Process ID text inside the bar (if space permits)
            text_x = current_x + bar_width / 2
            if bar_width > 25: # Adjust for readability
                self.gantt_canvas.create_text(text_x, pid_label_y, text=pid_text, anchor=tk.CENTER, font=('Helvetica', 10, 'bold'), fill="#eee") # Light text

            # Draw start time label below the bar
            self.gantt_canvas.create_text(current_x, time_label_y, text=str(start_time), anchor=tk.CENTER, font=('Helvetica', 9), fill="#ccc")

            current_x += bar_width

        # Draw final end time label
        self.gantt_canvas.create_text(current_x, time_label_y, text=str(max_time), anchor=tk.CENTER, font=('Helvetica', 9), fill="#ccc")

if __name__ == "__main__":
    # Create the main application window
    root = tk.Tk()

    # Instantiate the GUI class, passing the root window
    app = SchedulerGUI(root)

    # Start the Tkinter event loop
    root.mainloop()
