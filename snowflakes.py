import time

i = -1
last_timestamp = int(time.time())

def reset_increment_per_ms():
    global i, last_timestamp
    if int(time.time() * 1000) > last_timestamp:
        i = -1

def get_snowflake(type : str):
    global i, last_timestamp
    type_id = {"user" : 0, "goal" : 1, "step" : 2}[type]
    reset_increment_per_ms()
    last_timestamp = int(time.time() * 1000)
    i += 1
    return (last_timestamp - 1536328800000) * (2 ** 22) + \
            type_id * (2 ** 17) + \
            0 * (2 ** 12) + \
            i