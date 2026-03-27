#very simple stuff here nothing much to see here LOL
import time
import subprocess
import sys

INTERVAL_SECONDS = 0.08
MAX_KILLS = 10000000000000

TARGET_PROCESSES = [
    "StudentKeeper.exe",
    "WatchDog.exe",
    "StudentGuardian.exe",
    "ClassManager.exe"
]

def get_all_pids(process_name):
    try:
        txt = subprocess.check_output(
            f'tasklist /fi "imagename eq {process_name}" /nh /fo csv',
            creationflags=subprocess.CREATE_NO_WINDOW,
            encoding='utf-8',
            errors='replace',
            timeout=2
        )
    except subprocess.CalledProcessError:
        return []

    pids = []
    for line in txt.splitlines():
        line = line.strip()
        if not line or "No tasks" in line:
            continue
        parts = line.split('","')
        if len(parts) >= 2:
            try:
                pids.append(int(parts[1].strip('"')))
            except ValueError:
                pass

    return pids

def kill_pid(pid):
    try:
        subprocess.run(
            f'taskkill /f /pid {pid}',
            creationflags=subprocess.CREATE_NO_WINDOW,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=1
        )
        return True
    except:
        return False

def main():
    kill_count = 0
    print(f"StudentKeeper killer running", file=sys.stderr)

    while kill_count < MAX_KILLS:
        killed = 0

        for process in TARGET_PROCESSES:
            for pid in get_all_pids(process):
                if kill_pid(pid):
                    kill_count += 1
                    killed += 1

        if killed > 0:
            print(f"[{kill_count}] Killed {killed} process(es)", file=sys.stderr)

        time.sleep(INTERVAL_SECONDS)


if __name__ == '__main__':
    try:
        import ctypes
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        if hwnd != 0:
            ctypes.windll.user32.ShowWindow(hwnd, 0)
    except:
        pass

    main()
