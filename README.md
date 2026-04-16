# ResearchMAS

## A modular multi-agent research system with iterative self-reflection

### Key features
- Multi Agent (Orchestrator, Critic etc..)
- Parallel node processing
- State management
- Conditional Routing
- Reflection 
- Reducer-based state
- Multi-source grounding 
- Persistent checkpointer memory
- Persistent Vector Store
- Two-stage RAG integration
- Tools (Reranker, VectorSearch, Web Search)
- Error Handling
- Modular Design
- Centralized Configuration
- Structured Logging
- CLI runtime


### Tech Stack
- LangGraph
- LlamaIndex
- Loguru
- Groq
- Tavily
- HuggingFace

### Graph Structure
```mermaid
---
config:
  flowchart:
    curve: linear
---
graph TD;
        __start__([<p>__start__</p>]):::first
        orchestrator_node(orchestrator_node)
        researcher_node(researcher_node)
        retriever_node(retriever_node)
        analyst_node(analyst_node)
        writer_node(writer_node)
        critic_node(critic_node)
        __end__([<p>__end__</p>]):::last
        __start__ --> orchestrator_node;
        analyst_node --> writer_node;
        orchestrator_node --> researcher_node;
        orchestrator_node --> retriever_node;
        researcher_node --> analyst_node;
        retriever_node --> analyst_node;
        writer_node --> critic_node;
        critic_node --> __end__;
        classDef default fill:#f2f0ff,line-height:1.2
        classDef first fill-opacity:0
        classDef last fill:#bfb6fc
```


### Project Structure
```
ResearchMAS/
├── agents/
│   ├── orchestrator.py
│   ├── researcher.py
│   ├── retriever.py
│   ├── analyst.py
│   ├── writer.py
│   └── critic.py
├── config/
│   ├── config.py
│   └── settings.yaml
├── graph/
│   ├── graph.py
│   └── state.py
├── tools/
│   ├── vector_search.py
│   ├── reranker.py
│   └── web_search.py
├── memory/
├── ingestion.py
├── run.py
├── .env
└── .gitignore
```