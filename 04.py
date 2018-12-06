from util import read
import numpy as np
import pandas as pd
from collections import defaultdict

def parseInfo(s):
    s = s.split('[')[1]
    datetime, info = s.split('] ')
    return datetime, info

def parseDatetime(s):
    year, month, s = s.split('-')
    day, s = s.split(' ')
    hour, minute = s.split(':')
    year, month, day = int(year), int(month), int(day)
    hour, minute = int(hour), int(minute)
    return pd.datetime(year, month, day, hour, minute)

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


def getDttmAndLogs(x):
    info = [parseInfo(s) for s in x]
    datetimes, logs = list(zip(*info))
    datetimes = np.array(datetimes)
    logs = np.array(logs)
    idx = np.argsort(datetimes)
    datetimes = datetimes[idx]
    datetimes = np.array([parseDatetime(s) for s in datetimes])
    logs = logs[idx]
    return datetimes, logs


def countSleepiness(df):
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
    minutes_asleep = {i: np.zeros(60) for i in gid}
    for j in range(df.shape[0]):
        row = df.iloc[j, :]
        if 'falls asleep' in row.log:
            rrow = df.iloc[j+1, :]
            t0 = row.minute
            if ('wakes up' in rrow.log) and (rrow.gid == row.gid):
                t1 = rrow.minute
            else:
                t1 = 60
            minutes_asleep[row.gid][t0:t1] += 1
            total_minutes_asleep[row.gid] += (t1 - t0)
    return minutes_asleep, total_minutes_asleep


def argmax(dd):
    vmax = np.max([v for v in dd.values()])
    amax = [k for k, v in dd.items() if v == vmax]
    if len(amax) == 1:
        amax = amax[0]
    return amax

def answer1(df):
    minutes_asleep, total_minutes_asleep = countSleepiness(df)
    sleepy_gid = argmax(total_minutes_asleep)
    sleepiest_minute = np.argmax(minutes_asleep[sleepy_gid])
    return sleepy_gid * sleepiest_minute

def answer2(df):
    minutes_asleep, _ = countSleepiness(df)
    most_sleeps = np.max([v.max() for v in minutes_asleep.values()])
    sleepiest_gid = [k for k,v in minutes_asleep.items()
                     if np.any(v == most_sleeps)]
    assert len(sleepiest_gid) == 1, "more than one gid found."
    sleepiest_gid = sleepiest_gid[0]
    sleepiest_minute = np.argmax(minutes_asleep[sleepiest_gid])
    return sleepiest_minute * sleepiest_gid


if __name__ == "__main__":
    day = '04'
    print(f'Day {day}')
    print('------')
    print('Part 1: ', end='')
    x = read(day)
    datetimes, logs = getDttmAndLogs(x)
    gid = getGuardIDs(logs)

    df = pd.DataFrame(
        np.column_stack((datetimes, logs, gid)),
        columns=['dttm', 'log', 'gid'])
    df['minute'] = df.dttm.apply(lambda x: x.minute)
    df2 = df.loc[df.log.isin(['falls asleep', 'wakes up'])]

    print(answer1(df))
    print('\nPart 2: ', end='')
    print(answer2(df))

    
    
    
    
# Part 1: 138280

# Part 2: 
# p2_wrong_answers = [36119, ]
