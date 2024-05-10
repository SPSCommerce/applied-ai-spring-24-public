
from langchain.chains import LLMMathChain
from langchain.tools import Tool
from langchain_openai import ChatOpenAI


def load_llm_math_tool():
    # For wrapper we can use underscores, even though name will be llm-math
    llm = ChatOpenAI(
        temperature=0.1,
        verbose=True
    )
    return Tool(
        name="Calculator",
        description="Useful for when you need to answer questions about math.",
        func=LLMMathChain.from_llm(llm=llm).run,
        coroutine=LLMMathChain.from_llm(llm=llm).arun,
    )
