class Process:
    def __init__(self, pid, arrival_time, burst_time, priority, time_quantum):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.time_quantum = time_quantum
        self.start_time = -1
        self.finish_time = -1
        self.waiting_time = 0
        self.turnaround_time = 0
        self.response_time = 0

def read_processes(file_name):
    process_file = open(file_name, "r", encoding="utf-8")
    lines = process_file.readlines()
    num_processes = int(lines[0].strip())
    processes = []
    for line in lines[1:num_processes+1]:
        pid, arrival_time, burst_time, priority, time_quantum = map(int, line.split())
        processes.append(Process(pid, arrival_time, burst_time, priority, time_quantum))
    process_file.close()
    return processes

def sjf_scheduling(processes):
    processes.sort(key=lambda x: (x.arrival_time, x.burst_time))
    current_time = 0
    gantt_chart = []
    ready_queue = []
    finished_processes = []

    while processes or ready_queue:
        while processes and processes[0].arrival_time <= current_time:
            ready_queue.append(processes.pop(0))
        ready_queue.sort(key=lambda x: x.burst_time)
        
        if ready_queue:
            process = ready_queue.pop(0)
            if current_time < process.arrival_time:
                current_time = process.arrival_time
            process.start_time = current_time
            process.finish_time = process.start_time + process.burst_time
            process.turnaround_time = process.finish_time - process.arrival_time
            process.waiting_time = process.start_time - process.arrival_time
            process.response_time = process.waiting_time

            gantt_chart.append((process.pid, process.start_time, process.finish_time))
            current_time = process.finish_time
            finished_processes.append(process)
        else:
            current_time += 1
    
    return gantt_chart, finished_processes

def print_gantt_chart(gantt_chart):
    print("간트 차트 =>")
    chart_str = "|"
    for pid, start, finish in gantt_chart:
        chart_str += f" P{pid} ({start} -> {finish}) |"
    print(chart_str)

def calculate_averages(processes):
    n = len(processes)
    if n == 0:
        return (0, 0, 0)
    total_waiting_time = sum(p.waiting_time for p in processes)
    total_turnaround_time = sum(p.turnaround_time for p in processes)
    total_response_time = sum(p.response_time for p in processes)
    return (total_waiting_time / n, total_turnaround_time / n, total_response_time / n)

def print_results(processes, gantt_chart, avg_waiting_time, avg_turnaround_time, avg_response_time):
    print_gantt_chart(gantt_chart)
    print("\n프로세스 상세 정보 =>")
    for process in processes:
        print(f"PID: {process.pid} | 도착 시간: {process.arrival_time} | 실행 시간: {process.burst_time} | "
              f"대기 시간: {process.waiting_time} | 반환 시간: {process.turnaround_time} | "
              f"응답 시간: {process.response_time}")

    print("\n")
    print(f"평균 대기 시간: {avg_waiting_time:.2f}")
    print(f"평균 반환 시간: {avg_turnaround_time:.2f}")
    print(f"평균 응답 시간: {avg_response_time:.2f}")

if __name__ == "__main__":
    processes = read_processes("process.txt")
    if processes:
        gantt_chart, finished_processes = sjf_scheduling(processes)
        avg_waiting_time, avg_turnaround_time, avg_response_time = calculate_averages(finished_processes)
        print_results(finished_processes, gantt_chart, avg_waiting_time, avg_turnaround_time, avg_response_time)
    else:
        print("프로세스가 없습니다.")
