from dotenv import load_dotenv 
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.messages import HumanMessage, AIMessage
from tools import tools
from schema import AnalysisOutput, SYSTEM_PROMPT

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature = 0.2)
parser = PydanticOutputParser(pydantic_object=AnalysisOutput)

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("placeholder","{chat_history}"),
    ("human", "{query}"),
    ("placeholder","{agent_scratchpad}")
]).partial(format_instructions= parser.get_format_instructions())

agent = create_tool_calling_agent(llm, prompt, tools)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

chat_history=[]
print("AI Data Analyst Here (type 'exit' to quit")
while True:
    q = input("\nYou: ")
    if q.lower()=="exit":break
    chat_history.append(HumanMessage(content=q))
    response = executor.invoke({"query":q,"chat_history":chat_history})
    try:
        ans = parser.parse(response["output"])
        print("Insight: ", ans.answer)
        if ans.chart_path:print("Chart Saved at ", ans.chart_path)
        chat_history.append(AIMessage(content=ans.answer))
    except Exception as e:
        print("Parse error: ",e, "\nRaw: ", response["output"])

