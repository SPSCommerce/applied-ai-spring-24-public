import requests
from langchain_core.tools import tool


# https://python.langchain.com/v0.1/docs/modules/tools/custom_tools/
@tool
def aurora_forecast(x: str) -> str:
    """Get the aurora forecast for the next 3 days.
    Northern Lights for Nothern Hemisphere. Takes no input."""
    response = requests.get("https://services.swpc.noaa.gov/text/3-day-forecast.txt")
    if response.status_code == 200:
        return response.text
    else:
        return "Unable to get the aurora forecast."


def load_aurora_forecast_tool():
    return aurora_forecast
