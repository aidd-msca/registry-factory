from abc import ABC, abstractmethod
from registry_factory.index import HashTable


class Mediator(ABC):
    @abstractmethod
    def send(self, sender, message):
        raise NotImplementedError


class HashMediator(Mediator):
    def send(self, sender, message):
        HashTable().set(message[0], message[1], message[2], message[3])
