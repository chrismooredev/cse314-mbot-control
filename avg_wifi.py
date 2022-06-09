
import time
import statistics

def get_rssis():
    with open('/proc/net/wireless', 'r') as f:
        # skip headers
        next(f)
        next(f)
        iflvls = dict()
        for iface_line in f:
            iface, status, link, level, noise, *_rest = iface_line.split()
            iflvls[iface[:-1]] = int(level[:-1])
        return iflvls

def sample(times = 30, sleep = 0.1, iface="wlan0"):
    lvls = []
    for _ in range(times):
        lvls.append(get_rssis()[iface])
        time.sleep(sleep)

    return {
        "raw": lvls,
        "mean": statistics.mean(lvls),
        "stdev": statistics.stdev(lvls),
        "median": statistics.median(lvls),
        "mode": statistics.mode(lvls),
    }

if __name__ == "__main__":
    lis = []
    for _ in range(30):
        lis.append(get_rssis()["wlan0"])
        time.sleep(0.1)

    print(lis)
    print(f"mean: {statistics.mean(lis)} +/- {statistics.stdev(lis)}, median: {statistics.median(lis)}, mode: {statistics.mode(lis)}")

