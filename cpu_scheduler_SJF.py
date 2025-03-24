import matplotlib.pyplot as plt
def input_processes():
    processes = []
    num_processes = int(input("Enter the number of processes: "))

    for i in range(num_processes):

        arrival_time = int(input(f"Enter arrival time for process {i+1}: "))

        burst_time = int(input(f"Enter burst time for process {i+1}: "))

        processes.append({

            "id": i + 1,

            "arrival_time": arrival_time,

            "burst_time": burst_time

        })
