receivers = {}

def connect(receiver, signal):
    if signal not in receivers:
        receivers[signal] = []
    receivers[signal].append(receiver)


def send(signal, *arguments, **named):
    if signal not in receivers:
        return
    for receiver in receivers[signal]:
        receiver(*arguments, **named)
