import subprocess
import os
import getpass


def process_count(username: str) -> int:
    cmd = f"ps -u {username} --no-headers | wc -l"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return int(result.stdout.strip())


def total_memory_usage(root_pid: int) -> float:
    """Суммарное потребление памяти древа процессов"""
    cmd = f"ps --ppid {root_pid} -o %mem= | awk '{{s+=$1}} END {{print s}}'"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return float(result.stdout.strip() or 0)


if __name__ == "__main__":
    username = getpass.getuser()
    print(f"Пользователь: {username}")
    print(f"Количество процессов: {process_count(username)}")
    
    my_pid = os.getpid()
    print(f"Текущий PID: {my_pid}")
    print(f"Потребление памяти древа: {total_memory_usage(my_pid)}%")