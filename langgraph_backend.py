from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated, Literal
from langchain_groq import ChatGroq
import os 
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph.message import add_messages
from dotenv import load_dotenv


 
load_dotenv()


llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)
load_dotenv()

print("API Key:", os.getenv("GROQ_API_KEY"))

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

#define your function
def chat_node(state: ChatState):
    messages = state['messages']
    response = llm.invoke(messages)
    return{
        'messages': [response]
    }



## Define your Node 
graph = StateGraph(ChatState)
graph.add_node('chat_node', chat_node)

#add your edges
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

checkpointer = InMemorySaver()
chatbot = graph.compile(checkpointer=checkpointer)
