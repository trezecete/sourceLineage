from fastapi import FastAPI, HTTPException, UploadFile, File, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import os
import json
from typing import List, Optional, Dict, Any, Set

from lineage_parser import LineageParser
from bigquery_service import BigQueryDataTransferService

app = FastAPI(title="IPNET BigQuery Lineage Explorer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

SA_INFO = {}

class ScanRequest(BaseModel):
    location: str = "us"
    start_table: Optional[str] = None

@app.post("/api/upload-sa")
async def upload_sa(file: UploadFile = File(...)):
    global SA_INFO
    try:
        content = await file.read()
        sa_json = json.loads(content)
        SA_INFO = sa_json
        return {"status": "success", "project_id": sa_json["project_id"]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/auth")
async def authenticate(sa_json: Dict[str, Any] = Body(...)):
    global SA_INFO
    try:
        SA_INFO = sa_json
        return {"status": "success", "project_id": sa_json["project_id"]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def filter_graph(nodes: Set[str], edges: List[Dict[str, Any]], search_pattern: str) -> Dict[str, Any]:
    if not search_pattern:
        return {"nodes": list(nodes), "edges": edges}

    search_pattern = search_pattern.lower().strip()
    
    adj = {}
    rev_adj = {}
    for edge in edges:
        s, t = edge["source"], edge["target"]
        adj.setdefault(s, []).append(edge)
        rev_adj.setdefault(t, []).append(edge)

    # Find the node that matches the pattern (exact or partial)
    # Priority 1: Exact match
    start_node = next((n for n in nodes if n.lower() == search_pattern), None)
    
    # Priority 2: Ends with pattern (e.g. dataset.table)
    if not start_node:
        start_node = next((n for n in nodes if n.lower().endswith(search_pattern)), None)
        
    # Priority 3: Contains pattern
    if not start_node:
        start_node = next((n for n in nodes if search_pattern in n.lower()), None)
        
    if not start_node:
        return {"nodes": [], "edges": []}

    reachable_nodes = {start_node}
    reachable_edges = []
    
    # Downstream (BFS)
    queue = [start_node]
    while queue:
        curr = queue.pop(0)
        for edge in adj.get(curr, []):
            neighbor = edge["target"]
            if neighbor not in reachable_nodes:
                reachable_nodes.add(neighbor)
                queue.append(neighbor)
            if edge not in reachable_edges:
                reachable_edges.append(edge)
    
    # Upstream (BFS)
    queue = [start_node]
    while queue:
        curr = queue.pop(0)
        for edge in rev_adj.get(curr, []):
            neighbor = edge["source"]
            if neighbor not in reachable_nodes:
                reachable_nodes.add(neighbor)
                queue.append(neighbor)
            if edge not in reachable_edges:
                reachable_edges.append(edge)

    return {
        "nodes": list(reachable_nodes),
        "edges": reachable_edges
    }

@app.post("/api/scan")
async def scan_lineage(request: ScanRequest):
    global SA_INFO
    if not SA_INFO:
        raise HTTPException(status_code=401, detail="No credentials")

    try:
        service = BigQueryDataTransferService(SA_INFO)
        queries = service.list_scheduled_queries(location=request.location)
        
        all_nodes = set()
        all_edges = []
        
        for q in queries:
            sql = q["query"]
            sources, destinations, rels = LineageParser.extract_tables(sql)
            
            for d in destinations:
                all_nodes.add(d)
                for s in sources:
                    all_nodes.add(s)
            
            for r in rels:
                all_edges.append({
                    "source": r["source"], 
                    "target": r["target"], 
                    "columns": r.get("columns", ""),
                    "query_name": q["name"]
                })
        
        unique_edges = []
        seen = set()
        for e in all_edges:
            key = (e["source"], e["target"], e["columns"])
            if key not in seen:
                unique_edges.append(e)
                seen.add(key)

        result = filter_graph(all_nodes, unique_edges, request.start_table)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", response_class=HTMLResponse)
async def get_index():
    with open("frontend/index.html", "r", encoding="utf-8") as f:
        return f.read()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
