# process.py
# Defines the Process class to hold attributes for each process.

class Process:
    """
    Represents a process with its scheduling attributes.
    """
    def __init__(self, p_id, arrival_time, burst_time, priority=0):
        """
        Initializes a Process object.

        Args:
            p_id (int): Unique Process ID.
            arrival_time (int): Time at which the process arrives in the ready queue.
            burst_time (int): Total CPU time required by the process.
            priority (int): Priority of the process (lower number means higher priority). Defaults to 0.
        """
        self.p_id = p_id
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority

        # Attributes calculated during simulation
        self.remaining_burst_time = burst_time # For preemptive or RR algorithms
        self.start_time = -1          # Time when the process first gets the CPU
        self.completion_time = -1      # Time when the process finishes execution
        self.waiting_time = -1          # Time spent waiting in the ready queue
        self.turnaround_time = -1      # Time from arrival to completion

    def calculate_metrics(self):
        """
        Calculates waiting time and turnaround time after completion time is set.
        Note: For preemptive algorithms like RR, waiting time calculation might
        need adjustment if done incrementally. This calculates based on final times.
        """
        if self.completion_time != -1:
            self.turnaround_time = self.completion_time - self.arrival_time
            # Waiting time = Turnaround Time - Burst Time
            # This formula works for both non-preemptive and preemptive algorithms
            # when calculated *after* the process completes.
            self.waiting_time = self.turnaround_time - self.burst_time
            # Ensure waiting time isn't negative due to potential float inaccuracies or logic errors
            if self.waiting_time < 0:
                # This might happen if start_time logic in RR is slightly off, let's clamp it
                # print(f"Warning: Negative waiting time calculated for P{self.p_id}. Clamping to 0.")
                self.waiting_time = 0

        else:
            # Should not happen if calculation is called correctly after completion
            print(f"Warning: Completion time not set for Process {self.p_id} during metric calculation.")
            self.waiting_time = -1
            self.turnaround_time = -1

    def __repr__(self):
        """
        String representation for easy printing and debugging.
        """
        return (f"Process(ID={self.p_id}, Arrival={self.arrival_time}, "
                f"Burst={self.burst_time}, Priority={self.priority}, "
                f"RemBurst={self.remaining_burst_time}, Start={self.start_time}, "
                f"Completion={self.completion_time}, Waiting={self.waiting_time}, "
                f"Turnaround={self.turnaround_time})")
