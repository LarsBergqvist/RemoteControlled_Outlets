import threading

states = {}

lock = threading.Lock()

def get_state(groupNumber, buttonNumber):
    key = str(groupNumber) + '_' + str(buttonNumber)
    state = 'off'
    lock.acquire()
    try:
        if key in states:
            state = states[key]
    finally:
        lock.release()

    return state

def set_state(groupNumber, buttonNumber, state):
    key = str(groupNumber) + '_' + str(buttonNumber)

    lock.acquire()
    try:
        states[key] = state
    finally:
        lock.release()