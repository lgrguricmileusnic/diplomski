from abc import ABCMeta, abstractmethod


class Listener(metaclass=ABCMeta):
    @abstractmethod
    def update(self, model):
        pass
