from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from tools.cabin_crew_alert import generate_cabin_crew_alerts
from dotenv import load_dotenv
load_dotenv()
llm = ChatOpenAI(
    temperature=0,
    model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
    max_tokens=400
   
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are the final operations agent generating a cabin crew briefing based on flight data."),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

memory = ConversationBufferMemory(memory_key="agent_scratchpad", return_messages=True)

agent = create_openai_tools_agent(llm=llm, tools=[generate_cabin_crew_alerts], prompt=prompt)
crew_alert_agent = AgentExecutor(agent=agent, tools=[generate_cabin_crew_alerts], memory=memory, verbose=True)
