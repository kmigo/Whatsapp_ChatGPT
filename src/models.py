from typing import Optional,List,Any

from pydantic import BaseModel

class Contact(BaseModel):
    web_element:Any
    last_message_answered:Optional[str]=None
    last_messages:List[str] = []
    last_reply_sent:Optional[str] = None
    name_contact:str