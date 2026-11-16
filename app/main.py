import re, uuid
from collections import Counter
from fastapi import FastAPI
from pydantic import BaseModel, Field

app=FastAPI(title="Enterprise AI Knowledge Assistant",version="1.0.0")
docs={}
class Document(BaseModel):
    title:str=Field(min_length=1,max_length=160)
    text:str=Field(min_length=20,max_length=100000)
class Question(BaseModel):
    question:str=Field(min_length=3,max_length=1000)
    top_k:int=Field(default=3,ge=1,le=10)
def words(s): return re.findall(r"[a-z0-9]+",s.lower())
def split(s): return [p.strip() for p in re.split(r"\n\s*\n",s) if p.strip()]
@app.get("/health")
def health(): return {"status":"ok","documents":len(docs)}
@app.post("/documents",status_code=201)
def ingest(d:Document):
    i=str(uuid.uuid4()); docs[i]={"id":i,"title":d.title,"chunks":split(d.text)}
    return {"id":i,"title":d.title,"chunks_created":len(docs[i]["chunks"])}
@app.get("/documents")
def list_docs(): return [{"id":d["id"],"title":d["title"],"chunks":len(d["chunks"])} for d in docs.values()]
@app.post("/ask")
def ask(q:Question):
    query=set(words(q.question)); hits=[]
    for d in docs.values():
        for n,chunk in enumerate(d["chunks"]):
            t=words(chunk); overlap=sum(Counter(t)[w] for w in query)
            score=overlap/max(len(t)**0.5,1)
            if overlap: hits.append({"document_id":d["id"],"title":d["title"],"chunk":n,"excerpt":chunk,"relevance":round(score,4)})
    hits=sorted(hits,key=lambda h:h["relevance"],reverse=True)[:q.top_k]
    if not hits: return {"answer":"Insufficient evidence in indexed documents.","citations":[],"abstained":True}
    return {"answer":"Review these retrieved passages; the response is intentionally evidence-first.","citations":hits,"abstained":False}
