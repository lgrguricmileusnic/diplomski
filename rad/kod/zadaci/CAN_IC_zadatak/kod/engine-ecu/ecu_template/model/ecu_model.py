from abc import ABCMeta

from ecu_template.model.listener.listener import Listener


class ECUModel(metaclass=ABCMeta):
    def __init__(self):
        self.listeners = set()
        pass

    def notify(self):
        for listener in self.listeners:
            listener.update(self)

    def attach_listener(self, listener: Listener):
        self.listeners.add(listener)

    def detach_listener(self, listener: Listener):
        self.listeners.remove(listener)
