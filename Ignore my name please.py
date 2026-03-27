#Horribly made bru epick

import sys
import time
import subprocess

REQUIRED_MODULES = [
    "colorama",
]

INTERVAL_SECONDS = 0.08
MAX_ITERATIONS = 100000000000000000 #Im a lazy idiito

TARGET_PROCESSES = [
    "StudentKeeper.exe",
    "WatchDog.exe",
    "StudentGuardian.exe",
    "ClassManager.exe",
]

def ensure_dependencies():
    missing = []
    for mod in REQUIRED_MODULES:
        try:
            __import__(mod)
        except ImportError:
            missing.append(mod)
    if not missing:
        return

    print("Installing missing dependencies:", ", ".join(missing))
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-U", *missing],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        print("Dependencies installed. Restarting is recommended; retrying imports now...")
        # Try again after install
        for mod in missing:
            __import__(mod)
    except subprocess.CalledProcessError as e:
        print(f"Failed to install dependencies: {e}")
        sys.exit(2)


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


def run_kill_loop(dry_run: bool, confirm_flag: bool):
    iterations = 0
    kill_count = 0
    print(
        f"Process monitor {'(DRY RUN)' if dry_run else ''} started; targets: {', '.join(TARGET_PROCESSES)}",
        file=sys.stderr,
    )

    while iterations < MAX_ITERATIONS:
        iterations += 1
        attempted = 0
        killed = 0

        for name in TARGET_PROCESSES:
            for pid in get_all_pids(name):
                attempted += 1
                if dry_run:
                    print(f"[DRY] Would attempt to kill {name} PID {pid}", file=sys.stderr)
                else:
                    if confirm_flag:
                        if kill_pid(pid):
                            killed += 1
                            kill_count += 1
                        else:
                            print(f"Failed to kill PID {pid}", file=sys.stderr)
                    else:
                        print(
                            f"Refusing automated kill for PID {pid} unless --confirm is used",
                            file=sys.stderr,
                        )

        if attempted > 0:
            print(
                f"[iter {iterations}] scanned {attempted} match(es) -> killed {killed}",
                file=sys.stderr,
            )

        time.sleep(INTERVAL_SECONDS)


def show_menu():
    from colorama import init, Fore, Style
    init(autoreset=True)

    while True:
        print()
        print(Fore.CYAN + "=== StudentKeeper Killer ===" + Style.RESET_ALL)
        print("1. Scan only (dry run) — no process termination")
        print("2. Enable monitoring with confirmation required (manual trigger via --confirm)")
        print("3. Show target processes")
        print("4. Exit")
        choice = input(Fore.YELLOW + "Choose an option: " + Style.RESET_ALL).strip()

        if choice == "1":
            run_kill_loop(dry_run=True, confirm_flag=False)
            break
        elif choice == "2":
            print(
                Fore.RED + "\nWARNING: automatic termination can impact the system (but probibally wont)."
                + Style.RESET_ALL
            )
            confirm_arg = input("Type 'Epick' if you really intend to allow killing: ").strip()
            if confirm_arg == "Epick":
                run_kill_loop(dry_run=False, confirm_flag=True)
                break
            else:
                print("Canceled. Staying safe; no processes killed.")
        elif choice == "3":
            print("WOW its really working!!1")
        elif choice == "4":
            sys.exit(0)
        else:
            print(Fore.RED + "Invalid choice." + Style.RESET_ALL)


def main():
    ensure_dependencies()

    if len(sys.argv) > 1 and sys.argv[1] == "--headless":
        dry = not ("--confirm" in sys.argv)
        run_kill_loop(dry_run=dry, confirm_flag=bool("--confirm" in sys.argv))
    else:
        show_menu()


if __name__ == "__main__":
    main()
