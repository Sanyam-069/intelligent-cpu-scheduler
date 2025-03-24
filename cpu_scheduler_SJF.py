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
return processes

def sjf(processes):

    processes.sort(key=lambda x: (x["arrival_time"], x["burst_time"]))  

    current_time = 0
    scheduled_processes = []

    while processes:

        ready_processes = [p for p in processes if p["arrival_time"] <= current_time]
        if not ready_processes:
            current_time += 1
            continue

        shortest_process = min(ready_processes, key=lambda x: x["burst_time"])
        processes.remove(shortest_process)
        shortest_process["start_time"] = current_time
        shortest_process["end_time"] = current_time + shortest_process["burst_time"]
        shortest_process["waiting_time"] = shortest_process["start_time"] - shortest_process["arrival_time"]
        shortest_process["turnaround_time"] = shortest_process["end_time"] - shortest_process["arrival_time"]
        current_time = shortest_process["end_time"]
        scheduled_processes.append(shortest_process)

    return scheduled_processes
def plot_gantt(processes):

    fig, ax = plt.subplots()

    for i, process in enumerate(processes):

        ax.barh(i, process["burst_time"], left=process["start_time"], height=0.5, label=f"P{process['id']}")

    ax.set_xlabel("Time")
    ax.set_ylabel("Processes")
    ax.set_title("Gantt Chart (SJF)")
    ax.legend()
    plt.show()

if __name__ == "__main__":

    processes = input_processes()
    scheduled_processes = sjf(processes)
    print("Scheduled Processes (SJF):")
    for process in scheduled_processes:
        print(f"Process {process['id']}: Start Time = {process['start_time']}, End Time = {process['end_time']}, "
              f"Waiting Time = {process['waiting_time']}, Turnaround Time = {process['turnaround_time']}")

    plot_gantt(scheduled_processes)
