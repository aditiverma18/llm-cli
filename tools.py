import time
def add(a,b):
    return a+b

def multiply(a,b):
    return a*b

def get_current_time():
    local_time=time.localtime()
    formatted_time=time.strftime("%Y-%m-%d %H:%M:%S",local_time)
    return formatted_time
