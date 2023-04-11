from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from typing import List
from src import models
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
import time,os
from selenium.webdriver.common.action_chains import ActionChains
from src.utils import terminal as tr

def is_new_message(element:WebElement):
    css_selector='span[data-testid="icon-unread-count"]'
    time.sleep(1)
    found = element.find_elements(By.CSS_SELECTOR,css_selector)
    return len(found) >= 1

def text_element_message(element:WebElement):
    class_name_text_message = 'span[dir="ltr"][aria-label][class="_11JPr selectable-text copyable-text"]'
    try:
        found = element.find_elements(By.CSS_SELECTOR,class_name_text_message)
        return found[0].find_element(By.TAG_NAME,'span').text
    except :
        return ''
    
def serializer_element_current_conversation_to_model_contact(driver:WebDriver,element:WebElement = None):
    if element: element.click()
    time.sleep(1.5)
    css_selector_name_header = 'span[data-testid="conversation-info-header-chat-title"]'
    class_name_messages_received = 'div[class="message-in focusable-list-item _7GVCb _2SnTA _1-FMR"]'
    name_contact = driver.find_element(By.CSS_SELECTOR,css_selector_name_header).text
    messages_in = driver.find_elements(By.CSS_SELECTOR,class_name_messages_received)
    minimum_message_get = len(messages_in) - 10 if len(messages_in) >= 10 else 0 
    messages_in = messages_in[minimum_message_get : ]
    messages = [text_element_message(element) for element in messages_in ]
    return models.Contact(
        web_element=element,
        name_contact=name_contact,
        last_messages=[message for message in messages if message !='']
    )

def new_messages(driver:WebDriver):
    css_selector = 'div[aria-label="Lista de conversas"][class="_3YS_f _2A1R8"]'
    time.sleep(1)
    panel_conversations_web_element = driver.find_elements(By.CSS_SELECTOR,css_selector)
    if panel_conversations_web_element ==[]:return[]
    panel_conversations_web_element = panel_conversations_web_element[0]
    panel_conversations_web_element = panel_conversations_web_element.find_elements(By.CSS_SELECTOR,'div[class="lhggkp7q ln8gz9je rx9719la"]')
    panel_conversations_web_element = [element for element in panel_conversations_web_element if is_new_message(element)]
    return [serializer_element_current_conversation_to_model_contact(driver,element=element) for element in panel_conversations_web_element ]

def last_messages_current_conversation(driver:WebDriver):
    css_selector_name_header = 'span[data-testid="conversation-info-header-chat-title"]'
    time.sleep(1)
    name_contact = driver.find_elements(By.CSS_SELECTOR,css_selector_name_header)
    if len(name_contact) >0:
        return serializer_element_current_conversation_to_model_contact(driver)
    return

def send_message(driver:WebDriver,message:str):
    input_field = driver.find_elements(By.CSS_SELECTOR, 'div[class="to2l77zo gfz4du6o ag5g9lrv bze30y65 kao4egtt"]')
    if len(input_field)>0:
        input_field[0].send_keys(message)
        input_field[0].send_keys(Keys.ENTER)
        return True
    return False

def fetch_conversation_by_name(driver:WebDriver,name:str):
    css_selector_name = f'span[dir="auto"][title="{name}"]'
    found = driver.find_elements(By.CSS_SELECTOR,css_selector_name)
    return [serializer_element_current_conversation_to_model_contact(driver,element=element) for element in found ] 

def is_logged(driver:WebDriver):
    css_selector_qrcode = 'div[data-testid="qrcode"]'
    tr.CustomPrint.clear_terminal()
    found = driver.find_elements(By.CSS_SELECTOR,css_selector_qrcode)
    if len(found) > 0:
        tr.CustomPrint.error('Usuário desconectado')
        return False
    else:
        tr.CustomPrint.success('Usuário connectado!!!')
        return True
    
        