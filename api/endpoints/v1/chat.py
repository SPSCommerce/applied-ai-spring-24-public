from fastapi import APIRouter
from langchain.agents import load_tools, AgentType, initialize_agent
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.runnables.history import RunnableWithMessageHistory

from memory.session_memory import SessionMemory
from tools.aurora_forecast import aurora_forecast
from tools.employee_handbook import load_employee_handbook_tool
from tools.weather import load_weather_tool
from tools.tool_template import load_tool as load_pig_latin_tool

from models import Chat, SimpleChatResponse
import logging
logger = logging.getLogger(__name__)
router = APIRouter()
session_memory = SessionMemory()


@router.post("/chat",
            response_model=SimpleChatResponse)
def chat_with_persona(body: Chat):
    system_message = ("You are an AI Assistant that helps the user in their daily life. You can help with math, "
            "weather, work questions, and more.")
    llm = ChatOpenAI(
        model_name="gpt-4-turbo-2024-04-09",
        temperature=body.temperature,
        verbose=True
    )
    tools = load_tools(["llm-math"], llm=llm)
    tools.append(load_weather_tool())
    tools.append(TavilySearchResults(max_results=1))
    tools.append(load_employee_handbook_tool())
    tools.append(load_pig_latin_tool())
    tools.append(aurora_forecast())


    # Agents
    # Read more here https://python.langchain.com/docs/modules/agents/agent_types/
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

