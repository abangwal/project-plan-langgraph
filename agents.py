from langchain_openai import ChatOpenAI
from structure import KeyPointsSchema, PlanSchema, GraderSchema
from langchain.chains.openai_functions import create_structured_output_runnable
from langchain_core.prompts import ChatPromptTemplate


## Prompt Template ##
MARKETMAN_TEMPLATE = """For the given objective, come up with at least ten key-points user should do to achive the objective. \
These key-points should involve all the important task to do in market researh, if the key-points are executed correctly will complete the objective. \
Put number before each key-point also consider FEEDBACK if provided to genrate better response than before.

OBJECTIVE:
{objective}

FEEDBACK:
{feedback}
"""

PLANNER_TEMPLATE = """For the given SUB TASK, come up with a deataild plan to complete the SUB TASK condidering this SUB TASK with contribute in completing the ULTIMATE TASK.\
Plan should be clear, detailed, and helpful in achiving the SUB TASK hence helping with ULTIMATE TASK. Plan should be sorted, and if executed correctly should complete the SUB TASK.\
Put number before each plan step.

ULTIMATE TASK:
{task}

SUB TASK :
{step}
"""

GRADER_TEMPLATE = """You are a strict market researcher that Grade the RESPONSE out of 10 based on the OBJECTIVE and provide a detailed feedback to improve the response.\
Grade must be an integer and should range between 0-10 where higher number means better response to achive the given objective.\

OBJECTIVE:
{objective}

RESPONSE:
{response}
"""

api_key = ""


def MarketMan():
    model = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0,
        streaming=True,
        api_key=api_key,
    )

    prompt = ChatPromptTemplate.from_template(MARKETMAN_TEMPLATE)
    runnable = create_structured_output_runnable(
        output_schema=KeyPointsSchema, llm=model, prompt=prompt
    )

    return runnable


def Planner():

    model_kwargs = {"frequency_penalty": 1}

    model = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=1,
        model_kwargs=model_kwargs,
        streaming=True,
        api_key=api_key,
    )

    prompt = ChatPromptTemplate.from_template(PLANNER_TEMPLATE)
    runnable = create_structured_output_runnable(
        output_schema=PlanSchema, llm=model, prompt=prompt
    )

    return runnable


def Grader():
    model = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=1,
        streaming=True,
        api_key=api_key,
    )

    prompt = ChatPromptTemplate.from_template(GRADER_TEMPLATE)
    runnable = create_structured_output_runnable(
        output_schema=GraderSchema, llm=model, prompt=prompt
    )
    return runnable


## test inference
"""
agent1 = MarketMan()
agent2 = Planner()
agent3 = Grader()
response = agent1.invoke(
    {"objective": "Do market researh on a EV startup", "feedback": ""}
)
print(response.steps, "\n")

response2 = agent2.invoke({"step": response.steps[1], "feedback": ""})
print(response2.plan, "\n")

response3 = agent3.invoke({"objective": response.steps[1], "response": response2.plan})
print(response3.grade, "\n\n", response3.feedback)

response4 = agent2.invoke({"step": response.steps[1], "feedback": response3.feedback})
print("After feedback :", "\n\n", response4.plan)"""
