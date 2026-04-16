from loguru import logger

from langgraph.graph import (
        StateGraph,
        END
    )

from langgraph.checkpoint.sqlite import SqliteSaver 
from graph.state import ResearchState
from agents.orchestrator import orchestrator
from agents.researcher import researcher
from agents.retriever import retriever
from agents.analyst import analyst
from agents.writer import writer
from agents.critic import critic
from config.config import config


class graph():
    
    def __init__(self, query: str=""):
        self.query = {"query": query}
        self.checkpointer_config = {"configurable": {"thread_id": "session_001"}}
        
    @staticmethod
    def route_critic(state: ResearchState):
        if state.get("research_needed"):
            return "RESEARCH"
        elif state.get("revision_needed"):
            return "REVISION"
        else:
            return "FINISH"

    def run_graph(self):
        
        workflow = StateGraph(ResearchState)
        checkpointer_path = config.checkpointer_path

        #===============NODE CREATION======================
        workflow.add_node("orchestrator_node", orchestrator)
        workflow.add_node("researcher_node", researcher)
        workflow.add_node("retriever_node", retriever)
        workflow.add_node("analyst_node", analyst)
        workflow.add_node("writer_node", writer)
        workflow.add_node("critic_node", critic)


        #===============EDGE CREATION======================
        workflow.set_entry_point("orchestrator_node")
        workflow.add_edge("orchestrator_node", "researcher_node")
        workflow.add_edge("orchestrator_node", "retriever_node")
        workflow.add_edge("researcher_node", "analyst_node")
        workflow.add_edge("retriever_node", "analyst_node")
        workflow.add_edge("analyst_node", "writer_node")
        workflow.add_edge("writer_node", "critic_node")
        workflow.add_conditional_edges(
            "critic_node",
            self.route_critic,
            {
                "RESEARCH": "researcher_node",
                "REVISION": "writer_node",
                "FINISH": END,
            })
        #===============EXECUTION======================
        with SqliteSaver.from_conn_string(checkpointer_path) as memory:
            app = workflow.compile(
                checkpointer=memory
            )

            result = app.invoke(input=self.query, config=self.checkpointer_config)

        logger.info("Graph Execution Over")
        print(f"Writer Output: {result.get('writer_result')}")
        print(f"Number of Revision: {result.get('revision_count')-1}")