from abc import ABCMeta, abstractmethod


class Controller(metaclass=ABCMeta):
    @abstractmethod
    def start(self):
        raise NotImplementedError

    @abstractmethod
    def stop(self):
        raise NotImplementedError
