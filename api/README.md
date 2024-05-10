## Running locally
1. Be sure you're in the api directory of the project `cd api`
2. Create a virtual environment `python -m venv venv`
3. Activate the virtual environment `source venv/bin/activate`
4. Install the dependencies `pip install -r requirements.txt`
5. Create a `.env` file in the root of the project and add the following:
    ```env
    OPENAI_API_KEY=
    TAVILY_API_KEY=
    ```
6. Run the application `uvicorn main:app --reload`

You will now have a server running at `localhost:8000`

## Other Endpoints

[localhost:8000/v0/models](localhost:8000/v0/models)

Returns available OpenAI models sorted by date added
