from pydantic import BaseModel

class MessageInput(BaseModel):
    session_id: str
    message: str
