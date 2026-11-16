from fastapi.testclient import TestClient
from app.main import app,docs
c=TestClient(app)
def setup_function(): docs.clear()
def test_ingest_and_cited_retrieval():
    r=c.post("/documents",json={"title":"Security policy","text":"Company laptops must use full disk encryption and multi factor authentication."})
    assert r.status_code==201
    a=c.post("/ask",json={"question":"What encryption and authentication must laptops use?"}).json()
    assert not a["abstained"] and a["citations"][0]["title"]=="Security policy"
def test_abstains_without_evidence():
    assert c.post("/ask",json={"question":"Weather on Mars?"}).json()["abstained"]
