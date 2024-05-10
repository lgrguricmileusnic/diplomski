from abc import ABCMeta, abstractmethod


class Handler(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def handle_msg(self, msg):
        pass

    @abstractmethod
    def set_socket(self, socket):
        pass
