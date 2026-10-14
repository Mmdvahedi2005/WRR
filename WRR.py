import subprocess
import time
import psutil

processes = []

number = int(input("Number of programs: "))
quantum = float(input("Time quantum (seconds): "))

if number <= 0 or quantum <= 0:
    raise ValueError("Number and quantum must be positive")

for i in range(number):
    path = input(f"Program {i + 1} path: ")
    weight = int(input(f"Program {i + 1} weight: "))

    if weight <= 0:
        raise ValueError("Weight must be positive")

    processes.append({
        "name": f"P{i + 1}",
        "path": path,
        "weight": weight,
        "process": None,
        "monitor": None,
        "cpu_time": 0.0,
        "runtime": 0.0,
        "finished": False
    })

try:
    for p in processes:
        p["start"] = time.perf_counter()
        p["process"] = subprocess.Popen([p["path"]])
        p["monitor"] = psutil.Process(p["process"].pid)
        p["monitor"].suspend()

    while any(not p["finished"] for p in processes):
        for p in processes:
            if p["finished"]:
                continue

            for _ in range(p["weight"]):
                if p["process"].poll() is not None:
                    p["finished"] = True
                    break

                try:
                    before = p["monitor"].cpu_times()
                    p["monitor"].resume()

                    try:
                        p["process"].wait(timeout=quantum)
                        p["finished"] = True
                    except subprocess.TimeoutExpired:
                        p["monitor"].suspend()

                    after = p["monitor"].cpu_times()
                    p["cpu_time"] += (
                        after.user + after.system
                        - before.user - before.system
                    )

                    if p["finished"]:
                        p["runtime"] = time.perf_counter() - p["start"]
                        print(p["name"], "finished")
                        break

                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    p["finished"] = p["process"].poll() is not None
                    break

finally:
    for p in processes:
        process = p["process"]
        monitor = p["monitor"]

        if process is not None and process.poll() is None:
            try:
                if monitor is not None and monitor.is_running():
                    monitor.resume()
                process.terminate()
                process.wait(timeout=2)
            except (psutil.NoSuchProcess, psutil.AccessDenied, subprocess.TimeoutExpired):
                process.kill()

print("\nResults")
print("Program\tWeight\tCPU Time\tRuntime\tReturn Code")

for p in processes:
    if p["process"] is not None:
        print(
            f'{p["name"]}\t{p["weight"]}\t'
            f'{p["cpu_time"]:.3f}\t\t'
            f'{p["runtime"]:.3f}\t'
            f'{p["process"].returncode}'
        )
