from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages

from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

class ChatState(TypedDict):
    # basically here in order to update the state we are using reducer functions in langGraph
    messages: Annotated[list[BaseMessage], add_messages]

# defining our LLM 
llm = ChatGoogleGenerativeAI(
    api_key = os.environ.get("GOOGLE_GEMINI_API_KEY"),
    model = os.environ.get("GOOGLE_LLM_MODEL")
)

def chat_node(state: ChatState):
    # take user query from the state
    messages = state['messages']
    # send to LLM and get response
    response = llm.invoke(messages)
    # store the response in the state and return the state
    return {'messages': [response]}

# creating a checkpoint to save the conversation history
# checkpoint = MemorySaver()
checkpoint = InMemorySaver()

# defining out graph
graph  = StateGraph(ChatState)

# defining our nodes
graph.add_node('chat_node',chat_node)

# defing our edges
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

# compiling the graph
chatbot = graph.compile(checkpointer=checkpoint)



