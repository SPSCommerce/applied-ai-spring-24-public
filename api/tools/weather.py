import logging

from langchain.tools import StructuredTool
from langchain_core.tools import ToolException
import openmeteo_requests
import requests_cache
from retry_requests import retry
import pandas as pd

# Code Example from
# https://open-meteo.com/

logger = logging.getLogger(__name__)
name = "weather_forecast"
description = ("Useful to get the weather forecast for the next 7 days"
            "The input to this tool is the latitude and longitude is one string in this format: 'lat: 44.9 lon: 93.2'"
               )


def _handle_error(error: ToolException) -> str:
    return f"The following errors occurred during {name} tool execution:" + error.args[0]


def get_weather(location_str: str):
    try:
        split_str = location_str.split()
        lat = float(split_str[1])
        lon = float(split_str[3])
        # Setup the Open-Meteo API client with cache and retry on error
        cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        openmeteo = openmeteo_requests.Client(session=retry_session)

        # Make sure all required weather variables are listed here
        # The order of variables in hourly or daily is important to assign them correctly below
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "uv_index_max", "precipitation_sum",
                      "precipitation_probability_max"],
            "temperature_unit": "fahrenheit",
            "wind_speed_unit": "kn",
            "precipitation_unit": "inch",
            "timezone": "auto",
            "forecast_days": 7
        }
        responses = openmeteo.weather_api(url, params=params)

        # Process first location. Add a for-loop for multiple locations or weather models
        response = responses[0]
        print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
        print(f"Elevation {response.Elevation()} m asl")
        print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
        print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

        # Process daily data. The order of variables needs to be the same as requested.
        daily = response.Daily()
        daily_weather_code = daily.Variables(0).ValuesAsNumpy()
        daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()
        daily_temperature_2m_min = daily.Variables(2).ValuesAsNumpy()
        daily_uv_index_max = daily.Variables(3).ValuesAsNumpy()
        daily_precipitation_sum = daily.Variables(4).ValuesAsNumpy()
        daily_precipitation_probability_max = daily.Variables(5).ValuesAsNumpy()

        daily_data = {"date": pd.date_range(
            start=pd.to_datetime(daily.Time(), unit="s", utc=True),
            end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=daily.Interval()),
            inclusive="left"
        ), "wmo_weather_code": daily_weather_code, "temperature_2m_max": daily_temperature_2m_max,
            "temperature_2m_min": daily_temperature_2m_min, "uv_index_max": daily_uv_index_max,
            "precipitation_sum": daily_precipitation_sum,
            "precipitation_probability_max": daily_precipitation_probability_max}

        daily_dataframe = pd.DataFrame(data=daily_data)
    except Exception as e:
        logger.error(f"The following errors occurred during {name} tool execution:  {e=}, {type(e)=}")
        raise ToolException(f"The following errors occurred during {name} tool execution: {type(e)=}")

    return daily_dataframe.to_dict(orient="records")


def load_weather_tool():
    return StructuredTool.from_function(
        name=name,
        func=get_weather,
        description=description,
        handle_tool_error=_handle_error
    )
