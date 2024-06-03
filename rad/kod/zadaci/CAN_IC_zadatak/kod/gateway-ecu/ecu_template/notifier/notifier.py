from abc import ABCMeta, abstractmethod


class Notifier(metaclass=ABCMeta):
    @abstractmethod
    def _rx_thread(self):
        raise NotImplementedError

    @abstractmethod
    def start(self):
        raise NotImplementedError

    @abstractmethod
    def stop(self, timeout: float = 5.0):
        raise NotImplementedError

    @abstractmethod
    def add_listener(self, listener):
        raise NotImplementedError

    @abstractmethod
    def remove_listener(self, listener):
        raise NotImplementedError
