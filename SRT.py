class Process:
    def __init__(self, pid, arrival_time, burst_time, priority, time_quantum):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.priority = priority
        self.time_quantum = time_quantum
        self.start_time = -1
        self.finish_time = -1
        self.waiting_time = 0
        self.turnaround_time = 0
        self.response_time = -1

def read_processes(file_name):
    process_file = open(file_name, "r", encoding="utf-8")
    lines = process_file.readlines()
    num_processes = int(lines[0].strip())
    processes = []
    for line in lines[1:num_processes + 1]:
        pid, arrival_time, burst_time, priority, time_quantum = map(int, line.split())
        processes.append(Process(pid, arrival_time, burst_time, priority, time_quantum))
    return processes

def srt_scheduling(processes):
    current_time = 0
    gantt_chart = []
    ready_queue = []
    remaining_processes = processes[:]
    
    while remaining_processes or ready_queue:
        while remaining_processes and remaining_processes[0].arrival_time <= current_time:
            ready_queue.append(remaining_processes.pop(0))

        ready_queue.sort(key=lambda x: x.remaining_time)
        
        if ready_queue:
            process = ready_queue.pop(0)
            if process.start_time == -1:
                process.start_time = current_time
            if process.response_time == -1:
                process.response_time = current_time - process.arrival_time

            current_time += 1
            process.remaining_time -= 1
            
            gantt_chart.append((process.pid, current_time - 1, current_time))
            
            if process.remaining_time > 0:
                while remaining_processes and remaining_processes[0].arrival_time <= current_time:
                    ready_queue.append(remaining_processes.pop(0))
                ready_queue.append(process)
            else:
                process.finish_time = current_time
                process.turnaround_time = process.finish_time - process.arrival_time
                process.waiting_time = process.turnaround_time - process.burst_time
        else:
            current_time += 1
    
    return gantt_chart, processes

def print_gantt_chart(gantt_chart):
    print("간트 차트 =>")
    chart_str = "|"
    for pid, start, finish in gantt_chart:
        chart_str += f" P{pid} ({start} -> {finish}) |"
    print(chart_str)

def calculate_averages(processes):
    total_waiting_time = sum(p.waiting_time for p in processes)
    total_turnaround_time = sum(p.turnaround_time for p in processes)
    total_response_time = sum(p.response_time for p in processes)
    n = len(processes)
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
        gantt_chart, finished_processes = srt_scheduling(processes)
        avg_waiting_time, avg_turnaround_time, avg_response_time = calculate_averages(finished_processes)
        print_results(finished_processes, gantt_chart, avg_waiting_time, avg_turnaround_time, avg_response_time)
    else:
        print("프로세스가 없습니다.")
