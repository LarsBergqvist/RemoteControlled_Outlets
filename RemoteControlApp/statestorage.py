import threading

states = {}

lock = threading.Lock()

def get_state(buttonNumber):
    key = str(buttonNumber)
    state = 'off'
    lock.acquire()
    try:
        if key in states:
            state = states[key]
    finally:
        lock.release()

    return state

def set_state(buttonNumber, state):
    key = str(buttonNumber)

    lock.acquire()
    try:
        states[key] = state
    finally:
        lock.release()