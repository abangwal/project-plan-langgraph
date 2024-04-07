from structure import GraphState
from agents import MarketMan, Planner, Grader
from langgraph.graph import StateGraph, END


## Agents initialize
market_man = MarketMan()
planner = Planner()
grader = Grader()


## Define nodes
def market_man_node(state: GraphState):
    task = state["task"]
    feedback = state["feedback"]
    response = market_man.invoke({"objective": task, "feedback": feedback})
    if state["sender"] == "grader":
        next_node = "planner"
    else:
        next_node = "grader"
    return {
        "messages": [response],
        "steps": response.steps,
        "sender": "marketMan",
        "next_node": next_node,
    }


def planner_node(state: GraphState):
    task = state["task"]
    sub_task = state["steps"][int(input("Enter the step you want planning on : ")) - 1]
    current_plans = state["plan"]
    try:
        if sub_task not in current_plans.keys():
            response = planner.invoke({"task": task, "step": sub_task})
            current_plans[sub_task] = response.plan
            return {
                "messages": [response],
                "plan": current_plans,
                "sender": "planner",
                "next_node": "planner",
            }
        elif len(current_plans.keys()) == len(state["steps"]):
            return {"sender": "planner", "next_node": "end"}
        else:
            return {"sender": "planner", "next_node": "planner"}
    except:
        response = planner.invoke({"task": task, "step": sub_task})
        current_plans = {}
        current_plans[sub_task] = response.plan
        return {
            "messages": [response],
            "plan": current_plans,
            "sender": "planner",
            "next_node": "planner",
        }


def grader_node(state: GraphState):
    task = state["task"]
    steps = state["steps"]
    response = grader.invoke({"objective": task, "response": steps})
    return {
        "messages": [response],
        "feedback": response.feedback,
        "sender": "grader",
        "next_node": state["sender"],
    }


def router(state: GraphState):
    return state["next_node"]


## Stich web
def workflow_graph():
    workflow = StateGraph(schema=GraphState)

    workflow.add_node("marketMan", market_man_node)
    workflow.add_node("planner", planner_node)
    workflow.add_node("grader", grader_node)

    workflow.add_conditional_edges(
        "marketMan", router, {"planner": "planner", "grader": "grader"}
    )
    workflow.add_conditional_edges(
        "planner", router, {"planner": "planner", "end": END}
    )
    workflow.add_conditional_edges("grader", router, {"marketMan": "marketMan"})

    workflow.set_entry_point("marketMan")
    app = workflow.compile()

    return app


# app.get_graph().draw_png("graph_by_langGraph.png")
