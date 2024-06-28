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

def hrrn_scheduling(processes):
    current_time = 0
    gantt_chart = []
    completed_processes = []
    
    while processes:
        # 도착한 프로세스를 선택
        ready_queue = [p for p in processes if p.arrival_time <= current_time]
        if not ready_queue:
            current_time += 1
            continue
        
        # 응답 비율 계산
        for process in ready_queue:
            waiting_time = current_time - process.arrival_time
            process.response_ratio = (waiting_time + process.burst_time) / process.burst_time

        # 응답 비율이 가장 높은 프로세스를 선택
        process = max(ready_queue, key=lambda x: x.response_ratio)
        
        if process.start_time == -1:
            process.start_time = current_time
        if process.response_time == -1:
            process.response_time = current_time - process.arrival_time

        current_time += process.burst_time
        process.finish_time = current_time
        process.turnaround_time = process.finish_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time
        
        gantt_chart.append((process.pid, process.start_time, process.finish_time))
        completed_processes.append(process)
        processes.remove(process)
    
    return gantt_chart, completed_processes

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
        gantt_chart, finished_processes = hrrn_scheduling(processes)
        avg_waiting_time, avg_turnaround_time, avg_response_time = calculate_averages(finished_processes)
        print_results(finished_processes, gantt_chart, avg_waiting_time, avg_turnaround_time, avg_response_time)
    else:
        print("프로세스가 없습니다.")
