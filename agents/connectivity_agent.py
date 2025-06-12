from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from tools.connectivity_checker import check_connectivity_issues
from dotenv import load_dotenv
load_dotenv()
llm = ChatOpenAI(temperature=0, model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",max_tokens=400)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a connectivity analysis agent for Qatar Airways."),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

memory = ConversationBufferMemory(memory_key="agent_scratchpad", return_messages=True)

agent = create_openai_tools_agent(llm=llm, tools=[check_connectivity_issues], prompt=prompt)
connectivity_agent = AgentExecutor(agent=agent, tools=[check_connectivity_issues], memory=memory, verbose=True)
