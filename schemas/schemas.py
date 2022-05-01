from pydantic import BaseModel

#Used for post method; Declared the parameters required in request body
class Profile(BaseModel):
    id : int
    name : str
    age : int