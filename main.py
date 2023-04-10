from src.resources.driver import agent_driver
from src.resources.whatsapp import is_logged,new_messages
from dotenv import load_dotenv
import time
load_dotenv()

driver = agent_driver.open()

class MainThread:
    def __init__(self,driver) -> None:
        self.driver=driver
        driver.get('https://web.whatsapp.com/')

    def while_is_not_logged(self):
        while not is_logged(self.driver):
            time.sleep(1)
        self.while_is_logged()

    def while_is_logged(self):
        logged = is_logged(self.driver)
        while logged:
            print(new_messages(self.driver))
            time.sleep(1)
            logged = is_logged(self.driver)
        self.while_is_not_logged()
    
    def run(self):
        self.while_is_not_logged()

main_thread = MainThread(driver)

if __name__ == '__main__':
    main_thread.run()