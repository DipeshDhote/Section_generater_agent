from langgraph.graph import StateGraph, START, END

from app.graph.state import WorkflowState
from app.graph.routers import validation_router,has_more_sections_router
from app.graph.nodes.qdrant_nodes import get_available_sections_from_qdrant,get_chunks_by_current_section
from app.graph.nodes.constitution_nodes import rewrite_company_constitution
from app.graph.nodes.section_loop_nodes import init_section_loop, get_next_section
from app.graph.nodes.section_generation_nodes import generate_single_section
from app.graph.nodes.validation_nodes import validate_single_section
from app.graph.nodes.storage_nodes import store_section_result
from app.graph.nodes.retry_nodes import increment_retry_count

builder = StateGraph(WorkflowState)

# Nodes
builder.add_node("get_available_sections", get_available_sections_from_qdrant)
builder.add_node("rewrite_constitution", rewrite_company_constitution)
builder.add_node("init_section_loop", init_section_loop)
builder.add_node("get_next_section", get_next_section)
builder.add_node("get_section_chunks", get_chunks_by_current_section)
builder.add_node("generate_section", generate_single_section)
builder.add_node("validate_section", validate_single_section)
builder.add_node("increment_retry", increment_retry_count)
builder.add_node("store_section", store_section_result)

# Flow
builder.add_edge(START, "get_available_sections")
builder.add_edge("get_available_sections", "rewrite_constitution")
builder.add_edge("rewrite_constitution", "init_section_loop")
builder.add_edge("init_section_loop", "get_next_section")
builder.add_edge("get_next_section", "get_section_chunks")
builder.add_edge("get_section_chunks", "generate_section")
builder.add_edge("generate_section", "validate_section")

# Validation router
builder.add_conditional_edges(
    "validate_section",
    validation_router,
    {
        "retry": "increment_retry",
        "store": "store_section",
    }
)

builder.add_edge("increment_retry", "generate_section")

# Loop router
builder.add_conditional_edges(
    "store_section",
    has_more_sections_router,
    {
        "continue": "get_next_section",
        "end": END,
    }
)

graph = builder.compile()


