
from dataclasses import dataclass
import json
@dataclass
class User:

    def __init__(  self,  id:str,
    username:str,
    password:str):
        self.username=username
        self.password=password
        self.id=id
    def to_dict(self):
        return {"id":self.id, "username":  self.username , "password" :self.password}

    def to_json(self):
        return json.dumps({"id":self.id,"username":  self.username , "password" :self.password})
    

