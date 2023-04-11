from src.bot.bot import Bot,BotAction
from src import models
class BotAttendantQuestion(BotAction):
    def __init__(self,name,type_response) -> None:
        super().__init__()
        self.name = name
        self.response = None
        self.type_response = type_response
    def execute(self,data=None):
        try:
            self.response = self.type_response(data)
            return True
        except:
            return False


    def __repr__(self) -> str:
        return self.name
    
class BotAttendant(Bot):
    actions : BotAction = [BotAttendantQuestion('Qual o seu nome',str)]
    def __init__(self, contact:models.Contact) -> None:
        super().__init__()
        self.contact = contact
    def run(self):
        action : BotAction= self.actions[self.contact.bot_action]
        if  self.contact.last_message_answered == None:
            #  1 enviar menssagem de comprimento
            # 2 enviar questão
            self.contact.last_message_answered =''
            self.contact.last_reply_sent = action.name
            return True
        if self.contact.last_message_answered == '':
            message = self.contact.last_messages[-1]
            self.contact.last_message_answered = message
            self.contact.confirmation = True
            # 1 enviar uma nesagem pedindo a confirmaçao da resposta
            """
            send_message("pode repetir sua resposta para que posssamos confirmar?")
            """
            return True
        if self.contact.confirmation:
            if self.contact.last_message_answered != self.contact.last_messages[-1]:
                message = self.contact.last_messages[-1]
                self.contact.last_message_answered =''
                """
                send_message("Desculpe vc deu uma resposta diferente da ultima, pode repetir sua resposta novamente?")
                """
                return True
            self.contact.last_message_answered = None
            self.contact.last_reply_sent = None
            self.contact.confirmation=False
            current_action = self.contact.bot_action
            total_questions = len(self.actions)
            self.contact.bot_action = current_action +1 if current_action < (total_questions-1) else 0
            return self.contact.bot_action
            

        