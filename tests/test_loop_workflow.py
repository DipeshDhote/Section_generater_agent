import random
from langgraph.graph import StateGraph, END, START
from typing import List, TypedDict




# Create state for Agent
class InputState(TypedDict):
    name: str
    number: List[int]
    counter: int


# Define Functions
def greeting_node(state:InputState)->InputState:
    """This node greet"""
    state["name"] = f"Hi, {state['name']} !"
    state['counter'] = 0

    return state

def random_node(state:InputState)->InputState:
    state['number'].append(random.randint(1,10))
    state['counter'] += 1
    return state

def should_continue(state:InputState)->InputState:
    if state['counter'] < 3:
        return "loop"
    else:
        return "exit"
    

graph = StateGraph(InputState)

graph.add_node("greeting", greeting_node)
graph.add_node("random", random_node)

graph.add_edge(START, "greeting")
graph.add_edge("greeting", "random")

graph.add_conditional_edges(
    "random",
    should_continue,
    {
        "loop":"random",
        "exit" : END
    }
)

app = graph.compile()

from IPython.display import Image, display
display(Image(app.get_graph().draw_mermaid_png()))


response = app.invoke({"name": "Okan", "number": [], "counter": -1})

"""
Entering loop with counter: 1
Entering loop with counter: 2
Entering loop with counter: 3
Entering loop with counter: 4
"""

print(response)