from abc import ABC,abstractclassmethod
from typing import Any
class BotAction(ABC):
    name:str
    response:Any
    type_response=Any
    @abstractclassmethod
    def execute(self,data=None):
        raise  NotImplemented

class Bot(ABC):
    actions:BotAction=[]
    @abstractclassmethod
    def run(self):
        raise NotImplemented