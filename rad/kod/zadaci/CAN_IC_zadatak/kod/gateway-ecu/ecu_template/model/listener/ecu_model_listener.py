from abc import abstractmethod

from .listener import Listener
from ..ecu_model import ECUModel


class ECUModelListener(Listener):
    @abstractmethod
    def update(self, model: ECUModel):
        pass
