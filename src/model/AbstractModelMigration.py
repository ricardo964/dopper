from abc import ABC, abstractmethod

class AbstractModelMigration(ABC):
    @abstractmethod
    def create(self) -> bool:
        pass

    @abstractmethod
    def drop(self) -> bool:
        pass