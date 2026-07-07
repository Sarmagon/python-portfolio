import threading
import time
import requests
from queue import PriorityQueue


def worker(thread_id: int, log_queue: PriorityQueue) -> None:
    for _ in range(20):
        timestamp = time.time()
        try:
            response = requests.get(f"http://127.0.0.1:8080/timestamp/{timestamp}")
            date_str = response.text
            log_queue.put((timestamp, f"{timestamp} {date_str}"))
        except Exception as e:
            print(f"Ошибка в потоке {thread_id}: {e}")
        time.sleep(1)


def writer(log_queue: PriorityQueue, output_file: str) -> None:
    with open(output_file, 'w', encoding='utf-8') as f:
        while True:
            try:
                timestamp, log_line = log_queue.get(timeout=1)
                f.write(log_line + '\n')
                f.flush()
                log_queue.task_done()
            except:
                break


def main() -> None:
    log_queue = PriorityQueue()
    output_file = "logs.txt"
    
    writer_thread = threading.Thread(target=writer, args=(log_queue, output_file))
    writer_thread.start()
    
    threads = []
    for i in range(10):
        t = threading.Thread(target=worker, args=(i, log_queue))
        threads.append(t)
        t.start()
        time.sleep(1)
    
    for t in threads:
        t.join()
    
    log_queue.join()
    time.sleep(0.5)
    
    print(f"Логи записаны в {output_file}")


if __name__ == "__main__":
    main()