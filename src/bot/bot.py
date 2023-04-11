from abc import ABC,abstractclassmethod

class BotAction(ABC):
    @abstractclassmethod
    def execute(self):
        raise  NotImplemented

class Bot(ABC):
    actions:BotAction=[]
    @abstractclassmethod
    def run(self):
        raise NotImplemented