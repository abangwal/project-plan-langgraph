from graph import workflow_graph

app = workflow_graph()

query = input("Enter query : ")

for s in app.stream({"task": query, "feedback": ""}):
    agent_name = list(s.keys())[0]
    if agent_name == "marketMan":
        print(
            "\n######## Key Points to consider while doing market research ##########\n"
        )
        steps = s["marketMan"]["steps"]
        for step in steps:
            print(step)
        print("\n")

    if agent_name == "grader":
        print("\n######## Rethining above response ########\n")

    if agent_name == "planner":
        plan = s["planner"]["plan"]
        focus = list(plan.keys())[-1]
        print("\n######## Planning for asked step ########")
        print(f"\n Asked step : {focus}\n")
        for i in plan[focus]:
            print(i)
        print("\n")
