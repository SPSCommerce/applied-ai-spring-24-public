# Applied AI Conference Talk 
### Spring 2024


API &amp; UI for learning about Agents, Tools, and Personas

## Abstract

## Installation and Use with Docker
The easiest way to run the server locally is to use Docker. Execute the following command to build and run the application:
```bash
docker-compose up --build
```
The API will be running at http://localhost:8000
The UI will be running at http://localhost:5173

## Installation and Use without Docker
Each folder UI and API has its own README.md file with installation instructions.
There is a section in /ui/vite.config.ts that needs to be commented in for non-docker setup.

The API will be running at http://localhost:8000
The UI will be running at http://localhost:5173

## ENV Variables
The API requires the following environment variables to be set in the api/.env file

```
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
```

https://platform.openai.com/api-keys

https://app.tavily.com/home
