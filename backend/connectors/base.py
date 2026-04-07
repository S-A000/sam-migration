from abc import ABC, abstractmethod

class BaseSource(ABC):
    @abstractmethod
    def extract_in_chunks(self, batch_size: int):
        pass

class BaseDestination(ABC):
    @abstractmethod
    def load(self, data):
        pass