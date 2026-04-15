from typing import TypedDict, Annotated
import operator

class ResearchState(TypedDict):
    query: str
    web_search_result: str
    researcher_result: str
    retrieved_results: str
    analyst_result: str
    writer_result: str
    critic_result: str
    revision_needed: bool
    research_needed: bool
    revision_count: Annotated[int, operator.add]