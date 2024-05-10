import logging

from fastapi import APIRouter
from openai import OpenAI
from datetime import datetime

from models import SimpleChatResponse, Chat

logger = logging.getLogger(__name__)
router = APIRouter()

# try http://localhost:8000/v0/models
@router.get("/models")
def get_models():
    client = OpenAI()
    models = client.models.list().data
    # We could return this list as is, but we want to sort it by creation date
    # and convert the timestamp to a more human readable format
    for model in models:
        model.created = datetime.fromtimestamp(model.created)
    sorted_models = sorted(models, key=lambda x: x.created, reverse=True)
    return {'data': sorted_models}


@router.post("/chat",
             response_model=SimpleChatResponse,
             summary="Uses an agent to answer chat questions",
             description="Uses an agent to answer chat questions"
             )
def post_chat(body: Chat) -> SimpleChatResponse:
    system_message = ("You are an AI Assistant that helps the user in their daily life. You can help with math, "
                      "weather, work questions, and more.")
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": body.question}
        ]
    )
    logger.error(f"Got completion: {completion.choices[0].message}")
    return SimpleChatResponse(response=completion.choices[0].message.content)
