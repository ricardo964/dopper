from abc import ABC, abstractmethod

class AbstractModel(ABC):    
    @abstractmethod
    def save(self) -> bool:
        pass
    
    @abstractmethod
    def update(self, **kwargs) -> bool:
        pass
    
    @classmethod
    @abstractmethod
    def find_by_id(_class, id: str) -> 'AbstractModel':
        pass

    # @classmethod
    # @abstractmethod
    # def delete_by_id(_class, id) -> bool:
    #     pass
