from util import read
import numpy as np
from collections import defaultdict

def parseInfo(s):
    s = s[1:]
    datetime, info = s.split('] ')
    minute = int(datetime.split(':')[1])
    return minute, info

def parseGuardID(log):
    if '#' in log:
        ret = int(log.split('#')[1].split(' ')[0])
    else:
        ret = None
    return ret

def getGuardIDs(logs):
    gid = np.zeros(logs.shape)
    for j in range(logs.size):
        idno = parseGuardID(logs[j])
        if idno is not None:
            gid[j] = idno
        else:
            gid[j] = gid[j-1]
    gid = gid.astype(int)
    return gid

def getMinAndLogs(x):
    x = np.sort(x)
    info = [parseInfo(s) for s in x]
    minutes, logs = list(zip(*info))
    logs = np.array(logs)
    minutes = np.array(minutes)
    return minutes, logs


def countSleepiness(minutes, logs, gids):
    """
    df : DataFrame
    dttm                 log           gid    minute
    <datetime>           <str>         <int>  <int>
    1518-02-16 00:35:00  falls asleep  3557   35
    1518-02-16 00:38:00	 wakes up      3557   38
    1518-02-16 00:43:00	 falls asleep  3557   43
    1518-02-16 00:45:00  wakes up      3557   45
    1518-02-17 00:23:00  falls asleep  3457   23
    ...
    """
    total_minutes_asleep = defaultdict(int)
    minutes_asleep = {i: np.zeros(60) for i in gids}
    for j in range(len(logs)):
        minute, log, gid = minutes[j], logs[j], gids[j]
        if 'falls asleep' in log:
            mminute, llog, ggid = minutes[j+1], logs[j+1], gids[j+1]
            t0 = minute
            if ('wakes up' in llog) and (ggid == gid):
                t1 = mminute
            else:
                t1 = 60
            minutes_asleep[gid][t0:t1] += 1
            total_minutes_asleep[gid] += (t1 - t0)
    return minutes_asleep, total_minutes_asleep


def argmax(dd):
    vmax = np.max([v for v in dd.values()])
    amax = [k for k, v in dd.items() if v == vmax]
    if len(amax) == 1:
        amax = amax[0]
    return amax

def answer1(minutes, logs, gids):
    minutes_asleep, total_minutes_asleep = countSleepiness(minutes, logs, gids)
    sleepy_gid = argmax(total_minutes_asleep)
    sleepiest_minute = np.argmax(minutes_asleep[sleepy_gid])
    return sleepy_gid * sleepiest_minute

def answer2(minutes, logs, gids):
    minutes_asleep, _ = countSleepiness(minutes, logs, gids)
    most_sleeps = np.max([v.max() for v in minutes_asleep.values()])
    sleepiest_gid = [k for k,v in minutes_asleep.items()
                     if np.any(v == most_sleeps)]
    assert len(sleepiest_gid) == 1, f"more than one gid found: {sleepiest_gid}"
    sleepiest_gid = sleepiest_gid[0]
    sleepiest_minute = np.argmax(minutes_asleep[sleepiest_gid])
    return sleepiest_minute * sleepiest_gid


if __name__ == "__main__":
    day = '04'
    print(f'Day {day}')
    print('------')
    print('Part 1: ', end='')
    x = read(day)
    minutes, logs = getMinAndLogs(x)
    gids = getGuardIDs(logs)

    print(answer1(minutes, logs, gids))
    print('\nPart 2: ', end='')
    print(answer2(minutes, logs, gids))

# Part 1: 138280
