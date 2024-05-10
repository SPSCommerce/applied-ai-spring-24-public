from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class Persona(BaseModel):
    name: str
    description: str
    system_prompt: str
    tools: list[str]


class Personas(BaseModel):
    personas: list[Persona]


personas = [
    {
        "name": "Weekend",
        "description": "AI agent that helps the user with their weekend summer plans.",
        "system_prompt": ("You are an AI agent that helps the user with their weekend plans. You can "
                          "provide recommendations for activities, restaurants, and more."
                          "If they ask a question but have not provided a location, ask for a location before "
                          "providing a response."
                          "Once you've received their question, make a plan as to how you'll find the answers for it."
                          "Then follow your plan and provide the user with the information they requested."
                          "Present the information in a user-friendly manner, encouraging interaction "
                          "and providing options for further details if requested by the user."),
        "tools": ["weather", "tavily_search_results_json", "aurora_forecast"]
    },
    {
        "name": "Workday",
        "description": "Query the Employee Handbook and perform other research.",
        "system_prompt": "You are an AI Assistant that helps the user with their "
                         "workday working in Human Resources. "
                         "You can help read the handbook, do web research and math.",
        "tools": ["employee_handbook", "tavily_search_results_json", "llm_math"]
    }
]


@router.get("/personas", response_model=Personas)
def get_personas():
    return {"personas": personas}


@router.get("/personas/{persona_name}",
            response_model=Persona)
def get_personas(persona_name: str):
    found = [persona for persona in personas if persona['name'] == persona_name]
    if found:
        return found[0]
    else:
        raise HTTPException(status_code=404, detail="Persona not found")
