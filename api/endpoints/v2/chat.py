import importlib
from fastapi import APIRouter
from langchain.agents import load_tools, AgentType, initialize_agent
from langchain_openai import ChatOpenAI
# from langchain_cohere import ChatCohere

from memory.session_memory import SessionMemory
from .personas import personas

from models import Chat, SimpleChatResponse
import logging

from langchain_core.runnables.history import RunnableWithMessageHistory

session_memory = SessionMemory()
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/chat",
             response_model=SimpleChatResponse)
def chat_with_persona(body: Chat):
    # Get the persona from the list of personas
    persona = [persona for persona in personas if persona.get("name", "") == body.persona][0]
    # Get the system message from the persona
    system_message = persona.get("system_prompt", "")
    logger.info(f"System Message : {system_message}")

    llm = ChatOpenAI(
        model_name="gpt-4-turbo-2024-04-09",
        temperature=body.temperature,
        verbose=True
    )
    # llm = ChatCohere(model="command", verbose=True)
    # llm.temperature = body.temperature
    tools = load_tools([], llm=llm)
    tools.extend(load_persona_tools(persona.get("tools", [])))

    agent = initialize_agent(tools=tools,
                             llm=llm,
                             agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
                             verbose=True,
                             return_intermediate_steps=True,
                             max_iterations=25,
                             handle_parsing_errors=True)

    agent_with_chat_history = RunnableWithMessageHistory(
        agent,
        session_memory.get_memory,
        input_messages_key="input",
        history_messages_key="chat_history",
    )

    response = agent_with_chat_history.invoke(
        {"system_message": system_message, "input": body.question},
        config={"configurable": {"session_id": body.chatId}},
    )

    logger.info(f"Response: {response}")
    return SimpleChatResponse(response=response.get("output", "No response found"))


# Load the tools for the persona
# Use a convention to allow looping through the list of tools
# import from tools folder, loader is load_{tool}_tool
def load_persona_tools(persona_tools):
    tools = []
    for tool in persona_tools:
        try:
            module_name = f"tools.{tool}"
            function_name = f"load_{tool}_tool"
            module = importlib.import_module(module_name)
            function = getattr(module, function_name)
            tools.append(function())
        except Exception as e:
            logger.error(f"Error loading tool {tool}: {e}")
    return tools
