from dotenv import load_dotenv
import os

import logging
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.tools import Tool
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.llms.openai import OpenAI
from langchain_community.vectorstores import InMemoryVectorStore
from langchain_core.tools import ToolException

name = "employee_handbook"
description = "Query the employee handbook for information. You can query the employee handbook for information by passing in a string."
logger = logging.getLogger(__name__)


def _handle_error(error: ToolException) -> str:
    return f"The following errors occurred during {name} tool execution:" + error.args[0]


def get_answer(question: str):
    try:
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        loader = PyPDFLoader("tools/files/Handbook.pdf")
        data = loader.load_and_split(splitter)
        vectorstore = InMemoryVectorStore.from_documents(
            data,
            OpenAIEmbeddings(model="text-embedding-3-large")
        )

        chain = RetrievalQA.from_chain_type(
            llm=OpenAI(),
            chain_type="stuff",
            retriever=vectorstore.as_retriever(search_kwargs={'k': 5})
        )

        return chain.run(question)
    except Exception as e:
        logger.error(f"Error:{e}")
        raise ToolException(f"The following errors occurred during {name} tool execution: {type(e)=}")


if __name__ == "__main__":
    load_dotenv()
    print(get_answer("What is the dress code?"))


def load_employee_handbook_tool():
    return Tool.from_function(
        name=name,
        func=get_answer,
        description=description,
        handle_tool_error=_handle_error,
    )
