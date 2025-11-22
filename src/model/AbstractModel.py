from abc import ABC, abstractmethod

class AbstractModel(ABC):    
    @abstractmethod
    def save(self) -> bool:
        pass
