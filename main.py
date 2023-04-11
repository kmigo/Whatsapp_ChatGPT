from src.resources.driver import agent_driver
from src.resources.whatsapp import is_logged,new_messages,last_messages_current_conversation,send_message
from dotenv import load_dotenv
from src.bot.bot_attendant import BotAttendant
import time
load_dotenv()


class MainThread:
    def __init__(self) -> None:
        self.driver=agent_driver.open()
        self.driver.get('https://web.whatsapp.com/')
        

    def while_is_not_logged(self):
        while not is_logged(self.driver):
            time.sleep(1)
        self.while_is_logged()

    def while_is_logged(self):
        logged = is_logged(self.driver)
        while logged:
            new_messages_arrivied = new_messages(self.driver)
            last_messages_arrivied= last_messages_current_conversation(self.driver)
            bot = BotAttendant(self.driver,new_messages_arrivied,last_messages_arrivied)
            bot.run(send_message)
            time.sleep(1)
            logged = is_logged(self.driver)
            
        self.while_is_not_logged()
    
    def run(self):
        self.while_is_not_logged()



if __name__ == '__main__':
    
    main_thread = MainThread()
    main_thread.run()