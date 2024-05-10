from pydantic import BaseModel


class SimpleChatResponse(BaseModel):
    response: str


class Chat(BaseModel):
    chatId: str = "default"
    question: str
    temperature: float = 0.2
    persona: str = "default"
