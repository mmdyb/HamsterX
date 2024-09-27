import asyncio
from warna import *

async def countdown(i):
    for i in range(i, 0, -1):
        minutes, seconds = divmod(i, 60)
        hours, minutes = divmod(minutes, 60)
        seconds = str(seconds).zfill(2)
        minutes = str(minutes).zfill(2)
        hours = str(hours).zfill(2)
        
        c = gt
        if int(seconds) < 10:
            c = rt
        print(f"{wb}waiting{rs} {c}{hours}:{minutes}:{seconds}{rs} ", flush=True, end="\r")
        await asyncio.sleep(1)

def number_to_string(num):
    if num < 1000:
        return str(num)
    elif num < 1000000:
        return str(round(num / 1000, 2)) + "k"
    elif num < 1000000000:
        return str(round(num / 1000000, 2)) + "m"
    elif num < 1000000000000:
        return str(round(num / 1000000000, 2)) + "b"
    else:
        return str(round(num / 1000000000000, 2)) + "t"