from src.bot.bot import Bot,BotAction
from src import models
from typing import List,Dict
from selenium.webdriver.remote.webdriver import WebDriver
from src.utils import terminal as tr
import time

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
    history_conversation :Dict[str,models.Contact]= {}
    actions : BotAction = [BotAttendantQuestion('Qual o seu nome',str),BotAttendantQuestion('Você comprou os ingressos com agt ?',int),BotAttendantQuestion('Qual foi o evento?',str)]
    new_conversations:List[models.Contact]
    def __init__(self,driver: WebDriver, new_messages:List[models.Contact]=[],last_messages_current_contact:models.Contact = None) -> None:
        super().__init__()
        self.driver = driver
        self.new_conversations = new_messages
        if last_messages_current_contact:
            contacts_found = list(filter(lambda x: x.name_contact == last_messages_current_contact.name_contact ,new_messages)) 
            if len(contacts_found) >=1:
                pass
            else:
                before_contact = list(filter(lambda x: x.name_contact == last_messages_current_contact.name_contact ,self.history_conversation.values())) 
                if before_contact:
                    if ''.join(last_messages_current_contact.last_messages) != ''.join(before_contact[0].last_messages):
                        self.new_conversations.append(last_messages_current_contact)
                else:
                    self.new_conversations.append(last_messages_current_contact)
        
    

    
    def run(self,send_message):
        for contact in self.new_conversations:
            contact_in_histrory = contact.name_contact in self.history_conversation
            contact_history = self.history_conversation.get(contact.name_contact,contact)
            equal_conversation =  self.history_conversation.get(contact.name_contact)
            equal_conversation = False if equal_conversation == None else equal_conversation.last_messages[-1] == contact.last_messages[-1]
            if contact_in_histrory and equal_conversation  and  not contact_history.confirmation:continue
            last_message = contact.last_messages[:]
            contact = self.history_conversation.get(contact.name_contact,contact)
            contact.last_messages = last_message
            if contact.web_element:
                contact.web_element.click()
                while not isinstance(self.bot_run_action(contact,send_message),bool):pass


    def _update_conversation_by_contact(self,contact:models.Contact):
        if not contact:return
        if contact.name_contact not in self.history_conversation:
            self.history_conversation[contact.name_contact] = contact
        self.history_conversation[contact.name_contact].last_messages = contact.last_messages

    def bot_run_action(self,contact:models.Contact,send_message):
        if contact.done:
            contact.done = False
            return True
        tr.CustomPrint.warning('Conversa com:', message=contact.name_contact)
        time.sleep(.5)
        action : BotAction= self.actions[contact.bot_action]
        if  contact.last_message_answered == None:
            #  1 enviar menssagem de comprimento
            # 2 enviar questão
            if len(contact.actions) <=0:
                send_message(driver = self.driver,message="Olá tudo bem com você? irei fazer algumas perguntas peço que responda de forma simples e objetiva")
            send_message(driver = self.driver,message=action.name)
            contact.last_message_answered =''
            contact.last_reply_sent = action.name
            self._update_conversation_by_contact(contact)
            return True
        if contact.last_message_answered == '':
            message = contact.last_messages[-1]
            contact.last_message_answered = message
            contact.confirmation = True
            # 1 enviar uma nesagem pedindo a confirmaçao da resposta
      
            send_message(driver = self.driver,message="pode repetir sua resposta para que possamos confirmar?")
            self._update_conversation_by_contact(contact)
            return True
        if contact.confirmation:
            if contact.last_message_answered != contact.last_messages[-1]:
                message = contact.last_messages[-1]
                contact.last_message_answered =''
                send_message(driver = self.driver, message="Desculpe vc deu uma resposta diferente da ultima, pode repetir sua resposta novamente?")
                self._update_conversation_by_contact(contact)
                return True
            contact.last_message_answered = None
            contact.last_reply_sent = None
            contact.confirmation=False
            current_action = contact.bot_action
            total_questions = len(self.actions)
            contact.bot_action = current_action +1 if current_action < (total_questions-1) else 0
            contact.actions.append(models.Questions(name=action.name,response=contact.last_messages[-1]))
            self._update_conversation_by_contact(contact)
            if len(contact.actions) == len(self.actions):
                send_message(driver=self.driver,message="Obrigado por nos ajudar a melhorar nossa atendiment até a proxima")
                resume = ''.join([f'{index} - {question.name}\nR: {question.response}\n' for index,question in enumerate(contact.actions)])
                send_message(driver=self.driver,message=resume)
            if contact.bot_action == 0:
                #criar um script pa salvar todas as respostas anteriores e zerar do contato
                contact.done = True
                
            
            return contact.bot_action
            

        