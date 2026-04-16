from langgraph.graph import StateGraph, END
from graph.state import ResearchState
from agents.orchestrator import orchestrator
from agents.researcher import researcher
from agents.retriever import retriever
from agents.analyst import analyst
from agents.writer import writer
from agents.critic import critic

workflow = StateGraph(ResearchState)
workflow.add_node("orchestrator_node", orchestrator)
workflow.add_node("researcher_node", researcher)
workflow.add_node("retriever_node", retriever)
workflow.add_node("analyst_node", analyst)
workflow.add_node("writer_node", writer)
workflow.add_node("critic_node", critic)
workflow.set_entry_point("orchestrator_node")
workflow.add_edge("orchestrator_node", "researcher_node")
workflow.add_edge("orchestrator_node", "retriever_node")
workflow.add_edge("researcher_node", "analyst_node")
workflow.add_edge("retriever_node", "analyst_node")
workflow.add_edge("analyst_node", "writer_node")
workflow.add_edge("writer_node", "critic_node")

app = workflow.compile()
print(app.get_graph().draw_mermaid())