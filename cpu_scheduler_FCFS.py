import matplotlib.pyplot as plt
def input_proxy():
    works = []
    num_processes = int(input("Enter the number of processes: "))
    for i in range(num_processes):
        Arrivaltime = int(input(f"enter arrival time for process {i+1}:"))
        burst_time = int(input(f"enter burst time for process {i+1}:"))
        priority = int(input(f"enter priority for process {i+1}:"))
        works.append({
            "Id": i + 1,
            "Arrivaltime": Arrivaltime,
            "burst_time": burst_time,
            "priority": priority
        })
    return works

def plot_gantt(works):
    fig, ax = plt.subplots()  
    for i, process in enumerate(works):
        ax.barh(i, process["burst_time"], left=process["starttime"], height=0.5, label=f"P{process['Id']}")
    ax.set_xlabel("Time")
    ax.set_ylabel("Processes")
    ax.set_title("Gantt Chart (FCFS)")
    ax.legend()  
    plt.show() 
works = [
    {"Id": 1, "Arrivaltime": 0, "burst_time": 5, "starttime": 0},
    {"Id": 2, "Arrivaltime": 1, "burst_time": 3, "starttime": 5},
    {"Id": 3, "Arrivaltime": 2, "burst_time": 8, "starttime": 8}
]
